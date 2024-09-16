
# !pip install ultralytics==8.0.196
# !pip install rasterio
# !pip install imagecodecs
# !pip install gdal
import imageio
from PIL import Image
import os
HOME = os.getcwd()

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()
from ultralytics import YOLO

from IPython.display import display, Image
import numpy as np

import rasterio as rio
import cv2
# from osgeo import ogr, osr, gdal
# !conda install -c conda-forge gdal -y
model = YOLO(f"path to model") #if want model file mail me 
village_name = "Village name" 
village_code = "Village code" 

from osgeo import gdal,osr

# Define the directory to save the Excel file
excel = 'path' 
resultimg= 'path' 
# Check if the directory exists, if not, create it
if not os.path.exists(excel):
    os.makedirs(excel)
    
if not os.path.exists(resultimg):
    os.makedirs(resultimg)

def coordsgenrate(name,coords):

    # with rio.open(f'{HOME}/shape71cropped.tif') as img:
    with rio.open(f'{name}.tif') as img:
        arr = img.read()  # read as numpy array
        coord = img.profile
    a, b, xoff, d, e, yoff, f, g, h = coord['transform']
    # ds = gdal.Open(f'{HOME}/shape71cropped.tif')
    ds = gdal.Open(f'{name}.tif')

    def pixel2coord(x, y):
        """Returns global coordinates from coordinates x,y of the pixel"""
        #if kl is mirrored or rotated change the positions of variable a, b, d, e
        xp = b * x + a * y + xoff
        yp = e * x + d * y + yoff
        return xp, yp

    old_cs = osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())
    wgs84_wkt = """
        GEOGCS["WGS 84",
            DATUM["WGS_1984",
                SPHEROID["WGS 84",6378137,298.257223563,
                    AUTHORITY["EPSG","7030"]],
                AUTHORITY["EPSG","6326"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.01745329251994328,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs.ImportFromWkt(wgs84_wkt)

    transform = osr.CoordinateTransformation(old_cs, new_cs)
    finalcood = []

    for polygon_list in coords:
      perfarm=[]
      for polygon in polygon_list:
        if len(polygon) > 0:
          for point in polygon:
            row, col = point[0], point[1]
            x, y = pixel2coord(col, row)
            lonx, latx, _ = transform.TransformPoint(x, y)
            newcood = [lonx, latx]
            perfarm.append(newcood)
      finalcood.append(perfarm)
    # print(finalcood)
    return finalcood

total_Coords=[]
for h in range(horizontal):
    for v in range (vertical):
        
        name=f'filename_{int(h)+1}-{int(v)+1}' 
        print(name)
        source = (f'{name}.jpg')
        im = cv2.imread(f'{name}.jpg')
        x,y,z=im.shape
        results = model(source, conf=0.5, imgsz=(y,x))
        
        from PIL import Image 
        for r in results:

            im_array = r.plot(labels=False, boxes=False)
            im_array_rgb = im_array[..., ::-1]
            im = Image.fromarray(im_array_rgb)
            im.save(f'/path{h+1}_{v+1}.jpg') 


        import numpy as np

        all_mask_coordinates = []
        
        for r in results[0]:
            mask_coordinates = r.masks.xy
            all_mask_coordinates.append(mask_coordinates)

        coords = all_mask_coordinates
        finalcood=coordsgenrate(name,coords)

        import pandas as pd

        # Create an empty list to store all polygon coordinates
        all_coords = []
        
        # Iterate over each polygon and store its coordinates
        for i, polygon in enumerate(finalcood):
            # Convert the list of coordinates to a string
            coords_str = ', '.join([f'({coord[0]}, {coord[1]})' for coord in polygon])
            # Append the polygon and its coordinates to the list
            all_coords.append(['Polygon {}'.format(i+1), coords_str])
            total_Coords.append([f'Polygon_{h+1}_{v+1}_{i+1}', coords_str, village_name, village_code])
            
        # Create a DataFrame from the list of all coordinates
        df = pd.DataFrame(all_coords, columns=['Polygon', 'Coordinates'])

        # Save the DataFrame to an Excel file
        df.to_excel(f'/path{h+1}_{v+1}.xlsx', index=False) 

df = pd.DataFrame(total_Coords, columns=['Polygon', 'Coordinates', 'Village Name', 'Village Code'])

# Save the DataFrame to an Excel file
df.to_excel(f'path/coordinates_final.xlsx', index=False) 
# print(len(total_Coords))

