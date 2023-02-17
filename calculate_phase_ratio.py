import cv2
from skimage import measure
import numpy as np

def calculate_phase_ratio(image_path):


    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Binarize the image using thresholding
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Label the connected components in the binary image
    labels = measure.label(thresh)

    # Compute the region properties of the labeled regions
    props = measure.regionprops(labels, intensity_image=img)

    # Find the regions with the highest and lowest mean intensity
    max_intensity = -1
    min_intensity = 256
    for prop in props:
        if prop.mean_intensity > max_intensity:
            max_intensity = prop.mean_intensity
            max_label = prop.label
        if prop.mean_intensity < min_intensity:
            min_intensity = prop.mean_intensity
            min_label = prop.label

    # Compute the phase fraction
    total_area = img.shape[0] * img.shape[1]
    phase1_area = props[max_label-1].area
    phase2_area = props[min_label-1].area
    phase1_fraction = phase1_area / total_area
    phase2_fraction = phase2_area / total_area

    print('Phase 1 fraction: {:.2f}'.format(phase1_fraction))
    print('Phase 2 fraction: {:.2f}'.format(phase2_fraction))


image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@100X.bmp"
calculate_phase_ratio(image_path)
image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@200X.bmp"
calculate_phase_ratio(image_path)
image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@500X.bmp"
calculate_phase_ratio(image_path)
image_path="D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@1000X.bmp"
calculate_phase_ratio(image_path)