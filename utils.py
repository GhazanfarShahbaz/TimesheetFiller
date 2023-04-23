from selenium.webdriver.common.keys import Keys

from typing import List, Literal

NUM_TO_KEYPAD = {
    "0": Keys.NUMPAD0,
    "1": Keys.NUMPAD1,
    "2": Keys.NUMPAD2,
    "3": Keys.NUMPAD3,
    "4": Keys.NUMPAD4,
    "5": Keys.NUMPAD5,
    "6": Keys.NUMPAD6,
    "7": Keys.NUMPAD7,
    "8": Keys.NUMPAD8,
    "9": Keys.NUMPAD9
}


def number_string_to_keypad_list(num_string: str) -> List[Literal['']]:
    global NUM_TO_KEYPAD
    
    return [NUM_TO_KEYPAD[num] for num in num_string]


def get_hour_and_minute(time_string: str) -> List[str]:
    return time_string.split(":") 


def is_afternoon(hour: str) -> str:
    # if > 8 then we have am because, time sheets are up until 6pm
    return int(hour) < 8