from src import db
import os
from pathlib import Path

def read(path):
    try:
        f=open(path,'r')
    except OSError:
        print("No such file or directory.")
        return 0
    else:
        text=f.read()
        f.close()
        return text

def existancecheck():
    cur=db.all()
    for item in cur:
        if not os.path.exists(item[1]):
            db.delete(item[1])
            print(str(Path(item[1]).relative_to(Path.cwd()))+" is deleted.")
    return