#include "mbed.h"
#include "CRC16.h"
 
uint8_t     numbers[] = {10, 244, 20, 30}; // array of numbers [0-254]
CRC16       crc16;      // CRC16 instance
uint16_t    crc_calc;   // calculated CRC16
uint8_t     crc_lsb;    // LSB of calculated CRC16
uint8_t     crc_msb;    // MSB of calculated CRC16
 
int main(void) {
    crc_calc = crc16.calc((char*)numbers, sizeof(numbers)/sizeof(numbers[0]));
    crc_lsb = crc_calc & 0xff;
    crc_msb = (crc_calc >> 8) & 0xff;
    printf("CRC     = %d\r\n", crc_calc);       
    printf("CRC LSB = %d\r\n", crc_lsb);
    printf("CRC MSB = %d\r\n", crc_msb);   
       
    while(1) {}
}