from dataclasses import dataclass
from requests.cookies import RequestsCookieJar

@dataclass
class Authentication_Token:
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    
    def __init__(self, json):
        self.access_token = json['data']['AccessToken']
        self.id_token = json['data']['IdToken']
        self.refresh_token = json['data']['RefreshToken']
        self.expires_in = json['data']['ExpiresIn']
        
    def __str__(self):
        return f'''Access Token: {self.access_token}
                    ID Token: {self.id_token}
                    Refresh Token: {self.refresh_token}
                    Expires In: {self.expires_in}'''

@dataclass
class Authentication_Login:
    user_id: str
    key: str
    registration_state: int
    edp_login_status: int
    edp_login_message: str
    cookies: RequestsCookieJar
    
    def __init__(self, json, cookies):
        self.user_id = json['userId']
        self.key = json['key']
        self.registration_state = json['registrationState']
        self.edp_login_status = json['edpLoginStatus']
        self.edp_login_message = json['edpLoginMessage']
        self.cookies = cookies
        
    def __str__(self):
        return f'''User ID: {self.user_id}\nKey: {self.key}
                    Registration State: {self.registration_state}
                    EDP Login Status: {self.edp_login_status}
                    EDP Login Message: {self.edp_login_message}
                    Cookies: {self.cookies}'''
        
@dataclass
class Sleeper:
    is_account_owner: bool
    active: bool
    user_name: str
    first_name: str
    bed_id: str
    sleeper_id: str
    account_id: str
    last_login: str
    side: int
    
    def __init__(self, json):
        self.is_account_owner = json['isAccountOwner']
        self.active = json['active']
        self.user_name = json['username']
        self.first_name = json['firstName']
        self.bed_id = json['bedId']
        self.sleeper_id = json['sleeperId']
        self.account_id = json['accountId']
        self.last_login = json['lastLogin']
        self.side = json['side']
        
    def __str__(self):
        return f'''Is Account Owner: {self.is_account_owner}
                    Active: {self.active}
                    User Name: {self.user_name}
                    First Name: {self.first_name}
                    Bed ID: {self.bed_id}
                    Sleeper ID: {self.sleeper_id}
                    Account ID: {self.account_id}
                    Last Login: {self.last_login}
                    Side: {self.side}'''
                    
@dataclass
class Responsive_Air_Settings:
    adjustment_threshold: int
    in_bed_timeout: int
    left_side_enabled: bool
    right_side_enabled: bool
    out_of_bed_timeout: int
    poll_frequency: int
    pref_sync_state: str

    def __init__(self, json):
        self.adjustment_threshold = json['adjustmentThreshold']
        self.in_bed_timeout = json['inBedTimeout']
        self.left_side_enabled = json['leftSideEnabled']
        self.right_side_enabled = json['rightSideEnabled']
        self.out_of_bed_timeout = json['outOfBedTimeout']
        self.poll_frequency = json['pollFrequency']
        self.pref_sync_state = json['prefSyncState']
        
    def __str__(self):
        return f'''Adjustment Threshold: {self.adjustment_threshold}
                    In Bed Timeout: {self.in_bed_timeout}
                    Left Side Enabled: {self.left_side_enabled}
                    Right Side Enabled: {self.right_side_enabled}
                    Out Of Bed Timeout: {self.out_of_bed_timeout}
                    Poll Frequency: {self.poll_frequency}
                    Pref Sync State: {self.pref_sync_state}'''