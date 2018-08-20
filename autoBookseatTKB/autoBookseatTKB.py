from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
with open('autoBookseatTKB-settings.json', 'r', encoding="utf-8") as fp:
    settings = json.load(fp)
with open('locationList.json', 'r', encoding="utf-8") as fp:
    location_list = json.load(fp)

import datetime
date = datetime.date.today() + datetime.timedelta(days=6) # select the newest date

driver = webdriver.Chrome()

driver.get("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index")

driver.find_element_by_id("id").clear()
driver.find_element_by_id("id").send_keys(settings['id'])
driver.find_element_by_id("pwd").clear()
driver.find_element_by_id("pwd").send_keys(settings['password'])

driver.find_element_by_id("logininputcode").click()
driver.find_element_by_id("logininputcode").clear()
LonginSecurityCode = driver.execute_script("return LonginSecurityCode;")
driver.find_element_by_id("logininputcode").send_keys(LonginSecurityCode)

driver.find_element_by_link_text(u"送出").click()

driver.find_element_by_id("class_selector").click()
Select(driver.find_element_by_id("class_selector")).select_by_index(settings['classIndex'])
driver.find_element_by_id("class_selector").click()

driver.find_element_by_id("userinputcode").click()
driver.find_element_by_id("userinputcode").clear()
SecurityCode = driver.execute_script("return SecurityCode;")
driver.find_element_by_id("userinputcode").send_keys(SecurityCode)

location_value = location_list[settings['location']]
wait = WebDriverWait(driver, 30)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value=%s]" % location_value)))
driver.find_element_by_id("branch_selector").click()
Select(driver.find_element_by_id("branch_selector")).select_by_value(location_value)
driver.find_element_by_id("branch_selector").click()

element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='%d-%02d-%02d']" % (date.year, date.month, date.day))))
driver.find_element_by_id("date_selector").click()
Select(driver.find_element_by_id("date_selector")).select_by_value(str(date))
driver.find_element_by_id("date_selector").click()

element = wait.until(EC.presence_of_element_located((By.ID, "session_time_div")))
driver.find_element_by_name("session_time").click()
for i in settings['session']:
    if driver.find_elements_by_xpath('//input[@value="%d"]' % i):
        driver.find_element_by_xpath('//input[@value="%d"]' % i).click()

driver.find_element_by_link_text(u"送出").click()
alert = driver.switch_to_alert()
alert.accept()