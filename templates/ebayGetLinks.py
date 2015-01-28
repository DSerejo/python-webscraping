__author__ = 'dserejo'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run(kwargs):
    resp = {'scrapParams':kwargs}
    resp['links2add']=[]
    #profile = webdriver.FirefoxProfile('C:\Users\dserejo\AppData\Roaming\Mozilla\Firefox\Profiles\lltds86z.default')
    #browser= webdriver.Firefox(profile)
    browser=webdriver.PhantomJS(executable_path='C:/phantomjs-1.9.8-windows/phantomjs.exe')
    url = kwargs['url']
    browser.get(url)

    for el in browser.find_elements_by_css_selector('.lvtitle a'):
        resp['links2add'].append({
            'url':el.get_attribute('href'),
            'templatePath':'templates.ebayProduct'
        })
    browser.close()
    return resp