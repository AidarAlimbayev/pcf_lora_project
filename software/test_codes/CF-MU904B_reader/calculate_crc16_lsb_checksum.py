import crcmod

def calculate_crc16_lsb(data):
    crc16_func = crcmod.predefined.Crc('crc-16')
    crc16_func.update(data)
    crc16_result = crc16_func.crcValue
    return crc16_result.to_bytes(2, byteorder='little')

# Example usage:
data = b"00"
crc16_lsb_result = calculate_crc16_lsb(data)

print(f"CRC-16 LSB result for '{data.decode()}': {crc16_lsb_result.hex()}")
