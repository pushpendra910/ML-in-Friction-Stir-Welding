import cv2
import numpy as np
import os
from skimage import morphology, measure
import pandas as pd

dir_path = 'D:\Important\M.Teh thesis\For ML pushpendra\For ML pushpendra'
save_path=r"D:\Important\M.Teh thesis\For ML pushpendra\all_images"
def all_images(image_path,sub_filename,file_name):
    # Load the image
    image = cv2.imread(image_path)
    save=save_path+str("\\")+str(file_name)+str("+")+str(sub_filename)
    print(save)
    cv2.imwrite(save, image)


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
                    all_images(file_path,sub_filename,filename)
            else:
                print("Not going inside {file_path}")

