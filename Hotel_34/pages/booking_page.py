from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils.date_utils import select_random_dates, is_date_available
import time

class BookingPage:
    ACCEPT_COOKIES_BUTTON = (By.XPATH, "//div[@id='klaro-cookie-notice']//button[text()='אישור']")
    CHECKIN_MONTH = (By.CSS_SELECTOR, ".sb-checkin.month")
    CHECKOUT_MONTH = (By.CSS_SELECTOR, ".sb-checkout.month")
    CHECK_AVAILABILITY_BUTTON = (By.CSS_SELECTOR, ".sb-do-search-cmd")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".sb-room-container.closed")
    ROOM_NAME = (By.CSS_SELECTOR, ".sb-room-card__name")
    ROOM_PRICE = (By.CSS_SELECTOR, ".sb-room-card__price .sale-price-big")
    ROOM_AMENITIES = (By.CSS_SELECTOR, ".sb-icon-amenities")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def accept_cookies(self):
        self.wait.until(EC.element_to_be_clickable(self.ACCEPT_COOKIES_BUTTON)).click()

    def select_random_dates(self):
        return select_random_dates(self.driver)

    def select_dates(self, check_in, check_out):
        self._select_date(check_in, True)
        self._select_date(check_out, False)

    def _select_date(self, date, is_checkin):
        selector = self.CHECKIN_MONTH if is_checkin else self.CHECKOUT_MONTH
        month_select = Select(self.driver.find_element(*selector))
        month_select.select_by_value(f"{date.month},{date.year}")

        time.sleep(1)

        day_elements = self.driver.find_elements(By.CSS_SELECTOR, ".rg-day")
        for day_element in day_elements:
            day_header = day_element.find_element(By.CSS_SELECTOR, ".rg-day-header")
            if day_header.text == str(date.day):
                day_element.click()
                break

        if is_checkin:
            self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_MONTH))

    def click_check_availability(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECK_AVAILABILITY_BUTTON)).click()

    def get_search_results(self):
        time.sleep(3)
        results = self.wait.until(EC.presence_of_all_elements_located(self.SEARCH_RESULTS))
        return [self._extract_room_info(result) for result in results]

    def _extract_room_info(self, result):
        room_name = result.find_element(*self.ROOM_NAME).text.strip()
        price = result.find_element(*self.ROOM_PRICE).text.strip()
        amenities = ", ".join([amenity.get_attribute("title") for amenity in result.find_elements(*self.ROOM_AMENITIES)])
        return {"Room Name": room_name, "Price": price, "Amenities": amenities}