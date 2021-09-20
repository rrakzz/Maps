import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from PIL import Image
import os
import numpy as np

starttime = datetime.now()
Region = "LA"
inputfile = f'{Region}_lat_long.xlsx'
outputfolder = f'D:\\Maps\\{Region}\\'
result_df = []
outputfile = outputfolder + f'{Region}_lat_long_filtered.xlsx'
lat_long = pd.read_excel(inputfile)
lat = lat_long['Latitude'].values.tolist()
lon = lat_long['Longitude'].values.tolist()
for i in range(len(lat)):
    try:
        apple_image = outputfolder + f'({lat[i]}{lon[i]})apple_image.png'
        google_image = outputfolder + f'({lat[i]}{lon[i]})google_image.png'
        # sleep(5)
        print(apple_image)
        print(google_image)
        img = Image.open(apple_image)
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
            os.remove(apple_image)
            os.remove(google_image)
        else:
            temp = pd.DataFrame({'Latitude': str(lat[i]), 'Longitude': str(lon[i])}, index=[0])
            result_df.append(temp)
    except:
        continue
if len(result_df) > 0:
    result_df = pd.concat(result_df, ignore_index=True)
    result_df.insert(loc=0, column='S.No', value=np.arange(1, len(result_df) + 1))
    result_df.to_excel(outputfile, index=False)
# driver.quit()
endtime = datetime.now()
diff = endtime - starttime
print(diff.seconds)