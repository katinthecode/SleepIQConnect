"""This script gets the settings for each side of the bed and
    sets the sleep number for each side to the setting"""

from sleep_iq_api import (
    get_authorization_login,
    get_bed_status,
    get_sleep_number_settings,
)
from sleep_iq_api import set_to_sleep_number, Side

auth_login = get_authorization_login()

bed_status = get_bed_status(auth_login)

right_settings = get_sleep_number_settings(auth_login, bed_status.bed_id, Side.RIGHT)
left_settings = get_sleep_number_settings(auth_login, bed_status.bed_id, Side.LEFT)

set_to_sleep_number(
    auth_login, bed_status.bed_id, Side.RIGHT, right_settings.sleep_number
)
set_to_sleep_number(
    auth_login, bed_status.bed_id, Side.LEFT, left_settings.sleep_number
)
