import json
import requests

gatekeeper_url = 'http://127.0.0.1:8001'

url = f"{gatekeeper_url}/api/login/"

# User credentials in test database
response = requests.post(
    url,
    json={
        "username": "admin",
        "password": "admin"
    },
    headers={"Content-Type": "application/json"}
)

token = ''

if response.status_code == 200:
    # Extract tokens from the JSON response
    tokens = response.json()
    token = tokens.get("access")
    print(token)

# # User credentials in test database
# data = {
#     "base_url": "http://farmcalendar:8002/",
#     "service_name": "farm_calendar",
#     "endpoint": "api/v1/Farm/",
#     "methods": ["GET", "POST"],
#     "version": "v1",
#     "params": "name={string}&status={integer}"
# }
#
# url = f"{gatekeeper_url}/api/register_service/"
#
# # Send POST request to get the token
# headers = {
#     'Authorization': f'Bearer {token}',
# }
#
# response = requests.post(url, json=data, headers=headers)

service_url = 'http://127.0.0.1:8001/api/proxy/weather_data/api/data/thi/?lat=12.0&lon=12.0'
# service_url = 'http://127.0.0.1:8003/api/data/thi/?lat=12.0&lon=12.0'

headers = {
    'Authorization': f'Bearer {token}',
}

request_kwargs = {
    'headers': headers
}

response = requests.get(service_url, **request_kwargs)

print(response.text)

# print(f"Response Status Code: {response.status_code}\n\n")
# print(f"Response Content: {json.dumps(response.json(), indent=4)}\n\n")
