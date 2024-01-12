import requests

def test_user_registration():
    url = "http://127.0.0.1/:5000/login/register"
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "company": "Doe Inc",
        "user_type_id": 1,
        "password": "securepassword123"
    }

    try:
        response = requests.post(url, json=user_data)
        if response.status_code == 201:
            print(f"Registration successful: {response.json()}")
        else:
            print(f"Registration failed: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def test_user_authentication():
    url = "http://127.0.0.1/:5000/login/authenticate"
    login_data = {
        "email": "johndoe@example.com",
        "password": "securepassword123"
    }

    try:
        response = requests.post(url, json=login_data)
        if response.status_code == 200:
            print(f"Authentication successful: {response.json()}")
        else:
            print(f"Authentication failed: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_user_registration()
    test_user_authentication()
