import os
from pathlib import Path
from xml.dom.minidom import parse
import shutil


#def collect_packages(path: str, save_path: str) -> str:
def check_packages(str) -> bool:
    #str = "R01 KK56 50UKC 0 ET WP WD101=r01.pdf".split()
    flag = True

    for i in range(len(str)):
        if i == 0:
            j = 0
            if (str[i][j] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') and (str[i][j+1] in '0123456789') and (str[i][j+2] in '0123456789'):
                continue
            elif (str[i][j] == '_') and (str[i][j+1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') and (str[i][j+2] in '0123456789') and (str[i][j+3] in '0123456789'):
                continue
            else:
                flag = False
                break
        if i == 1:
            if ((str[i] == 'KK56') or (str[i] == 'KK34') or (str[i] == 'KK36')):
                continue
            else:
                flag = False
                break
        if i == 2:
            j = 0
            if (str[i][j] in '0123456789') and (str[i][j+1] in '0123456789') and (str[i][j+2] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') and (str[i][j+3] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') and (str[i][j+3] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                continue
            else:
                flag = False
                break
        if i == 3:
            if (str[3] == '0') and (str[4] == 'ET') and (str[5] == 'WP'):
                continue
            else:
                flag = False
                break
        if i == 6:
            j = 0
            if (str[i][j] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') and (str[i][j+1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') and (str[i][j+2] in '0123456789') and (str[i][j+3] in '0123456789') and (str[i][j+4] in '0123456789'):
                continue
            else:
                flag = False
                break
        if i == 6:
            j = 0
            if (str[i][j+6] == 'e' or str[i][j+7] == 'r') and (str[i][j+8] in '0123456789'):
                continue
        if i == 6:
            if str[i][-3::] == 'doc' or str[i][-3::] == 'docx':
                continue
            else:
                flag = False
                break
    return flag


if __name__ == '__main__':
    path = 'example'
    save_path = 'example_collected'
    #check_packages(path, save_path)
    check_packages(str)