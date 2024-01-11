from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import csv

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


# option_to_select = 'Home Health'
# dropdown.select_by_visible_text(option_to_select)

# print(li)

def sub():
    # Wait until the spinner disappears
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

    # Find the <ul> element
    ul_element = driver.find_element(By.XPATH, "//ul[@class='main_listing_provider list']")

    # Find all <li> elements under the <ul>
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

    for i in range(len(li_elements)):
        li_element = li_elements[i]
        provider_data = {}
        
        title = li_element.find_element(By.XPATH, './/b[@class="company_name"]')
        provider_data['Title'] = title.text
        
        div_element = li_element.find_element(By.CLASS_NAME, 'list_cont_box')    
        stitle = div_element.find_elements(By.TAG_NAME, 'p')[0]
        provider_data['Subtitle'] = stitle.text
        
        cs = div_element.find_elements(By.TAG_NAME, 'p')[1]
        city = cs.text.split(',')[0]
        provider_data['City'] = city
        
        street = cs.text.split(', ')[1].split(' ')[0]
        provider_data['Street'] = street
        
        zip = cs.text.split(', ')[1].split(' ')
        if len(zip)==2:
            provider_data['Zip'] = zip[1]
        else:
            provider_data['Zip'] = 'N/A'
        
        el = li_element.find_element("xpath",".//p[@class='view_more_eye']")
        driver.execute_script("arguments[0].click();", el)
        WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='sb_loading' and @style='display: block;']")))
        WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='sb_loading' and @style='display: none;']")))

        modal_validate = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//h3[text()='Accreditation Details']")))
        
        provider_data['Date'] = driver.find_element("xpath","//p[@class='start_end_date']").text.replace('Date: ', '')
        provider_data['Program'] = driver.find_element("xpath","//div[@id='TB_window']//p[2]").text.replace('Program: ', '')
        provider_data['Services'] = driver.find_element("xpath","//b[text()='Service: ']/parent::p").text.replace('Service: ', '')

        close_btn = driver.find_element("xpath","//button[@id='TB_closeWindowButton']")
        close_btn.click()
        
        providers_data.append(provider_data)
    

def main(option_to_select):
    dropdown.select_by_visible_text(option_to_select)
    # Wait until the spinner disappears
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

    # Find the <ul> element
    ul_element = driver.find_element(By.XPATH, "//ul[@class='main_listing_provider list']")

    # Find all <li> elements under the <ul>
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    if len(li_elements) == 0:
        return

    pages = []

    while True:
        try:
            # Find the active page number
            active_page_number = driver.find_element(By.CSS_SELECTOR, "li.active a.page").text
            if active_page_number in pages:
                break
            
            sub()
            pages.append(active_page_number)
            
            # # Find the <ul> element with class "pagination"
            # pagination_ul = driver.find_element(By.CLASS_NAME,"pagination")

            # # Find all <li> elements within the <ul> using XPath
            # li_elements = pagination_ul.find_elements(By.XPATH,".//li")
            # if len(li_elements)==1:
            #     break

            # # Construct the XPath for the next page
            next_page_xpath = "//div[@class='btn-next']"

            # # Check if the next page element exists
            next_page_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, next_page_xpath)))

            driver.execute_script("arguments[0].click();", next_page_element)

            # Wait until the spinner disappears
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

        except (TimeoutException, StaleElementReferenceException) as e:
            # print(f"Exception: {e}")
            # print(f"Element for page {int(active_page_number) + 1} not found. Exiting the loop.")
            break

        time.sleep(10)
        
x = 'Ambulatory Care'
main(x)

# for i in range(len(li)):
#     main(li[i])

# Print the collected data
for provider in providers_data:
    print(provider)
print(len(providers_data))

# Specify the CSV file path
csv_file_path = f'output-{x}.csv'

# Open the CSV file in write mode
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.DictWriter(csv_file, fieldnames=providers_data[0].keys())

    # Write the header
    csv_writer.writeheader()

    # Write the data rows
    csv_writer.writerows(providers_data)

print(f'CSV file "{csv_file_path}" has been created.')

# Close the browser window
driver.quit()
