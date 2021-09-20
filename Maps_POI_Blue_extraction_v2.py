from datetime import datetime
import cv2
import warnings
import pandas as pd
import cv2
import numpy as np
import pandas as pd

Region = "LA"
Screenshots_path = f"D:\\Maps\\{Region}\\"
Latitute_Longitude_file = f"{Region}_lat_long.xlsx"
Output_file = f"{Region}_Maps_image_analysis_output.xlsx"

width = 1780 #map surveyed in meters
height = 890 #map surveyed in meters
Apple_blue = [245, 225, 174]
Google_blue = [249, 192, 156]

lat_long = pd.read_excel(Latitute_Longitude_file)
lat = lat_long['Latitude'].values.tolist()
lon = lat_long['Longitude'].values.tolist()
print(lon)
print(lat)

def google_map_POI(PATH):
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
    
    count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if area > 200 and area < 500:
            if perimeter > 73 and perimeter < 77:
                count = count+1
                cv2.drawContours(image, contour, -1, (0, 255, 0), 3)

    print("Number of Google POIs found = " + str(count))        
#     cv2.imshow('Contours', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     cv2.imwrite(PATH+'.png', image)
    
    return count

  
def apple_map_POI(PATH):
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
    count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if area > 100 and area < 200:
            if perimeter > 40 and perimeter < 52:
                count = count+1
                cv2.drawContours(image, contour, -1, (0, 255, 0), 3)

    print("Number of Apple POIs found = " + str(count))        
#     cv2.imshow('Contours', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     cv2.imwrite(PATH+'.png', image)
    return count
    
def Area_sqm(value):
    MeterPerPixel = width * height / (in_img1.shape[0] * in_img1.shape[1])
    area_sqm = (MeterPerPixel * value) ** (0.5)
    return area_sqm  
    
starttime = datetime.now()
print(starttime)

warnings.filterwarnings('ignore')      
blue_app1 = []
blue_goog1 = []
apple_POI = []
google_POI = []
lat1 = []
lon1 = []
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
    lat1.append(lat[i])
    lon1.append(lon[i])
    blue_app1.append(blue_app)
    blue_goog1.append(blue_goog)  
    google_POI.append(google_map_POI(img2))
    apple_POI.append(apple_map_POI(img1))    
  except:
    pass
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