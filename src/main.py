import utils
import spider
import ocr

if __name__ == '__main__':
    utils = utils.CanvasUtils()
    utils.login()
    utils.get_all_courses()
