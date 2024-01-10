li_element = li_elements[0]
x = li_element.find_element(By.CLASS_NAME,"company_name")
ActionChains(driver).move_to_element(x).perform()
driver.find_element(By.XPATH,"//p[@class='view_more_eye']/i").click()
time.sleep(200)
driver.find_element(By.CLASS_NAME, "tb-close-icon").click()
time.sleep(200)
print('ok')