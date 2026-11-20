import requests 
URL=("http://127.0.0.1:8001")
user_credential={"username":"ty","user_type":"dispatcher","password":"7852"}

packages={
  "name": "python",
  "destination": "japan",
  "weight": 2,
  "arrival_date": "2026-11-22",
  "status": "dispatched"
}

# response = requests.post(url=URL+"/register",json=user_credential)
# print(response.json())

response=requests.post(url=URL+"/login",json=user_credential)
response_json=response.json()
access_token=response_json["access_token"]
refresh_token=response_json["refresh_token"]

# print(access_token)

header={"token":access_token}

response=requests.get(url=URL+"/package/6",headers=header)
print(response.json())

response=requests.post(url=URL+"/registerpackage",json=packages,headers=header)
print(response.json())

