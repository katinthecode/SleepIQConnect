import json
import os
import requests

from dotenv import load_dotenv

from data import Authentication_Login, Authentication_Token, Responsive_Air_Settings, Sleeper

load_dotenv()

def get_authorization_token():
    payload = { 
            'ClientID': os.getenv('CLIENT_ID'), 
            'Email': os.getenv('EMAIL'), 
            'Password': os.getenv('PASSWORD') 
            }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request('POST', os.getenv('TOKEN_URL'), headers=headers, data=json.dumps(payload))

    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
    
    return Authentication_Token(response.json())

def get_authorization_login():
    login_endpoint = '/login'
    payload = {
        'login': os.getenv('EMAIL'),
        'password': os.getenv('PASSWORD')
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request('PUT', f'{os.getenv('URL')}{login_endpoint}', headers=headers, data=json.dumps(payload))
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    return Authentication_Login(response.json(), response.cookies)

def get_sleepers(auth_token):
    sleeper_endpoint = '/sleeper'
    sleepers = []
    
    payload = {}
    headers = {
        'Authorization': auth_token.access_token
    }
    
    response = requests.request('GET', f'{os.getenv('URL')}{sleeper_endpoint}', headers=headers, data=json.dumps(payload))

    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    json_response = response.json()
    
    for item in json_response['sleepers']:
        sleeper = Sleeper(item)
        sleepers.append(sleeper)
        
    return sleepers

def get_responsive_air_data(auth_login: Authentication_Login, bed_id: str):
    responsive_air_endpoint = f'/bed/{bed_id}/responsiveAir?_k={auth_login.key}'
    payload = {}
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request('GET', f'{os.getenv('URL')}{responsive_air_endpoint}', 
                                headers=headers, data=payload, cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    return Responsive_Air_Settings(response.json())

def set_responsive_air_data(auth_login: Authentication_Login, bed_id: str):
    responsive_air_endpoint = f'/bed/{bed_id}/responsiveAir?_k={auth_login.key}'
    payload = {
        'EnabledAuto': 'enabled'
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    response = requests.request('PUT', f'{os.getenv('URL')}{responsive_air_endpoint}', 
                                headers=headers, data=json.dumps(payload), cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    print(response.text)

if __name__ == '__main__':
    auth_token = get_authorization_token()
    sleepers = get_sleepers(auth_token)
    auth_login = get_authorization_login()
    set_responsive_air_data(auth_login, sleepers[0].bed_id)
    