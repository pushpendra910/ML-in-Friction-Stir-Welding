import cv2
import numpy as np
import os
from skimage import morphology, measure
import pandas as pd

dir_path = 'D:\Important\M.Teh thesis\For ML pushpendra\For ML pushpendra'
save_path="D:\Important\M.Teh thesis\For ML pushpendra\Enlarged_images"
def enlarge(image_path,sub_filename,file_name):
    X = 10 # magnification factor
    if "100X" in sub_filename:
        X=10
    elif "200X" in sub_filename:
        X=5
    elif "500X" in sub_filename:
        X=2
    elif "1000X" in sub_filename:
        X=1
    # Load the image
    image = cv2.imread("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\WM1@200X.bmp")
    cv2.imshow('original',image)
    cv2.waitKey(0)
    enhanced = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    cv2.imshow('enhanced',enhanced)
    cv2.waitKey(0)
    # Magnify the image


    height, width = enhanced.shape[:2]
    new_height, new_width = int(height*X), int(width*X)
    resized = cv2.resize(enhanced, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('resized',resized)
    cv2.waitKey(0)
    # Crop the image to the original size
    cropped = resized[int((new_height-height)/2):int((new_height+height)/2), int((new_width-width)/2):int((new_width+width)/2)]
    cv2.imshow('cropped',cropped)
    cv2.waitKey(0)
    save=save_path+str("\\")+str(file_name)+str("+")+str(sub_filename)
    print(save)

    cv2.imwrite(save, cropped)


for filename in os.listdir(dir_path):
    # construct the full file path
    file_path = os.path.join(dir_path, filename)
    
    # check if the current item is a file
    if os.path.isfile(file_path):
        # process the file
        print('Processing file:', file_path)
        
    # check if the current item is a directory
    elif os.path.isdir(file_path):
        print('Processing directory:', file_path)
        for sub_filename in os.listdir(dir_path+"/"+filename):
            # print(sub_filename,filename)
            file_path=os.path.join(dir_path+"\\"+filename, sub_filename)
            if os.path.isfile(file_path):
                if file_path[-3:]!='xls' and file_path[-3:]!='csv':
                    enlarge(file_path,sub_filename,filename)
            else:
                print("Not going inside {file_path}")

