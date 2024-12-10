import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook

def test_scrape_data(driver):
    """
    Test function to scrape script data from the webpage.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
    
    Returns:
        tuple: (bool, str) - Test result (pass/fail) and comments
    """
    try:
        # Wait for the page to load (maximum 10 seconds)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Access ScriptData from the window object
        script_data = driver.execute_script("return window.ScriptData;")
        
        if not script_data:
            return False, "No ScriptData object found on the page"
        
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

        # Save data to a pandas DataFrame
        df = pd.DataFrame([data])

        # Save data into a new sheet in test_report.xlsx
        report_path = "reports/test_report.xlsx"
        sheet_name = "ScriptData"

        # Check if the file exists
        try:
            with pd.ExcelWriter(report_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        except FileNotFoundError:
            # Create a new workbook if it doesn't exist
            with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Prepare comments with scraped data
        comments = "\n".join([f"{k}: {v}" for k, v in data.items()])
        
        return True, f"ScriptData successfully scraped and saved to {report_path} in sheet '{sheet_name}'\n{comments}"
    
    except Exception as e:
        return False, f"Error scraping ScriptData: {str(e)}"
