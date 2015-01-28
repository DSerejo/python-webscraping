__author__ = 'dserejo'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.keys import Keys
def run(kwargs):
    resp = {'scrapParams':kwargs}
    resp['links2add']=[]
    #profile = webdriver.FirefoxProfile('C:\Users\dserejo\AppData\Roaming\Mozilla\Firefox\Profiles\lltds86z.default')
    profile = webdriver.FirefoxProfile('C:\Users\Denny\AppData\Roaming\Mozilla\Firefox\Profiles\\53v07vmv.default')
    browser= webdriver.Firefox(profile)
    #browser.set_window_size(300, 200)
    #browser.set_window_position(0, 200)
    #browser=webdriver.PhantomJS(executable_path='C:/phantomjs-1.9.8-windows/phantomjs.exe')

    url = kwargs['url']
    # browser.get('https://hide.me/en/proxy')
    # cy = browser.find_element_by_xpath('//*[@id="container"]/div[2]/div/div/form/fieldset/div[2]/div[1]/input')
    # browser.execute_script("arguments[0].value = 'us';", cy)
    # input=browser.find_element_by_xpath('//*[@id="u"]')
    # input.send_keys(url)
    # input.send_keys(Keys.RETURN)
    browser.get(url)

    #s = browser.find_element_by_css_selector('#JSDF script:nth-child(4)').get_attribute('innerHTML')
    resp['startprice']=price(browser)
    resp['category']=cat(browser)
    resp['quantity']=qty(browser)
    resp['title']=title(browser)
    resp['condition']=condition(browser)
    resp['description']=description(browser).replace("'","\\'")
    resp['productid']=pid(browser)
    resp['picurl']=picurl(browser)
    resp['link']=url
    #resp['paypalAccepted']=paypalAccepted(s)
    #binPrice
    # import re,json
    # p = re.compile("\$rwidgets\((.*)\)")
    # temp = p.search(s).group(1).split("])")[0][1:]
    # tempList=temp.split('],[')
    # matched={}
    # for el in tempList:
    #     el=el.replace("'",'"')
    #     try:
    #         e= json.loads("["+el+"]")
    #         matched.update({e[0]:e})
    #     except:
    #         print 'FALHOU!!',el

    #print resp
    browser.close()
    return resp

def price(browser):
    return browser.find_element_by_css_selector('#prcIsum').text
def cat(browser):
    list = browser.find_elements_by_css_selector('.bc-w a')
    return ' > '.join([el.text for el in list])
def condition(browser):
    return browser.find_element_by_css_selector('#vi-itm-cond').text
def qty(browser):
    return browser.find_element_by_css_selector('#qtySubTxt').text
#def paypalAccepted(s):
#    return s.split('isPaypalAccepted')[1].split(':')[1].split(',')[0]
def title(browser):
    return browser.find_element_by_css_selector('#itemTitle').text
def description(browser):
    return browser.find_element_by_css_selector('#x-main-ttrm-01').get_attribute('innerHTML')
def pid(browser):
    return browser.find_element_by_css_selector('.iti-act-num').text
def picurl(browser):
    return browser.find_element_by_css_selector('#icImg').get_attribute('src')

run({'url':'http://www.ebay.com/itm/Brother-QL-700-High-speed-Professional-Label-Printer-Free-Shipping-New-/121429087674?pt=LH_DefaultDomain_0&hash=item1c45bcd5ba'})