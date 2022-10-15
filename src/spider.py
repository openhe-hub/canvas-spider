import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

import logger

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}

webdriver_path = "../lib/msedgedriver.exe"


class CanvasSpider(object):
    def __init__(self):
        self.driver = webdriver.Edge(webdriver_path)
        self.canvas_root_url = "https://www.jicanvas.com/"
        self.login_url = 'https://jicanvas.com/login/canvas'
        self.course_cnt = 0
        self.courses = []

    def get_captcha(self, captcha_path):
        # forward to login page
        self.driver.get(self.login_url)
        link_node = self.driver.find_elements(By.XPATH, '//*[@id="footer"]/a[2]')[0]
        login_url = link_node.get_attribute('href')
        self.driver.get(login_url)
        # get captcha
        img_node = self.driver.find_elements(By.ID, 'captcha-img')[0]
        left = int(img_node.location['x'])
        top = int(img_node.location['y'])
        right = int(img_node.location['x'] + img_node.size['width'])
        bottom = int(img_node.location['y'] + img_node.size['height'])
        # screenshot and crop, this way is to cross the anti-spider mechanism
        self.driver.get_screenshot_as_file(captcha_path)
        img = Image.open(captcha_path)
        img = img.crop((left + 950, top + 440, right + 1150, bottom + 465))
        img.save(captcha_path)

    def login(self, captcha, username, password):
        curr_url = self.driver.current_url
        WRONG_CAPTCHA_ERR = '&err=1'
        print(f'[info] visit {curr_url}')

        username_input = self.driver.find_elements(By.XPATH, '//*[@id="user"]')[0]
        password_input = self.driver.find_elements(By.XPATH, '//*[@id="pass"]')[0]
        captcha_input = self.driver.find_elements(By.XPATH, '//*[@id="captcha"]')[0]
        btn_node = self.driver.find_elements(By.XPATH, '//*[@id="submit-button"]')[0]

        username_input.send_keys(username)
        password_input.send_keys(password)
        captcha_input.send_keys(captcha)
        btn_node.click()

        status = 1 if self.driver.current_url != curr_url + WRONG_CAPTCHA_ERR else 0
        if status == 1:
            print(f'[success] visit {self.driver.current_url}')
        else:
            print(f'[error] decaptcha failed. trying again')

        return status

    def get_all_courses(self):
        courses_container = self.driver.find_elements(By.XPATH, '//*[@id="DashboardCard_Container"]/div/div/div')
        self.course_cnt = len(courses_container)
        logger.log_separation('Courses List')
        print(f'Total found {self.course_cnt} courses:')
        for i in range(0, len(courses_container)):
            self.courses.append(courses_container[i].get_attribute("aria-label"))
            print(f'\t[{i + 1}]{self.courses[i]}')
        logger.log_separation('Courses List')

    def get_all_announcements(self):
        for i in range(self.course_cnt):
            # get href
            course = self.driver.find_element(By.XPATH,
                                              f'//*[@id="DashboardCard_Container"]/div/div/div[{i + 1}]/div/a')
            course_url = course.get_attribute("href")
            # get announcements
            logger.log_separation(self.courses[i])
            self.driver.get(course_url + '/announcements')
            time.sleep(2)
            titles = self.driver.find_elements(By.XPATH, '//*[@class="fOyUs_bGBk blnAQ_bGBk blnAQ_dnfM blnAQ_drOs"]')
            print(f'[output]:total {len(titles)} announcements\n')
            for j in range(len(titles)):
                text = titles[j].text.replace(" ", "").split(",")
                status = "read" if len(text) == 1 else "unread"
                print(f'\t{text[-1]}')
            self.driver.back()
            logger.log_separation(self.courses[i])
