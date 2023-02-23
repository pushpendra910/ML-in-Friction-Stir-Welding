import cv2
import numpy as np
import os
from skimage import morphology, measure
import pandas as pd
import matplotlib.pyplot as plt

data=pd.DataFrame(columns=['image_name','Grain_size_in_micron'])
conversion_factor=1/12.2

def calculate_grain_size(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform noise reduction using morphological opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)

    # Apply automatic thresholding to obtain a binary image
    thresh = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

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


    # Find the grain size
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(erosion, connectivity=8)
    # The first label corresponds to the background, so we exclude it from the statistics
    stats = stats[1:]
    grain_sizes = stats[:, cv2.CC_STAT_AREA]

    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate grain sizes and print average grain size
    diameters = []
    for i in range(1, labels.max()+1):
        area = np.sum(labels == i)
        diameter = 2 * np.sqrt(area/np.pi)
        diameters.append(diameter)

    # Calculate the average diametrical size of the grains
    diameters.sort(reverse=True)

    avg_size = np.mean(diameters[10:-50])
    print("Average diametrical size of grains in pixels: ", avg_size)
    # Display the grain size histogram
    # plt.hist(grain_sizes, bins=50)
    # plt.xlabel('Grain Size')
    # plt.ylabel('Frequency')
    # plt.show()

    # Display the grain-separated image
    # cv2.imshow('Grain Separation', erosion)
    # cv2.waitKey(0)

    # Display the original image, noise-reduced image, grayscale image, and binary image
    # cv2.imshow('Original Image', img)
    # cv2.imshow('Noise-Reduced Image', opening)
    # cv2.imshow('Grayscale Image', gray)
    # cv2.imshow('Binary Image', thresh)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    return avg_size

# specify the directory to iterate over
dir_path = "D:\Important\M.Teh thesis\For ML pushpendra\Enlarged_images"

# # loop through all files and directories in the specified directory
for filename in os.listdir(dir_path):
    # construct the full file path
    file_path = os.path.join(dir_path, filename)
    
    # check if the current item is a file
    if os.path.isfile(file_path):
        # process the file
        print('Processing file:', file_path)
        grain_size=calculate_grain_size(file_path)
    
        sub_data=pd.DataFrame(columns=['image_name','Grain_size_in_micron'])
        sub_data['image_name']=[filename]
        sub_data['Grain_size_in_micron']=[grain_size]
        # print(sub_data)
        data = pd.concat([data, sub_data], ignore_index=True)
        # data.append({image_name:grain_size},ignore_index=Tru
        # print(file_path)
print(data.head())
data.to_csv("data.csv")
# image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@200X.bmp"
# calculate_phase_ratio(image_path)
# image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp"
# calculate_phase_ratio(image_path)
# image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp"
# calculate_grain_size(image_path)