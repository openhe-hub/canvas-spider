from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}

canvas_url = 'https://jicanvas.com/login/canvas'

webdriver_path = "../lib/msedgedriver.exe"


class CanvasSpider(object):
    def __init__(self):
        self.driver = webdriver.Edge(webdriver_path)

    def get_captcha(self, captcha_path):
        # forward to login page
        self.driver.get(canvas_url)
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
        cnt = len(courses_container)
        print('[output]:\n' + '=' * 30 + 'Courses List' + '=' * 30)
        print(f'Total found {cnt} courses:')
        for i in range(0, len(courses_container)):
            print(f'\t[{i+1}]{courses_container[i].get_attribute("aria-label")}')
        print('=' * 30 + 'Courses List' + '=' * 30 + '\n')
