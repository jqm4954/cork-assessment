import requests

# This file is strictly for testing purposes.
base = "http://127.0.0.1:5000"

response = requests.post(base+"/assets", json={"name":"device1", 
                                              "type":"laptop", 
                                              "serial_number":12345})
print(response.text)

# response = requests.get(base+"/assets")
# print(response.text)

# response = requests.delete(base+"/assets/2")
# print(response.text)

# response = requests.delete(base+"/assets/3")
# print(response.text)

response = requests.get(base+"/assets")
print(response.text)