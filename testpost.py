import requests
import json

url = "localhost:5000"

payload = json.dumps({
  "password": "apppassword",
  "appname": "testapp",
  "errorjson": {
    "code": 500,
    "errormsg": "example failure"
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
