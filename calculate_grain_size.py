import cv2
import numpy as np
import os
from skimage import morphology, measure
import pandas as pd

data=pd.DataFrame(columns=['Specimen_name','image_name','Grain_size'])
conversion_factor=1

def calculate_grain_size(image_path,sub_filename):
    if "100X" in sub_filename:
        conversion_factor=1/1.22
    elif "200X" in sub_filename:
        conversion_factor=1/2.44
    elif "500X" in sub_filename:
        conversion_factor=1/6.1
    elif "1000X" in sub_filename:
        conversion_factor=1/12.2
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Otsu thresholding to convert to binary image
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Perform noise reduction by eliminating small regions
    cleaned = morphology.remove_small_objects(binary.astype(bool), min_size=500)

    # Perform morphological closing for grain division
    closed = morphology.binary_closing(cleaned)

    # Find contours of grains
    contours, _ = cv2.findContours(closed.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate equivalent diameter of each grain and store in a list
    equivalent_diameters = []
    for c in contours:
        region = measure.regionprops(c.astype(int))[0]
        equivalent_diameters.append(region.equivalent_diameter)

    # Calculate average grain size
    avg_grain_size = sum(equivalent_diameters) / len(equivalent_diameters)

    print("Average Grain Size: ", avg_grain_size)


    # print(f"average grain size in micron {average_grain_size*conversion_factor}")
    return avg_grain_size*conversion_factor

# specify the directory to iterate over
dir_path = 'D:\Important\M.Teh thesis\For ML pushpendra\For ML pushpendra'

# # loop through all files and directories in the specified directory
for filename in os.listdir(dir_path):
    # construct the full file path
    file_path = os.path.join(dir_path, filename)
    
    # check if the current item is a file
    if os.path.isfile(file_path):
        # process the file
        print('Processing file:', file_path)
        
    # check if the current item is a directory
    elif os.path.isdir(file_path):
        # process the directory
        print('Processing directory:', file_path)
        for sub_filename in os.listdir(dir_path+"/"+filename):
            # print(sub_filename,filename)
            file_path=os.path.join(dir_path+"\\"+filename, sub_filename)
            if os.path.isfile(file_path):
                if file_path[-3:]!='xls' and file_path[-3:]!='csv':
                    grain_size=calculate_grain_size(file_path,sub_filename)
                
                    sub_data=pd.DataFrame(columns=['Specimen_name','image_name','Grain_size'])
                    sub_data['Specimen_name']=[filename]
                    sub_data['image_name']=[sub_filename]
                    sub_data['Grain_size']=[grain_size]
                    # print(sub_data)
                    data = pd.concat([data, sub_data], ignore_index=True)
                    # data.append({image_name:grain_size},ignore_index=True)

                    # print(file_path)
            else:
                print("Not going inside {file_path}")
print(data.head())
data.to_csv("data.csv")
