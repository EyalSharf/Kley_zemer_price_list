from selenium.webdriver.common.by import By
import time
class HomePage:
    URL = "https://hotelh34.com/"
    ORDER_BUTTON = (By.PARTIAL_LINK_TEXT, "הזמינו עכשיו")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def click_order_button(self):
        self.driver.find_element(*self.ORDER_BUTTON).click()
        time.sleep(2)  # Add a delay to give time for the new window to open
        # Ensure there are at least two windows open before switching
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
        else:
            raise Exception("New window not opened.")