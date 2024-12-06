from selenium.webdriver.common.by import By

def test_html_tag_sequence(driver):
    heading_tags = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6")
    heading_levels = [int(tag.tag_name[1]) for tag in heading_tags]
    
    for i in range(len(heading_levels) - 1):
        if heading_levels[i] > heading_levels[i + 1]:
            return False, "HTML tag sequence broken"
    return True, "HTML tag sequence is correct"
