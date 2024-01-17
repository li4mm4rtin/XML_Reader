from bs4 import BeautifulSoup
import numpy as np
import math
import pandas as pd
import glob
import os
import natsort


def stringConvert(AD, PS):
    numericPoints = np.empty((3, 2))

    for i, a in enumerate(AD):
        intermediate = str(a)[9:-10]
        intermediate = intermediate.split(', ')

        numericPoints[i] = (float(intermediate[0]), float(intermediate[1]))

    v1 = numericPoints[0] - numericPoints[1]
    v2 = numericPoints[2] - numericPoints[1]

    incAngle = round(math.degrees(math.acos((np.dot(v1, v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2)))), 2)

    v1_length = round((math.sqrt(math.pow(v1[0], 2) + math.pow(v1[1], 2)) * PS)/10, 2)
    v2_length = round((math.sqrt(math.pow(v2[0], 2) + math.pow(v2[1], 2)) * PS)/10, 2)

    return incAngle, v1_length, v2_length


excelData = pd.read_excel('/Users/liammartin/Downloads/Project1/PB_Angle.xlsx')

path = r"/Users/liammartin/Downloads/Project1/*.xml"
files = glob.glob(path)
path = os.path.dirname(files[0])

for i in range(len(files)):
    files[i] = os.path.basename(files[i])

files = natsort.natsorted(files)
angles = np.zeros((len(files), 1))
PCL = np.zeros((len(files), 1))
PBL = np.zeros((len(files), 1))
filenames = np.empty((len(files), 1)).tolist()

for j, filename in enumerate(files):
    with open(os.path.join(path, filename), 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")
    angleData = Bs_data.find_all('array')[1].find_all('string')

    pixelSpacing = excelData["pixelSpacing"][j]

    angle, v1L, v2L = stringConvert(angleData, pixelSpacing)

    angles[j] = angle
    PCL[j] = v1L
    PBL[j] = v2L
    filenames[j] = filename

    print(angle, v1L, v2L, filename)

excelData["PB_Angle"] = angles
excelData["PCL"] = PCL
excelData["PS_PB"] = PBL
excelData["Read Study ID"] = filenames

excelData.to_excel("./output2.xlsx")
