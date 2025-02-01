import json
import os
import requests

from dotenv import load_dotenv

from data import Authentication_Token, Sleeper

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
        
    json_response = response.json()
    
    auth = Authentication_Token(json_response)
    
    return auth

def get_sleepers(auth):
    sleeper_endpoint = '/sleeper'
    sleepers = []
    
    payload = {}
    headers = {
        'Authorization': auth.access_token
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

if __name__ == '__main__':
    auth = get_authorization_token()
    sleepers = get_sleepers(auth)
    
    for sleeper in sleepers:
        print(str(sleeper))