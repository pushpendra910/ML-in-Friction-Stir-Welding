import cv2
from skimage import measure
import numpy as np
import pandas as pd
import os

def calculate_phase_ratio(image_path):

    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform noise reduction using morphological opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)

    # Apply automatic thresholding to obtain a binary image
    thresh = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    binary = cv2.bitwise_not(thresh)
    # Perform area-based noise removal
    a = 30
    _, labels = cv2.connectedComponents(thresh)
    unique, counts = np.unique(labels, return_counts=True)
    for i, count in enumerate(counts):
        if count <= a:
            thresh[labels == i] = 0

    # perform morphological closing for grain separation
    k = 1
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(k,k))
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # perform dilation before erosion for better grain division
    kernel = np.ones((1,1), np.uint8)
    dilation = cv2.dilate(closing, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    # cv2.imshow('binary',binary)
    # cv2.waitKey(0)
    # Define the regions of interest for ferrite and perlite
    pearlite_roi = erosion == 0
    ferrite_roi = erosion == 255

    # Calculate the area of each phase
    ferrite_area = np.count_nonzero(ferrite_roi)
    pearlite_area = np.count_nonzero(pearlite_roi)
    total_area=ferrite_area+pearlite_area
    ferrite_area=ferrite_area/total_area
    pearlite_area=pearlite_area/total_area

    # Calculate the phase ratio
    phase_ratio = pearlite_area / ferrite_area

    print("Ferrite area:", ferrite_area)
    print("Pearlite area:", pearlite_area)
    print("Phase ratio:", phase_ratio)
    return ferrite_area,pearlite_area

dir_path = r"D:\Important\M.Teh thesis\For ML pushpendra\all_images"
# # loop through all files and directories in the specified directory
phase=pd.DataFrame(columns=['ferrite','pearlite'])
for filename in os.listdir(dir_path):
    # construct the full file path
    file_path = os.path.join(dir_path, filename)
    
    # check if the current item is a file
    if os.path.isfile(file_path):
        # process the file
        print('Processing file:', file_path)
        f,p=calculate_phase_ratio(file_path)
        
        sub_data=pd.DataFrame(columns=['ferrite','pearlite'])
        sub_data['ferrite']=[f*100]
        sub_data['pearlite']=[p*100]
        # print(sub_data)
        phase = pd.concat([phase, sub_data], ignore_index=True)
        # data.append({image_name:grain_size},ignore_index=Tru
        # print(file_path)
print(phase.head())
data=pd.read_csv("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\data.csv")
data['ferrite_%']=phase['ferrite']
data['pearlite_%']=phase['pearlite']
# data['new name']=phase['image_name']
data.to_csv("data.csv", index=False)

# image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@1000X.bmp"
# calculate_phase_ratio(image_path)