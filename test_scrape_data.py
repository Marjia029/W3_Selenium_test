import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver (with visible browser)
chrome_options = Options()
# Do not set --headless, so the browser will show up
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Visit the URL
url = "https://www.alojamiento.io/property/bonita-casa-de-campo-t%c3%adpica-mallorquina/BC-12224317"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Wait for 5 seconds to make sure content is loaded

# Automated testing: Try to collect ScriptData
try:
    # Access ScriptData from the window object
    script_data = driver.execute_script("return window.ScriptData;")
    
    if script_data:
        print("Successfully collected ScriptData:")
        # Debugging - print the entire script_data object to understand its structure
        #print(script_data)
        
        # Extract required fields
        site_url = script_data.get('config', {}).get('SiteUrl', 'N/A')
        campaign_id = script_data.get('pageData', {}).get('CampaignId', 'N/A')
        site_name = script_data.get('config', {}).get('SiteName', 'N/A')
        browser = script_data.get("userInfo", {}).get("Browser", "N/A")
        country_code = script_data.get("userInfo", {}).get("CountryCode", "N/A")
        ip = script_data.get("userInfo", {}).get("IP", "N/A")

        # Store the extracted data in a dictionary
        data = {
            "SiteURL": site_url,
            "CampaignID": campaign_id,
            "SiteName": site_name,
            "Browser": browser,
            "CountryCode": country_code,
            "IP": ip
        }

        print(data)
        
        # Save data to a pandas DataFrame
        df = pd.DataFrame([data])

        # Write DataFrame to an Excel file
        df.to_excel("scraped_data.xlsx", index=False)
        print("Data has been written to 'scraped_data.xlsx'")
    else:
        print("No ScriptData object found on the page.")
except Exception as e:
    print(f"An error occurred while collecting ScriptData: {e}")

# Close the browser
driver.quit()
