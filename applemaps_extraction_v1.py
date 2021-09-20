import pandas as pd
from joblib import Parallel, delayed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
# driver.get('https://duckduckgo.com/')
# sleep(30)
starttime = datetime.now()
inputfile = 'Arkansas_lat_long.xlsx'
inputdata = pd.read_excel(inputfile,sheet_name='Sheet1')
print(inputdata)
for index, row in inputdata.iterrows():
    lat = str(row['Latitude'])
    lng = str(row['Longitude'])
    z = 17
    google_url = 'https://www.google.com/maps/@' + str(lat) + ',' + str(lng) + ',' + str(z) + 'z'
    driver.get(google_url)
    sleep(10)
    try:
        element = driver.find_element_by_xpath('//*[@id="omnibox-container"]')
        driver.execute_script("arguments[0].remove();", element)
    except:
        pass
    try:
        element1 = driver.find_element_by_xpath('//*[@id="vasquette"]')
        driver.execute_script("arguments[0].remove();", element1)
    except:
        pass
    try:
        element2 = driver.find_element_by_css_selector(("div[class='appviewcard-strip']"))
        driver.execute_script("arguments[0].remove();", element2)
    except:
        pass
    try:
        element3 = driver.find_element_by_css_selector(("div[class='scenefooter-container']"))
        driver.execute_script("arguments[0].remove();", element3)
    except:
        pass
    outputfolder = 'D:\\Maps\\Arkansas\\'
    google_image = outputfolder + '('+lat + '' + lng + ')' + 'google_'
    apple_image = outputfolder + '('+lat + '' + lng + ')' + 'apple_'

    # searchbox_input = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    # searchbox_input.send_keys(lat +','+ lng)
    # searchbox_input.send_keys(Keys.ENTER)
    # sleep(5)
    driver.save_screenshot(google_image + 'image.png')

    # lat = 35.9113349027868
    # lng = -89.78080320632905
    applesearchurl = 'https://duckduckgo.com/?q='+ str(lat)+ '%2C'+ str(lng) + '&t=h_&ia=web&iaxm=maps'
    # 'https://duckduckgo.com/?q=40.745255%2C+-74.034775&t=h_&ia=web&iaxm=maps'
    # sleep(5)
    driver.get(applesearchurl)
    sleep(10)
    try:
        element3 = driver.find_element_by_css_selector(("div[class='map-control vertical--map__sidebar__toggle js-vertical-map-toggle vertical--map__sidebar--light']"))
        element3.click()
        sleep(1)
    except:
        pass
    # driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    # ids = driver.find_elements_by_tag_name('canvas')
    # for ii in ids:
    #     # print ii.tag_name
    #     print(ii.get_attribute('id'))

    # try:
    #     zoomout_element = driver.find_element_by_css_selector(("div[class='mk-controls-container']"))
    #     zoomout_element.click()
    #     zoomout_element.click()
    #     zoomout_element.click()
    #     zoomout_element.click()
    #     zoomout_element.click()
    # except:
    #     pass
    # apple_searchbox_input = driver.find_element_by_xpath('//*[@id="search_form_input_homepage"]')
    # apple_searchbox_input.send_keys('35.9113349027868,-89.78080320632905')
    # apple_searchbox_input.send_keys(Keys.ENTER)
    # sleep(5)
    driver.save_screenshot(apple_image + 'image.png')
endtime = datetime.now()
diff = endtime - starttime
print(diff.seconds)