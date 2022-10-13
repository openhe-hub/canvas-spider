import ocr
import spider

username = 'hezhewen'
password = '5f6e778dx'
captcha_path = "../res/captcha.png"


class CanvasUtils(object):
    def __init__(self):
        self.spider = spider.CanvasSpider()

    def login(self):
        status = 0
        cnt = 0
        while status == 0 and cnt <= 5:
            cnt = cnt + 1
            self.spider.get_captcha(captcha_path)
            captcha = ocr.decaptcha(captcha_path)
            status = self.spider.login(captcha, username, password)
        return status

    def get_all_courses(self):
        self.spider.get_all_courses()
