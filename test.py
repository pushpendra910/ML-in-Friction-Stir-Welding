import cv2

# Load the image
img = cv2.imread('D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@100X.bmp')
cv2.imshow('img',img)
cv2.waitKey(0)
# Convert the image to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray_img)
cv2.waitKey(0)
# Apply adaptive thresholding
adaptive_threshold = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imshow('Adaptive', adaptive_threshold)
cv2.waitKey(0)
# Apply median blur to remove noise
median_blur = cv2.medianBlur(adaptive_threshold, 5)
cv2.imshow('BLur', median_blur)
cv2.waitKey(0)
# Apply morphology operations
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
closed = cv2.morphologyEx(median_blur, cv2.MORPH_CLOSE, kernel)

# Perform edge detection using Canny
edges = cv2.Canny(closed, 30, 100)

# Display the final image
cv2.imshow('Enhanced Image', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@100X.bmp","100X")
# calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@200X.bmp","200X")
# calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp","500X")
# calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\enhanced_image.jpg","1000X")
# calculate_grain_size("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@1000X.bmp","1000X")