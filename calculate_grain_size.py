import cv2
import numpy as np
import os

# specify the directory to iterate over
# dir_path = 'D:\Important\M.Teh thesis\For ML pushpendra\For ML pushpendra'

# # loop through all files and directories in the specified directory
# for filename in os.listdir(dir_path):
#     # construct the full file path
#     file_path = os.path.join(dir_path, filename)
    
#     # check if the current item is a file
#     if os.path.isfile(file_path):
#         # process the file
#         print('Processing file:', file_path)
        
#     # check if the current item is a directory
#     elif os.path.isdir(file_path):
#         # process the directory
#         print('Processing directory:', file_path)

# Load the microstructure image
img = cv2.imread('D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp')
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
conversion_factor=1/6.5
for contour in contours:
    area = cv2.contourArea(contour)
    equivalent_diameter = np.sqrt(4 * area / np.pi)
    equivalent_diameter=equivalent_diameter
    equivalent_diameters.append(equivalent_diameter)

# Calculate the average grain size
equivalent_diameters=equivalent_diameters[11:-9]
average_grain_size = np.mean(equivalent_diameters)

print(f"average grain size in micron {average_grain_size*conversion_factor}")
# print("Equivalent Diameters")
equivalent_diameters.sort()
# print(len(equivalent_diameters))