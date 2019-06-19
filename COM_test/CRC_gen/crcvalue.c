#define PRESET_VALUE 0xFFFF
#define POLYNOMIAL 0x8408



unsigned int uiCrc16Cal(unsigned char const * pucY, unsigned char ucX)
{
	unsigned char ucI, ucJ;
	unsigned short int uiCrcValue = PRESET_VALUE;

	for (ucI = 0; ucI < ucX; ucI++)
	{
		uiCrcValue = uiCrcValue^*(pucY + ucI);
		for(ucJ = 0; ucJ < 8; ucJ++)
		{
			if(uiCrcValue & 0x0001)
			{
				uiCrcValue = (uiCrcValue >> 1)^POLYNOMIAL;
			}
			else
			{
				uiCrcValue = (uiCrcValue >> 1);
			}
		}
	}
	return uiCrcValue;
}