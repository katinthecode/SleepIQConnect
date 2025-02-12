"""Data classes for the data from Sleep Number API"""

from dataclasses import dataclass
from enum import Enum
from requests.cookies import RequestsCookieJar


class Side(Enum):
    """Enum for the side of the bed."""

    RIGHT = "R"
    LEFT = "L"


@dataclass
class AuthenticationToken:
    """Data class for the authentication token"""

    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int

    def __init__(self, json):
        self.access_token = json["data"]["AccessToken"]
        self.id_token = json["data"]["IdToken"]
        self.refresh_token = json["data"]["RefreshToken"]
        self.expires_in = json["data"]["ExpiresIn"]

    def __str__(self):
        return f"""Access Token: {self.access_token}
                    ID Token: {self.id_token}
                    Refresh Token: {self.refresh_token}
                    Expires In: {self.expires_in}"""


@dataclass
class AuthenticationLogin:
    """Data class for the authentication login"""

    user_id: str
    key: str
    registration_state: int
    edp_login_status: int
    edp_login_message: str
    cookies: RequestsCookieJar

    def __init__(self, json, cookies):
        self.user_id = json["userId"]
        self.key = json["key"]
        self.registration_state = json["registrationState"]
        self.edp_login_status = json["edpLoginStatus"]
        self.edp_login_message = json["edpLoginMessage"]
        self.cookies = cookies

    def __str__(self):
        return f"""User ID: {self.user_id}\nKey: {self.key}
                    Registration State: {self.registration_state}
                    EDP Login Status: {self.edp_login_status}
                    EDP Login Message: {self.edp_login_message}
                    Cookies: {self.cookies}"""


@dataclass
class Sleeper:
    """Data class for sleeper"""

    is_account_owner: bool
    active: bool
    user_name: str
    first_name: str
    bed_id: str
    sleeper_id: str
    account_id: str
    last_login: str
    side_id: int
    side: Side

    def get_side_from_id(self):
        """Get the side of the bed from the side ID"""
        match self.side_id:
            case 0:
                return Side.RIGHT
            case 1:
                return Side.LEFT

    def __init__(self, json):
        self.is_account_owner = json["isAccountOwner"]
        self.active = json["active"]
        self.user_name = json["username"]
        self.first_name = json["firstName"]
        self.bed_id = json["bedId"]
        self.sleeper_id = json["sleeperId"]
        self.account_id = json["accountId"]
        self.last_login = json["lastLogin"]
        self.side_id = json["side"]
        self.side = self.get_side_from_id()

    def __str__(self):
        return f"""Is Account Owner: {self.is_account_owner}
                    Active: {self.active}
                    User Name: {self.user_name}
                    First Name: {self.first_name}
                    Bed ID: {self.bed_id}
                    Sleeper ID: {self.sleeper_id}
                    Account ID: {self.account_id}
                    Last Login: {self.last_login}
                    Side: {self.side}"""


@dataclass
class ResponsiveAirSettings:
    """Data class for responsive air settings"""

    adjustment_threshold: int
    in_bed_timeout: int
    left_side_enabled: bool
    right_side_enabled: bool
    out_of_bed_timeout: int
    poll_frequency: int
    pref_sync_state: str

    def __init__(self, json):
        self.adjustment_threshold = json["adjustmentThreshold"]
        self.in_bed_timeout = json["inBedTimeout"]
        self.left_side_enabled = json["leftSideEnabled"]
        self.right_side_enabled = json["rightSideEnabled"]
        self.out_of_bed_timeout = json["outOfBedTimeout"]
        self.poll_frequency = json["pollFrequency"]
        self.pref_sync_state = json["prefSyncState"]

    def __str__(self):
        return f"""Adjustment Threshold: {self.adjustment_threshold}
                    In Bed Timeout: {self.in_bed_timeout}
                    Left Side Enabled: {self.left_side_enabled}
                    Right Side Enabled: {self.right_side_enabled}
                    Out Of Bed Timeout: {self.out_of_bed_timeout}
                    Poll Frequency: {self.poll_frequency}
                    Pref Sync State: {self.pref_sync_state}"""


@dataclass
class SideData:
    """Data class for the side of the bed"""

    side: Side
    is_in_bed: bool
    alert_detailed_message: str
    sleep_number: int
    alert_id: int
    last_link: str
    pressure: int

    def __init__(self, side, json):
        self.side = Side(side)
        self.is_in_bed = json["isInBed"]
        self.alert_detailed_message = json["alertDetailedMessage"]
        self.sleep_number = json["sleepNumber"]
        self.alert_id = json["alertId"]
        self.last_link = json["lastLink"]
        self.pressure = json["pressure"]

    def __str__(self):
        return f"""Side: {self.side}
                    Is In Bed: {self.is_in_bed}
                    Alert Detailed Message: {self.alert_detailed_message}
                    Sleep Number: {self.sleep_number}
                    Alert ID: {self.alert_id}
                    Last Link: {self.last_link}
                    Pressure: {self.pressure}"""


@dataclass
class BedStatus:
    """Data class for the bed status"""

    status: int
    bed_id: str
    left_side: SideData
    right_side: SideData

    def __init__(self, json):
        self.status = json["status"]
        self.bed_id = json["bedId"]
        self.left_side = SideData(Side.LEFT, json["leftSide"])
        self.right_side = SideData(Side.RIGHT, json["rightSide"])

    def __str__(self):
        return f"""Status: {self.status}
                    Bed ID: {self.bed_id}
                    Left Side: 
                    {self.left_side}
                    Right Side: 
                    {self.right_side}"""


@dataclass
class SleepNumberSettings:
    """Data class for the sleep number settings"""

    sleep_number: int
    side: Side

    def __init__(self, json):
        self.sleep_number = json["sleepNumber"]
        self.side = Side(json["side"])

    def __str__(self):
        return f"""Sleep Number: {self.sleep_number}
                    Side: {self.side}"""
