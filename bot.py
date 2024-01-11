from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.achc.org/find-a-provider/")

open_dropdown = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='select2-provider_drop_box-container']")))
try:
    actions = ActionChains(driver)
    actions.move_to_element(open_dropdown[0]).perform()
except:
    pass

for i in range (24):
    open_dropdown = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='select2-provider_drop_box-container']")))
    try:
        actions = ActionChains(driver)
        actions.move_to_element(open_dropdown[0]).perform()
    except:
        pass
    open_dropdown = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='select2-provider_drop_box-container']")))
    sleep(5)
    open_dropdown[0].click()

    options = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='select2-provider_drop_box-results']/li")))
    options[i].click()


    WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='sb_loading' and @style='display: block;']")))
    WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='sb_loading' and @style='display: none;']")))

    next_page = True

    while next_page == True:
        items = driver.find_elements("xpath","//ul[@class='main_listing_provider list']/li")
        if len(items)==0:
            break
        for i in range(0,len(items)):
            no_item = items[i].find_elements("xpath",".//h3[@class='empty_message']")
            if not no_item:
                items = driver.find_elements("xpath","//ul[@class='main_listing_provider list']/li")
                item = items[i]

                d = dict()

                d['Title'] = item.find_element("xpath",".//b[@class='company_name']").text

                el = item.find_element("xpath",".//p[@class='view_more_eye']")
                driver.execute_script("arguments[0].click();", el)
                
                WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='sb_loading' and @style='display: block;']")))
                WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='sb_loading' and @style='display: none;']")))
                
                modal_validate = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//h3[text()='Accreditation Details']")))
                
                d['Services'] = driver.find_element("xpath","//b[text()='Service: ']/parent::p").text

                close_btn = driver.find_element("xpath","//button[@id='TB_closeWindowButton']")
                close_btn.click()

                print(d)
                sleep(2)
                print('-------')
        
        next_page_btn = driver.find_elements("xpath","//li[@class='active']/following::li[1]/a[@class='page']")
        if next_page_btn:
            driver.execute_script("arguments[0].click();", next_page_btn[0])
            sleep(5)