import re

def scrape_script_data(driver):
    script_data = driver.find_element_by_tag_name("script").get_attribute('innerHTML')
    # Example of how you might scrape this data, customize it as per site structure
    country_code = re.search(r'"countryCode":\s*"([^"]+)"', script_data)
    campaign_id = re.search(r'"campaignId":\s*"([^"]+)"', script_data)
    site_name = re.search(r'"siteName":\s*"([^"]+)"', script_data)
    ip = re.search(r'"ip":\s*"([^"]+)"', script_data)

    return {
        "country_code": country_code.group(1) if country_code else "Not Found",
        "campaign_id": campaign_id.group(1) if campaign_id else "Not Found",
        "site_name": site_name.group(1) if site_name else "Not Found",
        "ip": ip.group(1) if ip else "Not Found"
    }
