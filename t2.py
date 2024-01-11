from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

# Opening website
driver = webdriver.Chrome()
driver.get("https://www.achc.org/find-a-provider/")
driver.implicitly_wait(10)

providers_data = []

dropdown_locator = (By.ID, 'provider_drop_box') 
WebDriverWait(driver, 10).until(EC.presence_of_element_located(dropdown_locator))
dropdown = Select(driver.find_element(*dropdown_locator))
options = [option.text for option in dropdown.options]
li = []
for option in options:
    li.append(option)
li.pop(0)

option_to_select = 'Home Care'
dropdown.select_by_visible_text(option_to_select)

# Wait until the spinner disappears
WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

pages = set()

while True:
    try:
        # Find the active page number
        active_page_number = driver.find_element(By.CSS_SELECTOR, "li.active a.page").text
        print(active_page_number)
        pages.add(active_page_number)

        # Construct the XPath for the next page
        next_page_xpath = f"//a[normalize-space()='{int(active_page_number) + 1}']"

        # Check if the next page element exists
        next_page_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, next_page_xpath)))

        driver.execute_script("arguments[0].click();", next_page_element)

        # Wait until the spinner disappears
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

    except (TimeoutException, StaleElementReferenceException) as e:
        # print(f"Exception: {e}")
        # print(f"Element for page {int(active_page_number) + 1} not found. Exiting the loop.")
        break

    time.sleep(10)
