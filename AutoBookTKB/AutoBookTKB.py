# !/usr/bin/python
# -*-coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoBookTKB:

    def __init__(self, settings):
        import json
        with open(settings, 'r', encoding="utf-8") as fp:
            self.settings = json.load(fp)
        with open('locationList.json', 'r', encoding="utf-8") as fp:
            self.location_list = json.load(fp)
        fp.close()

        self.driver = webdriver.Chrome()
        self.driver.get("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index")

        self.wait = WebDriverWait(self.driver, 60)

    def login(self):
        element = self.driver.find_element_by_id("id")
        element.clear()
        element.send_keys(self.settings['id'])

        element = self.driver.find_element_by_id("pwd")
        element.clear()
        element.send_keys(self.settings['password'])

        element = self.driver.find_element_by_id("logininputcode")
        element.click()
        element.clear()
        code = self.driver.execute_script("return LonginSecurityCode;")
        element.send_keys(code)

        self.click_send()

    def click_send(self):
        element = self.driver.find_element_by_link_text(u"送出")
        element.click()

    def wait_until_noon_or_midnight(self):
        import datetime, time
        midnight = datetime.datetime.replace(
            datetime.datetime.now() + datetime.timedelta(days=1), 
            hour=0, minute=0, second=0)
        
        noon = datetime.datetime.now().replace(hour=12, minute=0, second=0)
        
        now = datetime.datetime.now()

        delta = noon - now
        if delta.days < 0: # It's afternoon now, wait until midnight.
            delta = midnight - now

        print("Current time : " + time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Sleep for " + str(delta.seconds) + " seconds..."
            "do not close this window and the web driver.")
        time.sleep(delta.seconds)

    def refresh(self):
        """Refresh current page."""
        self.driver.refresh()

    def select_class(self):
        element = self.driver.find_element_by_id("class_selector")
        element.click()
        Select(element).select_by_index(self.settings['classIndex'])
        element.click()

    def send_securitycode(self):
        element = self.driver.find_element_by_id("userinputcode")
        element.click()
        element.clear()
        code = self.driver.execute_script("return SecurityCode;")
        element.send_keys(code)

    def select_location(self):
        location_value = self.location_list[self.settings['location']]
        element = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "option[value=%s]" % location_value
            ))
        )
        element = self.driver.find_element_by_id("branch_selector")
        element.click()
        Select(element).select_by_value(location_value)
        element.click()

    def select_date(self):
        """Select the newest date."""
        import datetime
        date = datetime.date.today() + datetime.timedelta(days=6)

        element = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "option[value='%d-%02d-%02d']" % (date.year, date.month, 
                                                  date.day)
            ))
        )
        element = self.driver.find_element_by_id("date_selector")
        element.click()
        Select(element).select_by_value(str(date))
        element.click()

    def select_sessions(self):
        element = self.wait.until(
            EC.presence_of_element_located((By.ID, "session_time_div"))
        )
        element = self.driver.find_element_by_name("session_time")
        for i in self.settings['sessions']:
            if self.driver.find_elements_by_xpath('//input[@value="%d"]' % i):
                self.driver.find_element_by_xpath('//input[@value="%d"]' % i).click()

    def accept_alerts(self):
        """Keep accepting alerts until there's a result."""
        while self.wait.until(EC.alert_is_present()):
            if self.accept_one_alert():
                break

    def accept_one_alert(self):
        alert = self.driver.switch_to_alert()        
        print('**' + alert.text + '**')

        mylist = [u'已滿', u'請勾選場次時間', u'預約成功', u'請選擇', u'異常']
        for s in mylist:
            if s in alert.text:
                return True

        alert.accept()

    def main(self):
        print("Mission started...")
        self.login()

        self.wait_until_noon_or_midnight()
        self.refresh()

        self.select_class()
        self.send_securitycode()
        self.select_location()
        self.select_date()
        self.select_sessions()
        self.click_send()
        self.accept_alerts()
        print("Task completed. Plese check your booking:)")


if __name__ == '__main__':
    atb = AutoBookTKB('AutoBookTKB-settings.json')
    atb.main()
    
