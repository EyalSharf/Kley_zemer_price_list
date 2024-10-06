import allure
import pytest
from pages.home_page import HomePage
from pages.booking_page import BookingPage
from utils.excel_utils import save_to_excel


def test_hotel_booking(driver):
    home_page = HomePage(driver)
    home_page.open()
    home_page.click_order_button()

    booking_page = BookingPage(driver)
    booking_page.accept_cookies()
    check_in, check_out = booking_page.select_random_dates()
    booking_page.select_dates(check_in, check_out)
    booking_page.click_check_availability()

    search_results = booking_page.get_search_results()

    assert len(search_results) > 0, "No search results found"

    save_to_excel(search_results, "rooms_list.xlsx")
    allure.attach(driver.get_screenshot_as_png(), name="Order Button Screenshot",
                  attachment_type=allure.attachment_type.PNG)

    for result in search_results:
        assert "Room Name" in result, "Room Name is missing from the result"
        assert "Price" in result, "Price is missing from the result"
        assert "Amenities" in result, "Amenities are missing from the result"