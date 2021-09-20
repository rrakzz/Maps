import numpy as np
import math
import pandas as pd

kmsPerDegree=111
scanWidthKms=0.89 #1366x769 pixel screen
scanHeightKms=1.78 #1366x769 pixel screen

content = pd.read_excel("apple_maps_input.xlsx", sheet_name= 'LA')

lat= content.loc[0].at["Latitude"]
long= content.loc[0].at["Longitude"]
areaSqkm= content.loc[0].at["Area"]
print(lat, long, areaSqkm)

longitudinalDistance=math.sqrt(areaSqkm)
latitudinalDistance=longitudinalDistance
horizontalCount= int(math.ceil(longitudinalDistance/scanWidthKms))
verticalCount= int (math.ceil(latitudinalDistance/scanHeightKms))
northWestCornerLat=lat+latitudinalDistance/kmsPerDegree/2
northWestCornerLong=long-longitudinalDistance/kmsPerDegree/2

longit_list = []
latit_list = []
for i in np.arange(horizontalCount):
    for j in np.arange(verticalCount):
        print ("Scan Area Center Longitude: {0:10.8f} ;  Scan Area Center Latitude: {1:10.8f}".format(northWestCornerLong + (j+1/2)*scanHeightKms/kmsPerDegree, northWestCornerLat - (i+1/2)*scanWidthKms/kmsPerDegree))
        longit_list.append(northWestCornerLong + (j+1/2)*scanHeightKms/kmsPerDegree)
        latit_list.append(northWestCornerLat - (i+1/2)*scanWidthKms/kmsPerDegree)
        
lat_long= pd.DataFrame({'Latitude': latit_list, 'Longitude':longit_list})
lat_long.to_excel('LA_lat_long.xlsx', index=False)        