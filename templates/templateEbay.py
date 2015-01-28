__author__ = 'dserejo'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run(kwargs):
    profile = webdriver.FirefoxProfile('C:\Users\dserejo\AppData\Roaming\Mozilla\Firefox\Profiles\lltds86z.default')
    browser= webdriver.Firefox(profile)
    buscar=kwargs['buscar'].replace(' ','%20')
    url = 'http://www.ebay.com/itm/Jackery-Giant-High-capacity-Premium-Aluminum-Portable-Charger-10400mAh-External-/121360771291?pt=LH_DefaultDomain_0&hash=item1c41aa68db'
    browser.get(url)
    for el in browser.find_elements_by_tag_name('script'):
        print el.get_attribute('innerHTML')
    resp = {'scrapParams':kwargs}
    return resp