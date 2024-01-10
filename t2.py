from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
# print(li)

option_to_select = 'Home Health'
dropdown.select_by_visible_text(option_to_select)

# Wait until the spinner disappears
WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

page_no = 0



while True:
    page_no = driver.find_element(By.CSS_SELECTOR, "li[class='active'] a[class='page']").text
    print(page_no)
    driver.find_element(By.XPATH,"//div[@class='btn-next']").click
    if page_no == driver.find_element(By.CSS_SELECTOR, "li[class='active'] a[class='page']").text:
        break
    