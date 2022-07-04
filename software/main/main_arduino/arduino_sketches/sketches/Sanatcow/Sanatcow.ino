/*******************************************************************************
   Этот скетч отправляет данные с датчиков в сеть TTN


  Необходимые библиотеки:
  1) https://github.com/Risele/SHT3x.git
  2) https://github.com/matthijskooijman/arduino-lmic
  3) https://github.com/rocketscream/Low-Power.git


   Используется активация при помощи персонализации (ABP).
   В скетч зашит:
   уникальный адрес устройства - DevAddr
   сессионные ключи - NetSessionkey, AppSessionKey

   в OTAA активации эти ключи генерируются на устройстве

   Для правильной работы модуля нужно задать правильные настройки в Documents/Arduino/libraries/arduino-lmic-master/config.h
   нужно раскомментировать строки с disable_join, disable_ping, disable_beacons


 *******************************************************************************/
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
//#include <Wire.h>
#include <SoftwareSerial.h>

#define F_CPU 8000000UL


SoftwareSerial rpiSer =  SoftwareSerial(10, 11); // rxPin, txPin
uint8_t rpiData[23] = {0,};
uint8_t index = 0;
/*==============================================
  Настройка RFM95W
  ===============================================*/
// NWKSKEY - заменить на правильный при регистрации устройства в TTN (msb)
static const PROGMEM u1_t NWKSKEY[16] = { 0xDB, 0x5D, 0xEF, 0x7A, 0x42, 0x81, 0x4D, 0xC1, 0x8E, 0x33, 0xCE, 0x24, 0x1F, 0xDA, 0xB9, 0x20 };

// APPSKEY - заменить на правильный при регистрации устройства в TTN (msb)
static const u1_t PROGMEM APPSKEY[16] = { 0x9C, 0x68, 0x49, 0x1E, 0x48, 0xE5, 0xD8, 0xC6, 0x0C, 0x26, 0xF4, 0x89, 0xFB, 0x14, 0x51, 0xA6 };

// DEVADDR - заменить на правильный при регистрации устройства в TTN
static const u4_t DEVADDR = 0x26011EFD; // <-- Должен быть уникален для каждого устройства!

// Объект задачи для передачи данных по Lora
static osjob_t sendjob;

// Задание интервала передачи сообщений в секундах
const unsigned TX_INTERVAL = 3600 * 6;

// Объявление подключение ножек модуля LoRa и контроллера
const lmic_pinmap lmic_pins = {
  //  PINMAP FOR ARDUINO UNO
  //  .nss = 10,
  //  .rxtx = LMIC_UNUSED_PIN,
  //  .rst = 5,
  //  .dio = {/*dio0*/ 2, /*dio1*/ 3, LMIC_UNUSED_PIN},

  //  PINMAP FOR BSFRANCE BOARD
  .nss = 8,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 4,
  .dio = {/*dio0*/ 7, /*dio1*/ 5, LMIC_UNUSED_PIN},
};

/*================================
   Конец настройки RFM95
  ================================*/


/*=============================
   Обработка событий от RFM95
  ==============================*/
void onEvent (ev_t ev) {
  Serial.print(os_getTime());
  Serial.print(": ");
  switch (ev) {
    case EV_TXCOMPLETE:
      // Ждем данные от сервера сразу после отправки
      Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
      if (LMIC.txrxFlags & TXRX_ACK)
        Serial.println(F("Received ack"));
      if (LMIC.dataLen) {
        Serial.println(F("Received "));
        Serial.println(LMIC.dataLen);
        Serial.println(F(" bytes of payload"));
        for (int i = 0; i < LMIC.dataLen; i++) {
          if (LMIC.frame[LMIC.dataBeg + i] < 0x10) {
            Serial.print(F("0"));
          }
          Serial.print(LMIC.frame[LMIC.dataBeg + i], HEX);
          /***********************************************************************
             В этом месте можно будет попытаться вытащить данные полученные в ответ
             от сервера - downlink.
           * *********************************************************************/
        }
      }
      // Запланировать следующую передачу
      //      os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);

      os_setCallback(&sendjob, do_send);


      break;
    default:
      Serial.println(F("Unknown event"));
      break;
  }
}

/*=============================
   Функция отправки данных
  ==============================*/
void do_send(osjob_t* j) {
  // Проверить не идет ли прием/передача данных
  if (LMIC.opmode & OP_TXRXPEND) {
    Serial.println(F("OP_TXRXPEND, not sending"));
  } else {

    LMIC_setTxData2(1, rpiData, 23, 0);

    Serial.println(F("Packet queued"));
  }
  // Следующая передача планируется после события TX_COMPLETE
}


void setup() {
  pinMode(10, INPUT);
  pinMode(11, OUTPUT);
  rpiSer.begin(9600);

  Serial.begin(9600);
  while (!Serial.available());
  Serial.println(F("Starting"));

  Serial.println(F("Blink finished"));

//  Wire.begin();

  // Инициализация LMIC
  Serial.println("Initialize LMIC");
  os_init();

  // Reset the MAC state. Session and pending data transfers will be discarded.
  LMIC_reset();

  // On AVR, these values are stored in flash and only copied to RAM
  // once. Copy them to a temporary buffer here, LMIC_setSession will
  // copy them into a buffer of its own again.
  uint8_t appskey[sizeof(APPSKEY)];
  uint8_t nwkskey[sizeof(NWKSKEY)];
  memcpy_P(appskey, APPSKEY, sizeof(APPSKEY));
  memcpy_P(nwkskey, NWKSKEY, sizeof(NWKSKEY));
  LMIC_setSession (0x1, DEVADDR, nwkskey, appskey);

  // Set up the channels used by the Things Network, which corresponds
  // to the defaults of most gateways. Without this, only three base
  // channels from the LoRaWAN specification are used, which certainly
  // works, so it is good for debugging, but can overload those
  // frequencies, so be sure to configure the full frequency range of
  // your network here (unless your network autoconfigures them).
  // Setting up channels should happen after LMIC_setSession, as that
  // configures the minimal channel set.
  LMIC_setupChannel(0, 868100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(1, 868300000, DR_RANGE_MAP(DR_SF12, DR_SF7B), BAND_CENTI);      // g-band
  LMIC_setupChannel(2, 868500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(3, 867100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(4, 867300000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(5, 867500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(6, 867700000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(7, 867900000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(8, 868800000, DR_RANGE_MAP(DR_FSK,  DR_FSK),  BAND_MILLI);      // g2-band
  // TTN defines an additional channel at 869.525Mhz using SF9 for class B
  // devices' ping slots. LMIC does not have an easy way to define set this
  // frequency and support for class B is spotty and untested, so this
  // frequency is not configured here.


  // Disable link check validation
  LMIC_setLinkCheckMode(0);

  // TTN uses SF9 for its RX2 window.
  LMIC.dn2Dr = DR_SF9;

  // Set data rate and transmit power for uplink (note: txpow seems to be ignored by the library)
  LMIC_setDrTxpow(DR_SF7, 14);

  // Start job
  //  Serial.println("Initiale send");
  do_send(&sendjob);
}

void loop() {
  os_runloop_once();
  
  if (rpiSer.available() > 0) {
    rpiData[index] = rpiSer.read();
    Serial.println(rpiData[index]);
    index++;
  } else {
    if (index != 0) {
      Serial.println("Here i am");
      LMIC_setTxData2(1, rpiData, 23, 0);
      index = 0;
      os_setCallback(&sendjob, do_send);
    }
  }
}
