from datetime import datetime, timedelta
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def wait_for_calendar(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sb-checkin.month"))
    )

def is_date_available(driver, date):
    month_select = Select(driver.find_element(By.CSS_SELECTOR, ".sb-checkin.month"))
    month_select.select_by_value(f"{date.month},{date.year}")

    time.sleep(1)

    day_elements = driver.find_elements(By.CSS_SELECTOR, ".rg-day")
    for day_element in day_elements:
        day_header = day_element.find_element(By.CSS_SELECTOR, ".rg-day-header")
        if day_header.text == str(date.day):
            return "no-availability" not in day_element.get_attribute("class")
    return False

def select_random_dates(driver):
    wait_for_calendar(driver)
    today = datetime.now()
    max_date = today + timedelta(days=365)

    attempts = 0
    max_attempts = 50

    while attempts < max_attempts:
        check_in = today + timedelta(days=random.randint(1, 365))
        check_out = check_in + timedelta(days=7)

        if check_out <= max_date and is_date_available(driver, check_in) and is_date_available(driver, check_out):
            return check_in, check_out

        attempts += 1

    raise Exception("Unable to find available dates after multiple attempts")