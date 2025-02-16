"""This script gets the settings for each side of the bed and
    sets the sleep number for each side to the setting"""

from authentication import (
    get_authorization_login,
    get_authorization_token,
)

from sleep_iq_api import (
    get_bed_status,
    get_sleep_number_settings,
    get_sleepers,
    set_to_sleep_number,
    Side,
)

auth_login = get_authorization_login()
auth_token = get_authorization_token()


def print_bed_details():
    """Print bed details"""

    sleepers = get_sleepers(auth_token)

    for sleeper in sleepers:
        print(sleeper)

        sleep_number_settings = get_sleep_number_settings(
            auth_login, sleeper.bed_id, sleeper.side
        )
        print(sleep_number_settings)
        print()


def refill_to_sleep_number():
    """Sets each side to sleep number"""

    sleepers = get_sleepers(auth_token)

    for sleeper in sleepers:
        sleep_number_settings = get_sleep_number_settings(
            auth_login, sleeper.bed_id, sleeper.side
        )
        set_to_sleep_number(
            auth_login, sleeper.bed_id, sleeper.side, sleep_number_settings.sleep_number
        )


bed_status = get_bed_status(auth_login)

right_settings = get_sleep_number_settings(auth_login, bed_status.bed_id, Side.RIGHT)
left_settings = get_sleep_number_settings(auth_login, bed_status.bed_id, Side.LEFT)

set_to_sleep_number(
    auth_login, bed_status.bed_id, Side.RIGHT, right_settings.sleep_number
)
set_to_sleep_number(
    auth_login, bed_status.bed_id, Side.LEFT, left_settings.sleep_number
)
