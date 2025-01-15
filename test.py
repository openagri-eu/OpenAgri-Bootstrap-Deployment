import requests

# Configuration
GATEKEEPER_URL = 'http://127.0.0.1:8001'


# Function to log in and fetch an access token
def login_to_gatekeeper(username, password):
    url = f"{GATEKEEPER_URL}/api/login/"
    try:
        response = requests.post(
            url,
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        tokens = response.json()
        return tokens.get("access", "")
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        return ""


# Function to register a service
def register_service(token, service_data):
    url = f"{GATEKEEPER_URL}/api/register_service/"
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.post(url, json=service_data, headers=headers)
        if response.status_code == 201:
            print("Service created successfully.")
        elif response.status_code == 200:
            print("Service already exists. Updating the service with new data.")
            print("Service updated successfully.")
        else:
            print(f"Unexpected status code during service registration: {response.status_code}")
        return response.json()  # Return response for further processing if needed
    except requests.exceptions.RequestException as e:
        print(f"Error during service registration: {e}")
        return None


# Function to send a GET request to a service proxy
def fetch_service_data(token, service_url):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(service_url, headers=headers)
        response.raise_for_status()
        return response.json()  # Return response for further processing if needed
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching service data: {e}")
        return None


# Main logic
if __name__ == "__main__":
    print("Logging into the gatekeeper")
    token = login_to_gatekeeper("admin", "admin")

    if token:
        print("Successfully logged in.")

        # Service registration data
        service_data = {
            "base_url": "http://weathersrv:8003/",
            "service_name": "weather_data",
            "endpoint": "api/data/thi/",
            "methods": ["GET"],
            "params": "lat=12.0&lon=12.0",
            "comments": "Any comments about this service"
        }

        print("Registering the service...")
        registration_response = register_service(token, service_data)

        if registration_response:
            print(f"Registration response: {registration_response.get('message')}")
        else:
            print("Service registration failed.")

        # Service URL
        service_url = f"{GATEKEEPER_URL}/api/proxy/weather_data/api/data/thi/?lat=12.0&lon=12.0"

        print("Fetching service data...")
        service_response = fetch_service_data(token, service_url)

        if service_response:
            print("Service data fetched successfully:")
            print(service_response)
        else:
            print("Failed to fetch service data.")
    else:
        print("Login failed. Please check your credentials or server status.")
