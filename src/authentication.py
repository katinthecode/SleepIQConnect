"""Get authentication"""

import json
import os
import requests

from dotenv import load_dotenv

from data import (
    AuthenticationLogin,
    AuthenticationToken,
)

load_dotenv()

api_url = os.getenv("URL")
token_url = os.getenv("TOKEN_URL")
client_id = os.getenv("CLIENT_ID")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


def get_authorization_token():
    """Get the authorization token from the SleepIQ API"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "ClientID": client_id,
        "Email": email,
        "Password": password,
    }

    response = requests.request(
        "POST",
        token_url,
        headers=headers,
        data=json.dumps(payload),
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    return AuthenticationToken(response.json())


def get_authorization_login():
    """Get the authorization login from the SleepIQ API"""

    login_endpoint = "/login"
    headers = {"Content-Type": "application/json"}
    payload = {"login": email, "password": password}

    response = requests.request(
        "PUT",
        f"{api_url}{login_endpoint}",
        headers=headers,
        data=json.dumps(payload),
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    return AuthenticationLogin(response.json(), response.cookies)
