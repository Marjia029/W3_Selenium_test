from selenium.webdriver.common.by import By

def test_image_alt_attribute(driver):
    images = driver.find_elements(By.TAG_NAME, "img")
    failed_images = []

    for img in images:
        alt = img.get_attribute("alt")
        if not alt:
            failed_images.append(img.get_attribute("src"))
    
    if failed_images:
        return False, f"Images missing alt attribute: {failed_images}"
    
    return True, "All images have alt attributes"
