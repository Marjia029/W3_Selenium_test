import json
from selenium.webdriver.support.ui import WebDriverWait

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

        # Prepare comments with scraped data
        comments = json.dumps({
            "SiteURL": site_url,
            "CampaignID": campaign_id,
            "SiteName": site_name,
            "Browser": browser,
            "CountryCode": country_code,
            "IP": ip
        }, indent=2)
        
        return True, comments
    
    except Exception as e:
        return False, f"Error scraping ScriptData: {str(e)}"