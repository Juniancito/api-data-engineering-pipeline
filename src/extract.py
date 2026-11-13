import requests

def extract_users(api_url: str)-> list[dict]:

    response = requests.get(api_url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Expected a list of users from the API response.")

    return data