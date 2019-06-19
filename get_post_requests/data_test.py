import datetime

# datetime.datetime.now()

# print(datetime.datetime.now())


AnimalNumber = 'KZC154000000'
Date = datetime.datetime.now()
Weight = 300.5
ScalesModel = 'test_123'



data = {AnimalNumber, datetime.datetime.now(), Weight, ScalesModel} 
  
# # sending post request and saving response as response object 
# #r = requests.post(url = API_ENDPOINT, data = data) 
  
# # extracting response text  
# #pastebin_url = r.text 
print(data) 