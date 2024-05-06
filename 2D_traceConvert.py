from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import glob
import os
import natsort
import vtk
from scipy.interpolate import interp1d

def stringConvert(AD):
    list_of_points = []

    for i, a in enumerate(AD):
        intermediate = str(a)[9:-10]
        intermediate = intermediate.split(', ')

        list_of_points.append((0.0, float(intermediate[0]), float(intermediate[1])))

    return list_of_points

def bezier_curve_3d(points, n_points=101):
    n = len(points)
    t = np.linspace(0, 1, n, endpoint=True)
    _, y, z = zip(*points)
    fy = interp1d(t, y, kind='cubic')
    fz = interp1d(t, z, kind='cubic')
    t_new = np.linspace(0, 1, n_points, endpoint=True)
    y_new = fy(t_new)
    z_new = fz(t_new)
    return np.column_stack((np.zeros(n_points), y_new, z_new))

def rotate_z_180(curve):
    theta = np.pi  # 180 degrees in radians
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]])
    return np.dot(curve, rotation_matrix.T)

def rotate_x_180(curve):
    theta = np.pi  # 180 degrees in radians
    rotation_matrix = np.array([[1, 0, 0],
                                [0, np.cos(theta), -np.sin(theta)],
                                [0, np.sin(theta), np.cos(theta)]])
    return np.dot(curve, rotation_matrix.T)


xml_file_path = r"/Users/liammartin/Downloads/PB_Other_traces/Evacuation/*.xml"
studyName = "_Evacuation"
files = glob.glob(xml_file_path)
xml_file_path = os.path.dirname(files[0])
writer = vtk.vtkPolyDataWriter()

for i in range(len(files)):
    files[i] = os.path.basename(files[i])

files = natsort.natsorted(files)
filenames = np.empty((len(files), 1)).tolist()
traces = []

for j, filename in enumerate(files):
    with open(os.path.join(xml_file_path, filename), 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "lxml")
    angleData = Bs_data.find_all('array')[1].find_all('string')

    tempList = stringConvert(angleData)

    traces.append(tempList)

for i, trace in enumerate(traces):
    vtk_points = vtk.vtkPoints()
    polyLine = vtk.vtkCellArray()
    trace = bezier_curve_3d(trace)
    trace = rotate_z_180(trace)
    trace = rotate_x_180(trace)
    polyLine.InsertNextCell(len(trace))
    
    for j in range(len(trace)):
        vtk_points.InsertNextPoint(trace[j])
        polyLine.InsertCellPoint(j)

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(vtk_points)
    polyData.SetLines(polyLine)

    print(files[i])

    newFilename = files[i][:-4] + studyName + '.vtk'
    writer.SetFileName(os.path.join(xml_file_path, newFilename))
    # writer.SetFileVersion(42)
    writer.SetInputData(polyData)
    writer.Write()