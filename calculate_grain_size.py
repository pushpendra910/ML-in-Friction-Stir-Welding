import cv2
import numpy as np
import os
import pandas as pd

data=pd.DataFrame(columns=['Specimen_name','image_name','Grain_size'])

def calculate_grain_size(image_path,sub_filename):
    # Load the microstructure image
    img = cv2.imread(image_path)
    # cv2.imshow('Original image', img)
    # cv2.waitKey(0)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to create a binary image
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Apply a morphological closing operation to fill in any small gaps
    kernel = np.ones((3,3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    # cv2.imshow('closing', closing)
    # cv2.waitKey(0)
    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    # print(hierarchy)
    # Calculate the equivalent diameter of each contour
    equivalent_diameters = []
    conversion_factor=1
    if "100X" in sub_filename:
        conversion_factor=1/1.22
    elif "200X" in sub_filename:
        conversion_factor=1/2.44
    elif "500X" in sub_filename:
        conversion_factor=1/6.1
    elif "1000X" in sub_filename:
        conversion_factor=1/12.2
    
    for contour in contours:
        area = cv2.contourArea(contour)
        equivalent_diameter = np.sqrt(4 * area / np.pi)
        equivalent_diameter=equivalent_diameter
        equivalent_diameters.append(equivalent_diameter)

    # Calculate the average grain size
    equivalent_diameters.sort(reverse=True)
    equivalent_diameters=equivalent_diameters[10:50]
    average_grain_size = np.mean(equivalent_diameters)

    # print(f"average grain size in micron {average_grain_size*conversion_factor}")
    return average_grain_size*conversion_factor

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
