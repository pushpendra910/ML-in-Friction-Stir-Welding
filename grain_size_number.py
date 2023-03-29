import cv2
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image

gsn=pd.DataFrame(columns=['image_name','Grain_size_number'])

# Define function to calculate grain size number
def calculate_grain_size_number(image_file_path, shape='circle', radius=130, magnification=1000):
    # Load image and convert to grayscale
    img = cv2.imread(image_file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to smooth image
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Threshold the image to binary
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Find contours of objects in the image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask to inscribe the shape on
    mask = np.zeros_like(gray)

    # Get center coordinates of the image
    h, w = gray.shape[:2]
    center_x, center_y = w//2, h//2

    # Inscribing a shape on mask
    if shape == 'circle':
        cv2.circle(mask, (center_x, center_y), radius, 255, -1)
    elif shape == 'square':
        x1, y1 = center_x-radius, center_y-radius
        x2, y2 = center_x+radius, center_y+radius
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

    # Apply mask to get only the area of interest
    masked = cv2.bitwise_and(thresh, thresh, mask=mask)

    # Show the masked image
    cv2.imshow('Masked Image', masked)
    cv2.waitKey(0)

    # Create a new mask to get only the grains
    grain_mask = np.zeros_like(masked)

    # Find contours of grains in the image
    grain_contours, _ = cv2.findContours(masked, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw each grain contour on the grain mask
    for grain in grain_contours:
        cv2.drawContours(grain_mask, [grain], -1, 255, -1)

    # Show the grain mask
    cv2.imshow('Grain Mask', grain_mask)
    cv2.waitKey(0)

    # Count the number of grains that are completely within the area
    # grain_mask=masked ## delete it
    _, complete_grains = cv2.threshold(grain_mask, 254, 255, cv2.THRESH_BINARY)
    num_complete_grains = cv2.countNonZero(complete_grains)

    # Count the number of grains that are partially within the area
    _, partial_grains = cv2.threshold(grain_mask, 254, 255, cv2.THRESH_BINARY)
    num_partial_grains = cv2.countNonZero(partial_grains) - num_complete_grains

    # Divide the result from (c) by 2
    num_partial_grains /= 2
    print(f"number of partial grains {num_partial_grains}")
    print(f"number of complete grains {num_complete_grains}")
    # Add the result from (d) to the result from (b)
    num_total_grains = num_complete_grains + num_partial_grains

    # Divide the result from (e) by A
    A = np.pi * radius**2
    A=A*1.04*(10**(-9))
    print(f"A {A}")
    grains_per_area = num_total_grains / A
    print(num_total_grains)
    # Convert the result from (f) to grains/in2 @
    grains_per_sqaure_inch = grains_per_area * ((magnification / 100) ** 2)
    print(grains_per_sqaure_inch)
    n = 0.6989 + np.log10(grains_per_sqaure_inch)
    print("n",n)

image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@1000X.bmp"

calculate_grain_size_number(image_path)

dir_path = r"D:\Important\M.Teh thesis\For ML pushpendra\all_images"

# # loop through all files and directories in the specified directory
# for filename in os.listdir(dir_path):
#     # construct the full file path
#     file_path = os.path.join(dir_path, filename)
    
#     # check if the current item is a file
#     if os.path.isfile(file_path):
#         # process the file
#         print('Processing file:', file_path)
#         magnification=int(filename[-8:-5])
#         # break
#         number=grain_size_number(file_path,magnification)
    
#         sub_gsn=pd.DataFrame(columns=['image_name','Grain_size_number'])
#         sub_gsn['image_name']=[filename]
#         sub_gsn['Grain_size_number']=[number]
#         # print(sub_data)
#         gsn = pd.concat([gsn, sub_gsn], ignore_index=True)
#         # data.append({image_name:grain_size},ignore_index=Tru
#         # print(file_path)
# print(gsn.head())
# gsn.to_csv("grain_size_number.csv")

# image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp"
# grain_size_number(image_path,50)
# image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@1000X.bmp"
# grain_size_number(image_path,000)
# image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@100X.bmp"
# grain_size_number(image_path,100)