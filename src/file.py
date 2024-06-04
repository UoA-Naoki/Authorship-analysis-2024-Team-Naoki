import importlib
from src import system

def CESdetect(path):
    system.chardetinstall()
    chardet=importlib.import_module("chardet")
    try:
        f=open(path,'rb')
    except OSError:
        print("No such file or directory.")
        return "utf-8"
    else:
        return chardet.detect(f.read())["encoding"]
    
def read(path):
    try:
        f=open(path,'r',encoding=CESdetect(path))
    except OSError:
        return
    else:
        text=f.read()
        f.close()
        return text