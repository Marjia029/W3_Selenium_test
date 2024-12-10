from utils.driver_setup import setup_driver
from utils.test_utils import run_test
from tests.test_h1_tag import test_h1_tag
from tests.test_html_tag_sequence import test_html_tag_sequence
from tests.test_image_alt_attribute import test_image_alt_attribute
from tests.test_url_status import test_url_status
from tests.test_currency_filter import test_currency_filter
from tests.test_scrape_data import test_scrape_data

if __name__ == "__main__":
    driver = setup_driver(headless=True)
    url = "https://www.alojamiento.io/property/bonita-casa-de-campo-t%c3%adpica-mallorquina/BC-12224317"

    # Run each test
    print("H1 test performing")
    run_test(driver, url, test_h1_tag, "H1 tag existence test")
    print("H1 test performed")

    print("HTML tag sequence test performing")
    run_test(driver, url, test_html_tag_sequence, "HTML tag sequence test")
    print("HTML tag sequence test perfomed")

    print("Image alt attribute test performing")
    run_test(driver, url, test_image_alt_attribute, "Image alt attribute test")
    print("Image alt attribute test performed")

    print("URL status code test performing")
    run_test(driver, url, test_url_status, "URL status code test")
    print("URL status code test performed")

    print("Currency filter test performing")
    run_test(driver, url, test_currency_filter, "Currency filter test")
    print("Currency filter test performed")
    
    print("Script data scrape test performing")
    run_test(driver, url, test_scrape_data, "Script data scrape test")
    print("Script data scrape test performed")

    driver.quit()
