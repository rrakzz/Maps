from datetime import datetime
import cv2
import warnings
import pandas as pd
import cv2
import numpy as np
import pandas as pd
from statistics import mean
import math 
import os
import image_similarity_measures
from image_similarity_measures.quality_metrics import ssim

Region = "India"
Screenshots_path = f"D:\\Maps\\{Region}\\"
Latitute_Longitude_file = f"{Region}_lat_long.xlsx"
Output_file = f"{Region}_Maps_image_analysis_output.xlsx"
map_poi_class_a = f"D:\\Maps\\Class_a\\"
map_poi_class_g = f"D:\\Maps\\Class_g\\"

width = 1780 #map surveyed in meters
height = 890 #map surveyed in meters
Apple_blue = [245, 225, 174]
Google_blue = [249, 192, 156]

lat_long = pd.read_excel(Latitute_Longitude_file)
lat = lat_long['Latitude'].values.tolist()
lon = lat_long['Longitude'].values.tolist()

def google_map_POI(PATH, lat, long):
    outpath = ''
    image = cv2.imread(PATH)
    cv2.waitKey(0)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,5)

    alpha = 1.5 # Contrast control (1.0-3.0)
    beta = 10 # Brightness control (0-100)

    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    thresh = cv2.adaptiveThreshold(adjusted,255,1,1,11,1)
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    thresh = cv2.dilate(thresh,None,iterations = 2)
    thresh = cv2.erode(thresh,None,iterations = 2)
    edged = cv2.Canny(thresh, 30, 100)
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.imshow('Canny Edges After Contouring', edged)
    # cv2.waitKey(0)
    count2 = 0
    count1 = 0
    nlat, nlong = [], []
    
#     Money = [122, 134, 203]
#     General = [128, 128, 128]
#     Food = [241, 151, 4]
#     Hall = [17, 178, 202]
#     Hospital = [239, 97, 86]
#     Hotel = [239, 96, 145]
#     Store = [81, 143, 244]
#     Park = [54, 167, 84]

    google_white = [255, 255, 255]
    google_orange = [147, 226, 253]
    
    LT, LB, RT, RB = [], [], [], []
    class_list = []
    on_road1 = []
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if area > 200 and area < 500:
            if perimeter > 73 and perimeter < 77:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.imwrite('temp0.jpg', image[y:y+h,x:x+w])
#                 pad = 5
#                 cv2.imwrite('temp0_1.jpg', image[y-pad:y+h+pad,x-pad:x+w+pad])
                
                cl_list = []
                score_list = []
                for class_file in os.listdir(map_poi_class_g):
                    score = compare_SSIM(map_poi_class_g+class_file,'temp0.jpg')
                    score_list.append(score)
                    cl_list.append(class_file.split('.')[0])
                count1 = count1+1
                class_list.append(cl_list[score_list.index(max(score_list))])
