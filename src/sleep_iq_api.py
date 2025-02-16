"""Connect to the SleepIQ API"""

import json
import os
import requests

from dotenv import load_dotenv

from data import (
    AuthenticationLogin,
    AuthenticationToken,
    BedStatus,
    ResponsiveAirSettings,
    Side,
    Sleeper,
    SleepNumberSettings,
)

load_dotenv()

api_url = os.getenv("URL")


def get_sleepers(auth_token: AuthenticationToken):
    """Get sleepers data from the SleepIQ API"""

    sleeper_endpoint = "/sleeper"
    sleepers = []

    headers = {"Authorization": auth_token.access_token}
    payload = {}

    response = requests.request(
        "GET",
        f"{api_url}{sleeper_endpoint}",
        headers=headers,
        data=json.dumps(payload),
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    json_response = response.json()

    for item in json_response["sleepers"]:
        sleeper = Sleeper(item)
        sleepers.append(sleeper)

    return sleepers


def get_bed_status(auth_login: AuthenticationLogin):
    """Get bed status data from the SleepIQ API"""

    bed_status_endpoint = f"/bed/familyStatus?_k={auth_login.key}"

    headers = {}
    payload = {}

    response = requests.request(
        "GET",
        f"{api_url}{bed_status_endpoint}",
        headers=headers,
        data=payload,
        cookies=auth_login.cookies,
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    return BedStatus(response.json()["beds"][0])


def get_responsive_air_data(auth_login: AuthenticationLogin, bed_id: str):
    """Get responsive air data from the SleepIQ API"""

    responsive_air_endpoint = f"/bed/{bed_id}/responsiveAir?_k={auth_login.key}"

    headers = {"Content-Type": "application/json"}
    payload = {}

    response = requests.request(
        "GET",
        f"{api_url}{responsive_air_endpoint}",
        headers=headers,
        data=payload,
        cookies=auth_login.cookies,
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    return ResponsiveAirSettings(response.json())


def enable_responsive_air(auth_login: AuthenticationLogin, bed_id: str):
    """Enables responsive air for the bed"""

    responsive_air_endpoint = f"/bed/{bed_id}/responsiveAir?_k={auth_login.key}"

    headers = {"Content-Type": "application/json"}
    payload = {"EnabledAuto": "enabled"}

    response = requests.request(
        "PUT",
        f"{api_url}{responsive_air_endpoint}",
        headers=headers,
        data=json.dumps(payload),
        cookies=auth_login.cookies,
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    return True


def set_pump_to_idle(auth_login: AuthenticationLogin, bed_id: str):
    """Sets the pump to idle"""

    pump_to_idle_endpoint = f"/bed/{bed_id}/pump/forceIdle?_k={auth_login.key}"

    headers = {}
    payload = {}

    response = requests.request(
        "PUT",
        f"{api_url}{pump_to_idle_endpoint}",
        headers=headers,
        data=payload,
        cookies=auth_login.cookies,
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    return True


def get_sleep_number_settings(auth_login: AuthenticationLogin, bed_id: str, side: Side):
    """Get sleep number settings from the SleepIQ API"""

    sleep_number_endpoint = (
        f"/bed/{bed_id}/sleepNumber?_k={auth_login.key}&side={side.value}"
    )

    headers = {}
    payload = {}

    response = requests.request(
        "GET",
        f"{api_url}{sleep_number_endpoint}",
        headers=headers,
        data=payload,
        cookies=auth_login.cookies,
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    return SleepNumberSettings(response.json())


def set_to_sleep_number(
    auth_login: AuthenticationLogin, bed_id: str, side: Side, sleep_number: int
):
    """Set the sleep number for the bed"""

    if set_pump_to_idle(auth_login, bed_id) is not True:
        print("Error setting pump to idle")
        exit()

    responsive_air_endpoint = f"/bed/{bed_id}/sleepNumber?_k={auth_login.key}"

    headers = {"Content-Type": "application/json"}
    payload = {"side": side.value, "sleepNumber": sleep_number}

    response = requests.request(
        "PUT",
        f"{api_url}{responsive_air_endpoint}",
        headers=headers,
        data=json.dumps(payload),
        cookies=auth_login.cookies,
        timeout=30,
    )

    if response.status_code < 200 or response.status_code >= 300:
        print("Error: " + str(response.status_code))
        print(response.text)
        exit()

    print("Sleep Number set to " + str(sleep_number))
    return True
