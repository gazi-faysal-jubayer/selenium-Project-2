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

# Find the <ul> element
ul_element = driver.find_element(By.XPATH, "//ul[@class='main_listing_provider list']")

# Find all <li> elements under the <ul>
li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

for li_element in li_elements:
    provider_data = {}
    
    title = li_element.find_element(By.XPATH, './/b[@class="company_name"]')
    provider_data['Title'] = title.text
    
    div_element = li_element.find_element(By.CLASS_NAME, 'list_cont_box')    
    stitle = div_element.find_elements(By.TAG_NAME, 'p')[0]
    provider_data['Subtitle'] = stitle.text
    
    cs = div_element.find_elements(By.TAG_NAME, 'p')[1]
    city = cs.text.split(',')[0]
    provider_data['City'] = city
    
    street = cs.text.split(', ')[1]
    provider_data['Street'] = street
    
    providers_data.append(provider_data)

# Print the collected data
for provider in providers_data:
    print(provider)

# Close the browser window
driver.quit()
