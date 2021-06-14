import shutil
import os
import re

path = r"D:\BaiduNetdiskDownload\mri"

def sort_file(path):
    files_list = os.listdir(path)
    for file in files_list:
        filename, suffix = os.path.splitext(file)
        label = filename.split('_')[0]
        label=re.sub(r'[A-Z]', '', label)
        print(label)
        dict = {'mwp1': 'GrayMatter', 'mwp2': 'WhiteMatter', 'p0': 'OriginalImg', 'wm' : 'T1Img'}
        filePath = path + "\\" + file
        sortPath = path + "\\" + dict[label]
        if not os.path.exists(sortPath):
            os.makedirs(sortPath)
        shutil.move(filePath, sortPath)

sort_file(path)