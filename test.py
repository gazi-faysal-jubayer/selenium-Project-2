from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


#Opening website
driver = webdriver.Chrome()
driver.get("https://www.achc.org/find-a-provider/")
driver.implicitly_wait(10)

Title, Subtitle, Street, City, State, Zip, Date, Program, Service = [], [], [], [], [], [], [], [], []


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

#wait untill load the spinner
WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))


# Find the <ul> element
ul_element = driver.find_element(By.XPATH, "//ul[@class='main_listing_provider list']")

# Find all <li> elements under the <ul>
li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

print(li_elements)

# for i in range(len(li_elements)):
# for li_element in li_elements:
li_element = li_elements[0]
x = li_element.find_element(By.CLASS_NAME,"company_name")
driver.execute_script("arguments[0].scrollIntoView(true);", x)
time.sleep(20)
ActionChains(driver).move_to_element(x).perform()
time.sleep(20)
driver.find_element(By.XPATH,"//p[@class='view_more_eye']/i").click()
time.sleep(20)
driver.find_element(By.CLASS_NAME, "tb-close-icon").click()
time.sleep(20)
print('ok')

