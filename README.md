# Machine Learning for Advanced Image Analysis - Research Major Project

## Project Overview
This code comprises of only part which is after the dataset is created and based on that dataset the model is tranined.Hence the code is of extraction of boundaries using model from image consisting of format"img" and "tiff".This code is written to work on big size region like a village. This project is focused on advanced image analysis using machine learning, particularly for processing satellite imagery to extract geographical coordinates of specific areas (e.g., agricultural fields). The process leverages the YOLO (You Only Look Once) model for image segmentation and classification and converts pixel coordinates into geographical coordinates for further analysis.

## Requirements
The project uses Python for scripting, with the following dependencies:

## Python Libraries:
#### Ultralytics (YOLO): A state-of-the-art object detection library.
#### Rasterio: For handling raster imagery.
#### GDAL (Geospatial Data Abstraction Library): For reading and processing geospatial data.
#### OpenCV: For image manipulation.
#### Pandas: For handling data in tabular form (Excel export).
#### Numpy: For array operations.
#### PIL (Python Imaging Library): For working with images.

### Installation:

To install the required libraries, run the following commands:
#### !pip install ultralytics==8.0.196
#### !pip install rasterio
#### !pip install imagecodecs
#### !pip install gdal
#### !conda install -c conda-forge gdal -y

### Steps in the Code

YOLO Model Loading: The project starts by loading the pre-trained YOLO model from a specified path:
#### model = YOLO('path to model')
#### village_name = "Village name"
#### village_code = "Village code"

Coordinate Generation: The function coordsgenrate() converts pixel coordinates of segmented areas into geographical coordinates (longitude, latitude). It reads the raster image file (GeoTIFF format), extracts the pixel coordinate transformation matrix, and applies the conversion to WGS84 geographic coordinates.

Segmentation and Image Processing: The YOLO model processes each image tile, detecting the desired objects (such as fields), saving the segmented output, and extracting mask coordinates.
#### results = model(source, conf=0.5, imgsz=(y,x))

Saving the Segmented Image: For each tile, the segmentation results are saved as an image file:
#### im.save(f'/path{h+1}_{v+1}.jpg')

Coordinate Extraction: The coordinates of the segmented masks are passed to the coordsgenrate() function, which converts them from pixel to geographical coordinates. This data is stored for further analysis.

Exporting Coordinates to Excel: The extracted coordinates for each tile are stored in an Excel file, with additional metadata such as village name and code:
#### df.to_excel(f'/path{h+1}_{v+1}.xlsx', index=False)

Final Excel File: All polygon coordinates from multiple tiles are consolidated and saved into a final Excel file:
#### df.to_excel(f'path/coordinates_final.xlsx', index=False)

## Project Structure
The project processes imagery in a grid fashion (horizontal and vertical tiling). Each image tile is passed through the YOLO model, segmented, and then analyzed to extract field boundary coordinates, which are saved in Excel for further usage in geospatial tools.

## Output

#### Segmented Images: Output images with detected regions.
Example image of region of a village:

![results_1_4](https://github.com/user-attachments/assets/28f4afae-4ae7-400c-8229-430bedf3c8cd)

![results_3_2](https://github.com/user-attachments/assets/40fa059a-95e7-48a6-8c20-029d5f5f4cf0)


#### Coordinates Excel File: An Excel file with the geographical coordinates of detected regions.

[coordinates_1_4.xlsx](https://github.com/user-attachments/files/17018806/coordinates_1_4.xlsx)


## Usage

Place the raster GeoTIFF files in the specified path.
Modify the script paths for your model, data, and output directories.
Run the script to extract and save field boundaries and their geographical coordinates.

## Contact
For model or dataset details, you can reach out to me.
