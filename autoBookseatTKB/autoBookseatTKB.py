from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoBookseatTKB:

    def __init__(self, settings):
        import json
        with open(settings, 'r', encoding="utf-8") as fp:
            self.settings = json.load(fp)
        with open('locationList.json', 'r', encoding="utf-8") as fp:
            self.location_list = json.load(fp)

        import datetime
        # select the newest date
        self.date = datetime.date.today() + datetime.timedelta(days=6)

        self.driver = webdriver.Chrome()
        self.driver.get("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index")

        self.wait = WebDriverWait(self.driver, 60)

    def login(self):
        self.driver.find_element_by_id("id").clear()
        self.driver.find_element_by_id("id").send_keys(self.settings['id'])

        self.driver.find_element_by_id("pwd").clear()
        self.driver.find_element_by_id("pwd").send_keys(self.settings['password'])

        self.driver.find_element_by_id("logininputcode").click()
        self.driver.find_element_by_id("logininputcode").clear()
        code = self.driver.execute_script("return LonginSecurityCode;")
        self.driver.find_element_by_id("logininputcode").send_keys(code)

        self.click_send()

    def click_send(self):
        self.driver.find_element_by_link_text(u"送出").click()

    def wait_until_tomorrow(self):
        """Wait until tommorow 00:00 am"""
        import datetime, time
        tomorrow = datetime.datetime.replace(
            datetime.datetime.now() + datetime.timedelta(days=1), 
            hour=0, minute=0, second=0)
        delta = tomorrow - datetime.datetime.now()
        print("Sleep for " + str(delta.seconds) + " seconds..."
            "do not close this window and the web driver.")
        time.sleep(delta.seconds)

    def refresh(self):
        """Refresh current page."""
        self.driver.refresh()

    def select_class(self):
        self.driver.find_element_by_id("class_selector").click()
        Select(self.driver.find_element_by_id("class_selector")).select_by_index(
            self.settings['classIndex'])
        self.driver.find_element_by_id("class_selector").click()

    def enter_securitycode(self):
        self.driver.find_element_by_id("userinputcode").click()
        self.driver.find_element_by_id("userinputcode").clear()
        code = self.driver.execute_script("return SecurityCode;")
        self.driver.find_element_by_id("userinputcode").send_keys(code)

    def select_location(self):
        location_value = self.location_list[self.settings['location']]
        element = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "option[value=%s]" % location_value)))
        self.driver.find_element_by_id("branch_selector").click()
        Select(self.driver.find_element_by_id("branch_selector")).select_by_value(location_value)
        self.driver.find_element_by_id("branch_selector").click()

    def select_date(self):
        element = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "option[value='%d-%02d-%02d']" % (self.date.year, 
                                              self.date.month, 
                                              self.date.day))))
        self.driver.find_element_by_id("date_selector").click()
        Select(self.driver.find_element_by_id("date_selector")).select_by_value(str(self.date))
        self.driver.find_element_by_id("date_selector").click()

    def select_sessions(self):
        element = self.wait.until(EC.presence_of_element_located((
            By.ID, "session_time_div")))
        self.driver.find_element_by_name("session_time").click()
        for i in self.settings['sessions']:
            if self.driver.find_elements_by_xpath('//input[@value="%d"]' % i):
                self.driver.find_element_by_xpath('//input[@value="%d"]' % i).click()

    def accept_alert(self):
        alert = self.driver.switch_to_alert()
        alert.accept()


if __name__ == '__main__':
    print("Mission started...")
    atb = AutoBookseatTKB('autoBookseatTKB-settings.json')
    atb.login()

    atb.wait_until_tomorrow()
    atb.refresh()

    atb.select_class()
    atb.enter_securitycode()
    atb.select_location()
    atb.select_date()
    atb.select_sessions()
    atb.click_send()
    atb.accept_alert()

    