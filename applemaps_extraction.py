import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from PIL import Image
import os
import numpy as np
options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
starttime = datetime.now()
inputfile = 'India_lat_long.xlsx'
outputfolder = 'D:\\Maps\\India\\'
inputdata = pd.read_excel(inputfile,sheet_name='Sheet1')
result_df = []
outputfile = outputfolder + 'filtered_latlng.csv'
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

    google_image = outputfolder + '('+lat + '' + lng + ')' + 'google_'
    apple_image = outputfolder + '('+lat + '' + lng + ')' + 'apple_'
    driver.save_screenshot(google_image + 'image.png')

    applesearchurl = 'https://duckduckgo.com/?q='+ str(lat)+ '%2C'+ str(lng) + '&t=h_&ia=web&iaxm=maps'
    driver.get(applesearchurl)
    sleep(10)
    try:
        element3 = driver.find_element_by_css_selector(("div[class='map-control vertical--map__sidebar__toggle js-vertical-map-toggle vertical--map__sidebar--light']"))
        element3.click()
        sleep(1)
    except:
        pass
    driver.save_screenshot(apple_image + 'image.png')
    sleep(5)
    img = Image.open(apple_image + 'image.png')
    img = img.convert("RGB")

    co_ordinates = [(59, 13), (59, 19), (108,13), (108,19), (113, 13), (113, 19), (124,15)]
    flag = False
    for co_ordinate in co_ordinates:
        co_ordinate_tuple = img.getpixel(co_ordinate)
        if co_ordinate_tuple != (72, 69, 65):
            flag = True
            break

    print(flag)
    if flag == True:
        pass
        #os.remove(apple_image + 'image.png')
        #os.remove(google_image + 'image.png')
    else:
        temp = pd.DataFrame({'Latitude': lat, 'Longitude': lng}, index=[0])
        result_df.append(temp)
    # rgb_value1 = img.getpixel((59, 13))
    # print(rgb_value1)
    # rgb_value2 = img.getpixel((59, 19))
    # rgb_value3 = img.getpixel((108,13))
    # rgb_value4 = img.getpixel((108,19))
    # rgb_value5 = img.getpixel((113, 13))
    # rgb_value6 = img.getpixel((113, 19))
    # rgb_value7 = img.getpixel((124,15))
if len(result_df) > 0:
    result_df = pd.concat(result_df, ignore_index=True)
    result_df.insert(loc=0, column='S.No', value=np.arange(1, len(result_df) + 1))
    result_df.to_csv(outputfile, index=False)
driver.quit()
endtime = datetime.now()
diff = endtime - starttime
print(diff.seconds)