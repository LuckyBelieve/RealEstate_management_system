import requests
import pandas as pd
from requests import request


def fetch_users():
    try:
        users_request = requests.get("http://127.0.0.1:8000/api/auth/all")
        users_request.raise_for_status()
        users = users_request.json()
        return (pd.DataFrame(users['users']))
    except requests.exceptions.RequestException as e:
        print(f"error fetching users data: {e}")
        return None

def fetch_estates():
    try:
        estates_request = requests.get("http://127.0.0.1:8000/api/estates/all")
        estates_request.raise_for_status()
        estates = estates_request.json()
        return (pd.DataFrame(estates['estates']))
    except requests.exceptions.RequestException as e:
        print(f"error fetching causes data: {e}")
        return None