#                 print(cl_list[score_list.index(max(score_list))], max(score_list))

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)                
        if area > 200 and area < 500:
            if perimeter > 73 and perimeter < 77:
                cv2.drawContours(image, contour, -1, (0, 0, 255), 3)
                x, y = [], []
                for kp in contour:
                    x.append(kp[0][0])
                    y.append(kp[0][1])
                display_text =  str(count2) + '_' + class_list[count2]  
                cv2.putText(image, display_text, (mean(x)+10, mean(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1, cv2.LINE_AA)
#                 cv2.putText(image, str(count2), (mean(x)+10, mean(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1, cv2.LINE_AA)
                lat1, long1 = long_lat_perPixel(lat,long, mean(x), mean(y), 'google')
    
                x, y, w, h = cv2.boundingRect(contour)
                pady = 4
                pad = 10
                on_road = 0 
                try:
                    if list(image[y+h,x+pad]) == google_white or list(image[y+h,x+pad]) == google_orange:
                        #print(f'On road{count2}')
                        on_road = on_road+1
                    if list(image[y+h,x+w-pad]) == google_white or list(image[y+h,x+w-pad]) == google_orange:
                        #print(f'On road{count2}')  
                        on_road = on_road+1
                    if list(image[y+h+pady,x+pad]) == google_white or list(image[y+h+pady,x+pad]) == google_orange:
                        #print(f'On road{count2}') 
                        on_road = on_road+1
                    if list(image[y+h+pady,x+w-pad]) == google_white or list(image[y+h+pady,x+w-pad]) == google_orange:
                        #print(f'On road{count2}')     
                        on_road = on_road+1
                except Exception as e: print(e)
#                 if on_road == 4:
#                     cv2.rectangle(image,(x-4,y-4),(x+w+4,y+h+4),(0,0,255),2)
#                     cv2.putText(image, 'On road', (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                if on_road > 0 :
                    cv2.rectangle(image,(x-4,y-4),(x+w+4,y+h+4),(0,0,255),2)
                    cv2.putText(image, 'On road', (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                    on_road1.append(1)
                else:
                    on_road1.append(0)
                nlat.append(lat1)
                nlong.append(long1)
                LT.append(list(image[y+h,x+pad]))
                LB.append(list(image[y+h+pady,x+pad]))
                RT.append(list(image[y+h,x+w-pad]))
                RB.append(list(image[y+h+pady,x+w-pad]))              
                count2 = count2+1
                
    print("Number of Google POIs found = " + str(count2))        
#     cv2.imshow('Contours', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    cv2.imwrite(PATH+'.png', image)
    
    return count2, nlat, nlong, class_list, on_road1, LT, LB, RT, RB

  
def apple_map_POI(PATH, lat, long):
    image = cv2.imread(PATH)
    cv2.waitKey(0)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,5)
#     alpha = 1.5 # Contrast control (1.0-3.0)
#     beta = 0 # Brightness control (0-100)
#     adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,10)
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    thresh = cv2.dilate(thresh,None,iterations = 1)
    thresh = cv2.erode(thresh,None,iterations = 1)
    edged = cv2.Canny(thresh, 30, 100)
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     cv2.imshow('Canny Edges After Contouring', edged)
#     cv2.waitKey(0)
    count1 = 0
    count2 = 0
    nlat, nlong = [], []

    apple_yellow = [64, 226, 255]
    apple_orange = [221, 252, 252]
    apple_white = [255, 255, 255]
    
    LT, LB, RT, RB = [], [], [], []
    class_list = []
    on_road1 = []
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if area > 100 and area < 200:
            if perimeter > 40 and perimeter < 52:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.imwrite('temp0.jpg', image[y:y+h,x:x+w])                    
                    
                cl_list = []
                score_list = []
                for class_file in os.listdir(map_poi_class_a):
                    score = compare_SSIM(map_poi_class_a+class_file,'temp0.jpg')
                    score_list.append(score)
                    cl_list.append(class_file.split('.')[0])
                count1 = count1+1
                class_list.append(cl_list[score_list.index(max(score_list))])
                
#                 print(cl_list[score_list.index(max(score_list))], max(score_list))
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)                
        if area > 100 and area < 200:
            if perimeter > 40 and perimeter < 52:
                cv2.drawContours(image, contour, -1, (0, 0, 255), 3)
                x, y = [], []
                for kp in contour:
                    x.append(kp[0][0])
                    y.append(kp[0][1])
                display_text =  str(count2) + '_' + class_list[count2]  
                cv2.putText(image, display_text, (mean(x)+10, mean(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1, cv2.LINE_AA)
#                 cv2.putText(image, str(count2), (mean(x)+10, mean(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1, cv2.LINE_AA)
                lat1, long1 = long_lat_perPixel(lat,long, mean(x), mean(y), 'apple')
    
                x, y, w, h = cv2.boundingRect(contour)
                pad = 0
                on_road = 0
                try:
                    if list(image[y-pad,x-pad]) == apple_yellow or list(image[y-pad,x-pad]) == apple_orange or list(image[y-pad,x-pad]) == apple_white:
                        #print(f'On road{count2}')
                        on_road = on_road+1
                    if list(image[y+h+pad+1,x-pad]) == apple_yellow or list(image[y+h+pad+1,x-pad]) == apple_orange or list(image[y+h+pad+1,x-pad]) == apple_white:
                        #print(f'On road{count2}')  
                        on_road = on_road+1
                    if list(image[y-pad,x+w+pad+1]) == apple_yellow or list(image[y-pad,x+w+pad+1]) == apple_orange or list(image[y-pad,x+w+pad+1]) == apple_white:
                        #print(f'On road{count2}') 
                        on_road = on_road+1
                    if list(image[y+h+pad+1,x+w+pad+1]) == apple_yellow or list(image[y+h+pad+1,x+w+pad+1]) == apple_orange or list(image[y+h+pad+1,x+w+pad+1]) == apple_white:
                        #print(f'On road{count2}')     
                        on_road = on_road+1
                except Exception as e: print(e)
                
#                 if on_road == 4:
#                     cv2.rectangle(image,(x-4,y-4),(x+w+4,y+h+4),(0,0,255),2)
#                     cv2.putText(image, 'On road', (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
#                     on_road1.append(1)
#                 elif on_road < 4 and on_road > 0 :
#                     cv2.rectangle(image,(x-4,y-4),(x+w+4,y+h+4),(0,0,255),2)
#                     cv2.putText(image, 'Partially on road', (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
#                     on_road1.append(0.5)
#                 else:
#                     on_road1.append(0)  
                    
                if on_road > 0 :
                    cv2.rectangle(image,(x-4,y-4),(x+w+4,y+h+4),(0,0,255),2)
                    cv2.putText(image, 'On road', (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
                    on_road1.append(1)
                else:
                    on_road1.append(0)
                    
                nlat.append(lat1)
                nlong.append(long1)
                LT.append(list(image[y-pad,x-pad]))
                LB.append(list(image[y+h+pad+1,x-pad]))
                RT.append(list(image[y-pad,x+w+pad+1]))
                RB.append(list(image[y+h+pad+1,x+w+pad+1]))
                count2 = count2+1                
                
                
    print("Number of Apple POIs found = " + str(count2))        
#     cv2.imshow('Contours', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    cv2.imwrite(PATH+'.png', image)
    return  count2, nlat, nlong, class_list, on_road1, LT, LB, RT, RB

def long_lat_perPixel(lat,long, x, y, brand):
    width = 1780 #m
    height = 890 #m
    
    if brand == 'apple':
        kms = 0.94
    else:
        kms = 1.0
    
    
    MeterPerPixel = width * height / (in_img1.shape[0] * in_img1.shape[1])
    Lat_PerPixel = MeterPerPixel * 0.00001 / kms
    Lon_PerPixel = MeterPerPixel * 0.00001 /(kms*math.cos(lat))
    
    if in_img1.shape[0]/2 > y:
        new_lat = lat+(Lat_PerPixel * abs(in_img1.shape[0]/2 - y))
    else:
        new_lat = lat-(Lat_PerPixel * abs(in_img1.shape[0]/2 - y))

    if in_img1.shape[1]/2 > x:
        new_long = long-(abs(Lon_PerPixel) * abs(in_img1.shape[1]/2 - x))
    else:
        new_long = long+(abs(Lon_PerPixel) * abs(in_img1.shape[1]/2 - x))        
        
#     print( in_img1.shape[0]/2 , y, in_img1.shape[1]/2 , x, new_lat, new_long)
    return new_lat, new_long


def Area_sqm(value):
    MeterPerPixel = width * height / (in_img1.shape[0] * in_img1.shape[1])
    area_sqm = (MeterPerPixel * value) ** (0.5)
    return area_sqm  

def compare_SSIM(img1,img2):
#     print(img1,img2)
    in_img1 = cv2.imread(img1)
    in_img2 = cv2.imread(img2)

    img1_outputimage = 'D:\\Maps\\temp1.png'
    img2_outputimage = 'D:\\Maps\\temp2.png'

    temp1_image = cv2.resize(in_img1, (20, 27), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(img1_outputimage, temp1_image)

    temp2_image = cv2.resize(in_img2, (20, 27), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(img2_outputimage, temp2_image)

    out_ssim = ssim(temp1_image, temp2_image) # Structural Similar Index Measure (SSIM)
#     print('SSIM : ', out_ssim)
    return out_ssim

starttime = datetime.now()
print(starttime)

warnings.filterwarnings('ignore')      
blue_app1 = []
blue_goog1 = []
apple_POI = []
google_POI = []
lat1 = []
lon1 = []
class1 = []
for i in range(len(lat)):
  try:
    img1 = Screenshots_path + f'({lat[i]}{lon[i]})apple_image.png'
    img2 = Screenshots_path + f'({lat[i]}{lon[i]})google_image.png'
    print('-'*100)
    print('Checking....', i+1,'/', len(lat))
    print(img1)
    print(img2)
    in_img1 = cv2.imread(img1)
    in_img2 = cv2.imread(img2)
    
    blue_app = 0
    blue_goog = 0
    for y in range(in_img1.shape[0]):
        for x in range(in_img1.shape[1]):
            if in_img1[y,x][0] == Apple_blue[0]  and in_img1[y,x][1] == Apple_blue[1] and in_img1[y,x][2] == Apple_blue[2]:
                blue_app = blue_app + 1
    for y in range(in_img2.shape[0]):
        for x in range(in_img2.shape[1]):        
            if in_img2[y,x][0] == Google_blue[0] and in_img2[y,x][1] == Google_blue[1] and in_img2[y,x][2] == Google_blue[2]:
                blue_goog = blue_goog + 1
                
    print("Google Blue pixels: ", blue_goog)
    print("Apple Blue pixels: ", blue_app)
    
    gcount, gnlat, gnlong, gclass, groad, gLT, gLB, gRT, gRB = google_map_POI(img2, lat[i], lon[i])
    acount, anlat, anlong, aclass, aroad, aLT, aLB, aRT, aRB = apple_map_POI(img1, lat[i], lon[i])
    
    g_lat_lon = pd.DataFrame({'lat': gnlat,'long': gnlong, 
                              'Le_Top': gLT, 'Le_Bot': gLB, 'Ri_Top': gRT, 'Ri_Bot': gRB, 
                              'class': gclass, 'on_road':groad})
    g_lat_lon.to_csv(Screenshots_path + f'({lat[i]}{lon[i]})google_POI.csv')

    a_lat_lon = pd.DataFrame({'lat': anlat,'long': anlong,  
                              'Le_Top': aLT, 'Le_Bot': aLB, 'Ri_Top': aRT, 'Ri_Bot': aRB,
                              'class': aclass, 'on_road':aroad})
    a_lat_lon.to_csv(Screenshots_path + f'({lat[i]}{lon[i]})apple_POI.csv')
    
    lat1.append(lat[i])
    lon1.append(lon[i])
    blue_app1.append(blue_app)
    blue_goog1.append(blue_goog)  
    google_POI.append(gcount)
    apple_POI.append(acount)    
    
    
  except Exception as e: print(e)

results = pd.DataFrame({'Latitude': lat1, 'Longitude': lon1, 'apple_blue_px': blue_app1, 
                        'google_blue_px': blue_goog1, 'apple_POI': apple_POI, 
                        'google_POI': google_POI})
                        
results['Survey_area_sqm'] = width * height
results['apple_blue_sqm'] = results['apple_blue_px'].apply(Area_sqm)
results['google_blue_sqm'] = results['google_blue_px'].apply(Area_sqm)

results.to_excel(Output_file, index = False)


enditme = datetime.now()
print(enditme)    
diff = enditme -starttime
print("Time taken:", diff, 'seconds')
