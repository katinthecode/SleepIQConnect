import json
import os
import requests

from dotenv import load_dotenv

from data import Authentication_Login, Authentication_Token, Bed_Status, Responsive_Air_Settings
from data import Side, Sleeper, Sleep_Number_Settings

load_dotenv()

def get_authorization_token():
    headers = {
        'Content-Type': 'application/json'
    }
    payload = { 
            'ClientID': os.getenv('CLIENT_ID'), 
            'Email': os.getenv('EMAIL'), 
            'Password': os.getenv('PASSWORD') 
            }

    response = requests.request('POST', os.getenv('TOKEN_URL'), headers=headers, data=json.dumps(payload))

    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
    
    return Authentication_Token(response.json())

def get_authorization_login():
    login_endpoint = '/login'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'login': os.getenv('EMAIL'),
        'password': os.getenv('PASSWORD')
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
    
    headers = {
        'Authorization': auth_token.access_token
    }
    payload = {}
    
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

def get_bed_status(auth_login: Authentication_Login):
    bed_status_endpoint = f'/bed/familyStatus?_k={auth_login.key}'
    
    headers = {}
    payload = {}
    
    response = requests.request('GET', f'{os.getenv('URL')}{bed_status_endpoint}', 
                                headers=headers, data=payload, cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
    
    return Bed_Status(response.json()['beds'][0])

def get_responsive_air_data(auth_login: Authentication_Login, bed_id: str):
    responsive_air_endpoint = f'/bed/{bed_id}/responsiveAir?_k={auth_login.key}'
    
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {}
    
    response = requests.request('GET', f'{os.getenv('URL')}{responsive_air_endpoint}', 
                                headers=headers, data=payload, cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    return Responsive_Air_Settings(response.json())

def enable_responsive_air(auth_login: Authentication_Login, bed_id: str):
    responsive_air_endpoint = f'/bed/{bed_id}/responsiveAir?_k={auth_login.key}'
    
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'EnabledAuto': 'enabled'
    }
    
    response = requests.request('PUT', f'{os.getenv('URL')}{responsive_air_endpoint}', 
                                headers=headers, data=json.dumps(payload), cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    return True

def set_pump_to_idle(auth_login: Authentication_Login, bed_id: str):
    pump_to_idle_endpoint = f'/bed/{bed_id}/pump/forceIdle?_k={auth_login.key}'
    
    headers = {}
    payload = {}
    
    response = requests.request('PUT', f'{os.getenv('URL')}{pump_to_idle_endpoint}', 
                                headers=headers, data=payload, cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    return True

def get_sleep_number_settings(auth_login: Authentication_Login, bed_id: str, side: Side):
    sleep_number_endpoint = f'/bed/{bed_id}/sleepNumber?_k={auth_login.key}&side={side.value}'
    
    headers = {}
    payload = {}
    
    response = requests.request('GET', f'{os.getenv('URL')}{sleep_number_endpoint}', 
                                headers=headers, data=payload, cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
        
    return Sleep_Number_Settings(response.json())
    
def set_to_sleep_number(auth_login: Authentication_Login, bed_id: str, side: Side, sleep_number: int):
    if set_pump_to_idle(auth_login, bed_id) != True:
        print('Error setting pump to idle')
        exit()
    
    responsive_air_endpoint = f'/bed/{bed_id}/sleepNumber?_k={auth_login.key}'
    
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'side': side.value,
        'sleepNumber': sleep_number
    }
    
    response = requests.request('PUT', f'{os.getenv('URL')}{responsive_air_endpoint}', 
                                headers=headers, data=json.dumps(payload), cookies=auth_login.cookies)
    
    if response.status_code < 200 or response.status_code >= 300:
        print('Error: ' + str(response.status_code))
        print(response.text)
        exit()
    
    print('Sleep Number set to ' + str(sleep_number))
    return True
    
def print_bed_details():
    auth_token = get_authorization_token()
    auth_login = get_authorization_login()
    
    sleepers = get_sleepers(auth_token)
        
    for sleeper in sleepers:
        print(sleeper)
        
        sleep_number_settings = get_sleep_number_settings(auth_login, sleeper.bed_id, sleeper.side)
        print(sleep_number_settings)
        print()
    
def refill_to_sleep_number():
    auth_token = get_authorization_token()
    auth_login = get_authorization_login()
    
    sleepers = get_sleepers(auth_token)
    
    for sleeper in sleepers:
        sleep_number_settings = get_sleep_number_settings(auth_login, sleeper.bed_id, sleeper.side)
        set_to_sleep_number(auth_login, sleeper.bed_id, sleeper.side, sleep_number_settings.sleep_number)