from aip import AipOcr

APPID = '27892624'
API_KEY = '3amuDHsWiFhqmdUy3FjchwGO'
SECRET_KEY = 'ouBgYPlyaF6xxrnVfFNy540zfYguvOsg'

options = {"language_type": "CHN_ENG", "detect_direction": "true", "detect_language": "true", "probability": "true"}


def decaptcha(captcha_path):
    with open(captcha_path, 'rb') as file:
        client = AipOcr(APPID, API_KEY, SECRET_KEY)
        message = client.basicAccurate(file.read(), options)
    print(f'[info] OCR Message: msg={message}')
    code_text = message['words_result'][0]['words']
    code_text = code_text.replace(" ", "")
    print(f'[info] Decaptcha Finished: captcha={code_text}')
    return code_text
