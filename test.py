import cv2
import numpy as np
import numpy as np
import os
from skimage import morphology, measure
import pandas as pd
# Load the image
img = cv2.imread("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@100X.bmp")

# Enhance the image quality
img = cv2.bilateralFilter(img, 9, 75, 75)
img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

# Resize the image to 10 times larger
height, width = img.shape[:2]
img_resized = cv2.resize(img, (10*width, 10*height), interpolation=cv2.INTER_CUBIC)

# Crop the image to the original size
crop_x = int((10*width - width) / 2)
crop_y = int((10*height - height) / 2)
img_cropped = img_resized[crop_y:crop_y+height, crop_x:crop_x+width]

# Display the original and processed images
cv2.imshow('Original Image', img)
cv2.imshow('Processed Image', img_cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('enhanced_image.jpg', img_cropped)

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

    print("Average Grain Size: ", avg_grain_size*conversion_factor)


    # print(f"average grain size in micron {average_grain_size*conversion_factor}")
    return avg_grain_size*conversion_factor
calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@100X.bmp","100X")
calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@200X.bmp","200X")
calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp","500X")
calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\enhanced_image.jpg","1000X")
calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@1000X.bmp","1000X")