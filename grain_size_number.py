import cv2
import numpy as np
import pandas as pd
import os

gsn=pd.DataFrame(columns=['image_name','Grain_size_number'])
def grain_size_number(path,m):
    # Load image
    img = cv2.imread(path)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform noise reduction using morphological opening
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    # Apply automatic thresholding to obtain a binary image
    _, thresh = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Perform area based noise removal
    area_threshold = 50
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < area_threshold:
            cv2.drawContours(thresh, [cnt], 0, 0, -1)

    # Perform morphological closing for grain separation
    kernel = np.ones((1,1),np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Perform dilation before erosion for better grain division and then erosion
    kernel = np.ones((1,1),np.uint8)
    dilation = cv2.dilate(closing, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    cv2.imshow("erosion",erosion)
    cv2.waitKey(0)
    # Inscribe a circle (or other shape) of known area, A, on an image of magnification, M
    A = 150000  # Known area in square pixels
    M=m
    if m==000:
        M=1000
    else:
        M=m
    # M = 10   # Magnification
    img=erosion
    radius = int(np.sqrt(A/np.pi))
    center = (img.shape[1]//2, img.shape[0]//2)  # Center of the image
    cv2.circle(img, center, radius, (0, 255, 0), 2)
    cv2.imshow('circle',img)
    cv2.waitKey(0)
    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of grains that are completely within the area
    grains_completely_within_area = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area <= A and area/M**2 > np.pi*radius**2:
            grains_completely_within_area += 1
    print("grains_completely_within_area",grains_completely_within_area)
    # Count the number of grains that are partially within the area
    grains_partially_within_area = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area > A and area/M**2 > np.pi*radius**2:
            grains_partially_within_area += 1

    # Divide the result from (c) by 2
    grains_partially_within_area /= 2
    print("grains_partially_within_area",grains_partially_within_area)
    # Add the result from (d) to the result from (b)
    total_grains = grains_completely_within_area + grains_partially_within_area
    print("total_grains",total_grains)
    # Divide the result from (e) by A
    grains_per_square_pixel = total_grains/A
    print("grains_per_square_pixel",grains_per_square_pixel)
    # Convert the result from (f) to grains/in2 @ 100x
    grains_per_square_inch = grains_per_square_pixel * M**2 / 100
    print("grains_per_square_inch",grains_per_square_inch)
    # Use the definition of ASTM grain size number to determine n
    n = -1.476 + 3.29*np.log10(grains_per_square_inch)
    print("n",n)
    return n

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
image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@200X.bmp"
grain_size_number(image_path,200)
image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp"
grain_size_number(image_path,50)
image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@1000X.bmp"
grain_size_number(image_path,000)
image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@100X.bmp"
grain_size_number(image_path,100)