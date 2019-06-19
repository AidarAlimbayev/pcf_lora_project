# importing the requests library 
import requests 
import datetime  


# defining the api-endpoint  
API_ENDPOINT = "http://87.247.28.238:8501/api/weights"
  
AnimalNumber = "KZC154000000"
Date = "2019-04-16T13:15:00"
Weight = "300.5"
ScalesModel = "ver_1_test"
  
# data to be sent to api 
data = {AnimalNumber, Date, Weight, ScalesModel} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
#pastebin_url = r.text 
print(data) 
