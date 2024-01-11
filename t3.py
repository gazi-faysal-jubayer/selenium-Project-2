from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Opening website
driver = webdriver.Chrome()
driver.get("https://www.achc.org/find-a-provider/")
driver.implicitly_wait(10)

dropdown_locator = (By.ID, 'provider_drop_box') 
WebDriverWait(driver, 10).until(EC.presence_of_element_located(dropdown_locator))
dropdown = Select(driver.find_element(*dropdown_locator))

# Get all options in the dropdown
options = dropdown.options

for index, option in enumerate(options):
    # Skip the first option (index 0) since it's already selected
    if index == 0:
        continue

    # Print the name of the selected option
    print(f"Selected Option: {option.text}")

    # Select the option
    dropdown.select_by_index(index)

    # Wait until the spinner disappears
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

    # Additional actions if needed after selecting an option
    # ...

# Close the browser window
driver.quit()
