from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(headless=False):
    # Create Chrome options
    chrome_options = Options()
    
    # Add common arguments to improve WebDriver performance
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Set headless mode if specified
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
    
    # WebDriver Manager will automatically manage the ChromeDriver installation
    service = Service(ChromeDriverManager().install())
    
    # Create and return the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver