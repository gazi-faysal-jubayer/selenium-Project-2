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
print(li)
    
option_to_select = 'Home Health'
dropdown.select_by_visible_text(option_to_select)

#wait untill load the spinner
WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))


# Find the <ul> element
ul_element = driver.find_element(By.XPATH, "//ul[@class='main_listing_provider list']")

# Find all <li> elements under the <ul>
li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

# print(len(li_elements))

for li_element in li_elements:
    title = li_element.find_element(By.XPATH, './/b[@class="company_name"]')
    Title.append(title.text)
    
    div_element = li_element.find_element(By.CLASS_NAME, 'list_cont_box')    
    stitle = div_element.find_elements(By.TAG_NAME, 'p')[0]
    Subtitle.append(stitle.text)
    
    cs = div_element.find_elements(By.TAG_NAME, 'p')[1]
    city = cs.text.split(',')[0]
    City.append(city)
    
    street = cs.text.split(', ')[1]
    Street.append(street)
    
    commen_opt_div = li_element.find_element(By.CLASS_NAME, 'commen_opt')
    time.sleep(2)
    # Check if the <div> is visible
    if commen_opt_div.is_displayed():
        # Hover over the <div class="commen_opt">
        ActionChains(driver).move_to_element(commen_opt_div).perform()

        # Wait for the "View" option to be visible
        view_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'view_more_eye'))
        )

        # Click on the "View" option
        view_option.click()
        
        commen_opt_div.send_keys(Keys.ENTER)
        
        print('ok')

    
    time.sleep(200)

print(Title)
print(Subtitle)
print(City)
print(Street)

# time.sleep(500)

# Close the browser window
driver.quit()