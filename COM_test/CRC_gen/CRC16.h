/*
 * This is a fork of the CRC16 library COPYRIGHT(c) Emilie Laverge
 * published at [https://developer.mbed.org/users/EmLa/code/CRC16/]
 * using the polynomial 0x8005: X^16 + X^15 + X^2 + 1.
 * Default initial CRC value = 0x0000
 *
 * Modified by Zoltan Hudak
 */
 
#ifndef CRC16_H
#define CRC16_H
 
class   CRC16
{
private:
    static const unsigned int   SHIFTER;
    static const unsigned short TABLE[];
public:
    CRC16(void){};
    ~CRC16(void){};
    unsigned short calc(char input[], int length, unsigned short crc = 0x0000);
};
#endif // CRC16_H