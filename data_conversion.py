import pandas as pd
data=pd.read_csv("D:\Important\M.Teh thesis\For ML pushpendra\ML for thesis\ML-in-Friction-Stir-Welding\data.csv")
print(data.isnull().sum())
data['Grain size in micron']=[0 for _ in range(len(data))]
data['phase_ratio']=[0 for _ in range(len(data))]
for i in range(len(data)):
    sub_filename=data['image_name'].loc[i]
    X = 10 # magnification factor
    if "100X" in sub_filename:
        X=1.22
    elif "200X" in sub_filename:
        X=2.44
    elif "500X" in sub_filename:
        X=6.1
    elif "1000X" in sub_filename:
        X=12.2
    data['Grain size in micron'].loc[i]=data['Grain_size_in_pixels'].loc[i]*(1/X)
    data['phase_ratio'].loc[i]=data['ferrite_%'].loc[i]/data['pearlite_%'].loc[i]

data.to_csv("data.csv",index=False)