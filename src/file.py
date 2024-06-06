import importlib
from src import system

def CESdetect(path):
    system.chardetinstall()
    chardet=importlib.import_module("chardet")
    try:
        f=open(path,'rb')
    except OSError:
        print("No such file or directory.")
        return "cp932"
    else:
        return chardet.detect(f.read())["encoding"]
    
def read(path):
    try:
        f=open(path,'r',encoding="cp932")
    except OSError:
        print("No such file or directory.")
        return
    except UnicodeDecodeError:
        try:
            f=open(path,'r',encoding="utf-8")
        except OSError:
            print("No such file or directory.")
            return
        except UnicodeDecodeError:
            try:
                f=open(path,'r',encoding=CESdetect(path))
            except OSError:
                return
    text=f.read()
    f.close()
    return text