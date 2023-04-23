from time import sleep 
from os import  getenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from typing import Dict 

from dotenv import load_dotenv
load_dotenv()

from utils import number_string_to_keypad_list, get_hour_and_minute, is_afternoon

payroll_xpath: str = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
last_name_xpath: str = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
first_name_xpath: str = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'

TIME_XPATHS = {
    "MONDAY_1": '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/input', 
}


first_time_xpath: str = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/input'

browser = webdriver.Safari()
browser.get(getenv("FORM"))
browser.set_window_position(0, 0)
browser.set_window_size(1024, 1560)


# Fill out basic information
browser.find_element(By.XPATH, payroll_xpath).send_keys(input("Which payroll number is this? "))
browser.find_element(By.XPATH, last_name_xpath).send_keys(getenv("LAST_NAME"))
browser.find_element(By.XPATH, first_name_xpath).send_keys(getenv("FIRST_NAME"))

time_sheet_data: Dict[int, str] = {
    0 : getenv("MONDAY_IN_1"),
    1 : getenv("MONDAY_OUT_1"),
    2 : getenv("TUESDAY_IN_1"),
    3 : getenv("TUESDAY_OUT_1"),
    4 : getenv("WEDNESDAY_IN_1"),
    5 : getenv("WEDNESDAY_OUT_1"),
    6 : getenv("THURSDAY_IN_1"),
    7 : getenv("THURSDAY_OUT_1"),
    8 : getenv("FRIDAY_IN_1"),
    9 : getenv("FRIDAY_OUT_1"),
    10: getenv("MONDAY_IN_2"),
    11: getenv("MONDAY_OUT_2"),
    12: getenv("TUESDAY_IN_2"),
    13: getenv("TUESDAY_OUT_2"),
    14: getenv("WEDNESDAY_IN_2"),
    15: getenv("WEDNESDAY_OUT_2"),
    16: getenv("THURSDAY_IN_2"),
    17: getenv("THURSDAY_OUT_2"),
    18: getenv("FRIDAY_IN_2"),
    19: getenv("FRIDAY_OUT_2"),
}


for x in range(20):
    number_of_tabs = x * 3 # each element is seperated by 3 tabs
    
    entry_data = time_sheet_data.get(x)
    
    if entry_data == "SAME":
        if x < 10:
            entry_data = time_sheet_data.get(x+10)
        else:
            entry_data = time_sheet_data.get(x-10)
        
        if entry_data =="SAME":
            print("There is an error with your env file")
            exit()
            
    if entry_data == "NONE":
        continue
    
    hour, minute = get_hour_and_minute(entry_data)
    
        
    first_hour_element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, first_time_xpath)))
    first_hour_element.click()
    
    # hour input 
    first_hour_element.send_keys([Keys.TAB] * number_of_tabs + number_string_to_keypad_list(str(hour)))
    # minute input
    first_hour_element.send_keys([Keys.TAB] * (number_of_tabs+1) + number_string_to_keypad_list(str(minute)))
    
    # select pm from dropdown
    if is_afternoon(hour):
        first_hour_element.send_keys([Keys.TAB] * (number_of_tabs+2), Keys.ENTER, Keys.ARROW_DOWN, Keys.ENTER)
        
    sleep(1)
    
    
first_hour_element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, first_time_xpath)))
first_hour_element.click()

if input("Are you sure all the information is correct? Press yes to submit").strip().lower() == "yes":
    first_hour_element.send_keys([Keys.TAB] * (20*3), Keys.ENTER, Keys.ARROW_DOWN, Keys.ENTER)
else:
    print("Edit your env file and try again")
    
sleep(3)
browser.close()