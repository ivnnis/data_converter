from tkinter import *
from tkinter import filedialog as fd
import pandas as pd
import zipfile
import os 

root = Tk()


df = pd.DataFrame()
result_file_name = ''

# открывает файл и загружает его pandas 
def open_file():
    global df
    global result_file_name
    
    header = []
    filename = fd.askopenfilename()
    result_file_name = filename[:-4]
    zip = zipfile.ZipFile(filename)
    zip.extractall(r'\extracted')
    zip.close()
    files = os.listdir(r'\extracted')
    for file_name in files:
        if 'ttl' in file_name:
            with open('C:\\extracted\\'+file_name) as f:
                for line in f.readlines():
                    if 'Priz=' in line:
                        header = line[5:-1].split('#')
        if 'txt' in file_name and 'ИС_БД' in file_name:
            df = pd.read_csv('C:\\extracted\\'+file_name, sep='#', encoding='ansi', names=header)
            df = df.fillna(0)
            df = df.astype({'ИНН': 'int64'})
    for file_name in files:        
        os.remove('C:\\extracted\\'+file_name)

#сохраняет файл из датафрейма
def save_new_file():
    filename = fd.asksaveasfile(mode='w', defaultextension=".csv", initialfile = result_file_name)
    df.to_csv(filename, sep=',', index=False, line_terminator='\n')



read_source_file = Button(root, text='open', command=open_file)
save_file = Button(root, text='save', command=save_new_file)

read_source_file.place(x=25, y=20)
save_file.place(x=25, y=50)


root.mainloop()
 