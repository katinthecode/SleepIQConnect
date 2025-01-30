from dataclasses import dataclass

@dataclass
class Authentication:
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
        return f'Access Token: {self.access_token}\nID Token: {self.id_token}\nRefresh Token: {self.refresh_token}\nExpires In: {self.expires_in}'
        
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
        return f'Is Account Owner: {self.is_account_owner}\nActive: {self.active}\nUser Name: {self.user_name}\nFirst Name: {self.first_name}\nBed ID: {self.bed_id}\nSleeper ID: {self.sleeper_id}\nAccount ID: {self.account_id}\nLast Login: {self.last_login}\nSide: {self.side}'