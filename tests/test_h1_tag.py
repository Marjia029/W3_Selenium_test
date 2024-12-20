from selenium.webdriver.common.by import By

def test_h1_tag(driver):
    try:
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        if not h1_tags:
            return False, "Missing <h1> tag"
        return True, "H1 tag exists"
    except Exception as e:
        return False, f"Error: {e}"