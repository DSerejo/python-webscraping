__author__ = 'dserejo'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def run(kwargs):
    profile = webdriver.FirefoxProfile('C:\Users\dserejo\AppData\Roaming\Mozilla\Firefox\Profiles\lltds86z.default')
    browser= webdriver.Firefox(profile)
    buscar=kwargs['buscar'].replace(' ','%20')
    url = 'http://busca.paodeacucar.com.br/search?p=Q&lbc=paodeacucar&uid=917484295&ts=custom&w='+buscar+'&isort=price&method=and&cnt=36&af=&view=list'

    browser.get(url)
    browser.implicitly_wait(20)
    try:
        a =  browser.find_elements_by_css_selector('.boxProduct .showcase-item__price');
        elements = browser.find_elements_by_css_selector('.boxProduct');
        for el in elements:
            print el.find_element_by_css_selector('.showcase-item__name').text,el.find_element_by_css_selector('.showcase-item__price').text
    except:
        print 'falhou'
    browser.close()
    resp = {'scrapParams':kwargs}
    return resp
