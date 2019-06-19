input_string = "EVN"
  
# CONVERT string data to binary string data 
data = (''.join(format(ord(x), 'b') for x in input_string)) 
print (data) 