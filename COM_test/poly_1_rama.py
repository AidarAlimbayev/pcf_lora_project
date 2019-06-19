# import crcmod

# crc16 = crcmod.mkCrcFun(0x18408, rev=True, initCrc=0xffff, xorOut=0x0000)
# print hex(crc16("04ff21".decode("hex")))

#04 ff21 1995
pucY = [0x06, 0x00, 0x01, 0x04, 0xff]
ucX = 5
POLY = 0x8408



def uiCrc16Cal(pucY, ucX):
	uiCrcValue = 0xffff  
	for ucI in range(0, ucX):
		print "debug 1 1", hex(uiCrcValue)
		uiCrcValue = uiCrcValue ^ pucY[ucI]
		print "debug 1", hex(uiCrcValue)
		
		for ucJ in range(0, 8):
			print ucJ
			if uiCrcValue & 0x0001:
				uiCrcValue = (uiCrcValue >> 1) ^ POLY

			else:
				uiCrcValue = uiCrcValue >> 1
			print "debug 2", hex(uiCrcValue)



	print "what the fuck"
	print hex(uiCrcValue)
	return uiCrcValue


uiCrc16Cal(pucY, ucX)