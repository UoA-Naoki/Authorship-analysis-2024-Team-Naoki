from src import db
from src import file
from src import system
from pathlib import Path
import os
import glob
import fnmatch

def abspath(path):
    return str(Path(path).resolve())

def relpath(path):
    try:
        path=str(Path(path).relative_to(Path.cwd()))
    except ValueError:
        path=str(Path(path))
    return path

def find(find):
    cur=db.all()
    for row in cur:
        for i in row:
            if str(i)==str(find):
                return row[1]
    return None

def wildcard(things,fs=False):
    items=[]
    for item in things:
        if fs:
            found=glob.glob(item)
        else:
            cur=db.all()
            paths=[]
            for row in cur:
                paths.append(relpath(row[1]))
            found=fnmatch.filter(paths,item)
        if len(found)==0:
            items.append(item)
        items.extend(found)
    items=list(set(items))
    return items

def findpath(option,item,v=True):
    if option=="-i":
        item=str(item).upper()
        path=find(item)
    elif option=="-p":
        path=find(abspath(item))
    else:
        print("No such action. Input help for command list.")
        return 0
    if path==None and v:
        print("Not Found: "+item)
        return None
    return path

def findid(id):
    cur=db.all()
    for row in cur:
        if str(id)==str(row[0]):
            return True
    return False

def overwrite(id,path):
    while True:
        try:
            overwrite=input(id+" is already exists. Do you want to overwrite (Y/n)?> ")
        except EOFError:
            print("Action canceled.")
            system.close()
        if overwrite=="y" or overwrite=="Y":
            db.delete(path)
            return
        elif overwrite=="n" or overwrite=="N":
            print("Action canceled.")
            return

def creatable(item):
    path=findpath("-p",item,False)
    if path!=None:
        print(relpath(path)+" is already exists.")
        return None
    if not os.path.exists(item):
        print("Not found: "+relpath(item))
        return None
    return abspath(item)

def create(idtype,items):
    idtype=str(idtype).upper()
    idnum=1
    id=idtype+str(idnum)
    for item in items:
        while findid(id):
            idnum+=1
            id=idtype+str(idnum)
        path=creatable(item)
        if path!=None:
            db.create(id,path)
    return

def showall():
    cur=db.all()
    for row in cur:
        print("id: "+row[0]+"\t\tpath: "+relpath(row[1]))
    return

def retrieve(option,item):
    path=findpath(option,item)
    if path==None or path==0:
        return
    print(file.read(path))
    return

def update(option,item,id):
    path=findpath(option,item)
    if path==None or path==0:
        return
    id=str(id).upper()
    row=find(id)
    if path==row:
        print("Nothing changed.")
        return
    if row!=None:
        overwrite(id,row)
    db.update(id,path)
    return

def delete(option,items):
    for item in items:
        path=findpath(option,item)
        if path==None or path==0:
            continue
        db.delete(path)
    return

def help():
    print(file.read(".help.txt"))