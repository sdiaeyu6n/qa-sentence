import os

path = 'C:/Users/User/OneDrive/바탕 화면/2022/학부연구생/QA/'
file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.startswith('CBCA')]

print(file_list_py)