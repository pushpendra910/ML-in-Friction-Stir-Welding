import cv2
import numpy as np

# Load the microstructure image
img = cv2.imread('D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\WM1@100X.bmp')
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
conversion_factor=1/1.22
for contour in contours:
    area = cv2.contourArea(contour)
    equivalent_diameter = np.sqrt(4 * area / np.pi)
    equivalent_diameter=equivalent_diameter*conversion_factor
    equivalent_diameters.append(equivalent_diameter)

# Calculate the average grain size
average_grain_size = np.mean(equivalent_diameters)
print("At the end")

print(average_grain_size/conversion_factor)
