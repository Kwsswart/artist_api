from app.scraper.headers.platforms import *
from app.scraper.headers.headers import *
from app.scraper.headers.browsers import *


class Headers:
    '''
    browser - str, chrome/firefox/opera. User Agent browser. Default: random\n
    os - str, win/mac/lin. OS of User Agent. Default: random\n
    headers - bool, True/False. Generate random headers or no. Default: False
    '''

    __os = {
        'win': windows,
        'mac': macos,
        'lin': linux
    }

    __browser = {
        'chrome': chrome,
        'firefox': firefox,
        'opera': opera
    }

    def __init__(self, browser: str = None, os: str = None,
                 headers: bool = False, referer: str = None):
        self.__platform = self.__os.get(os, random_os)
        self.__browser = self.__browser.get(browser, random_browser)
        self.__headers = make_header if headers else self.empty
        self.__referer = referer
    # TODO: edit in order to allow for full customization of headers and post to PyPi as first library
    def empty(self, arg) -> dict:
        return {}

    def generate(self) -> dict:
        platform = self.__platform()
        browser = self.__browser()

        headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': browser.replace('%PLAT%', platform)
        }

        if self.__headers:
            headers.update(self.__headers(self.__referer))
        else:
            headers.update(self.__headers)

        return headers
