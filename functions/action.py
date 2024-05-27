from functions import db
from functions import file
from pathlib import Path
import os

def abspath(path):
    return str(Path(path).resolve())

def relpath(path):
    return str(Path(path).relative_to(Path.cwd()))

def find(find):
    cur=db.all()
    for row in cur:
        for i in row:
            if str(i)==str(find):
                return row[1]
    return None

def findpath(option,item):
    if option=="-i":
        item=item.upper()
        path=find(item)
    elif option=="-p":
        path=find(abspath(item))
    else:
        print("No such action. Input help for command list.")
        return None
    if path==None:
        print("Not Found: "+item)
        return None
    return path

def overwrite(id,path):
    while True:
        overwrite=input(id+" is already exists. Do you want to overwrite? [y or n]> ")
        if overwrite=="y" or overwrite=="Y":
            db.delete(path)
            break
        elif overwrite=="n" or overwrite=="N":
            print("Action canceled.")
            return
    return

def create(id,path):
    id=id.upper()
    rowid=find(id)
    path=abspath(path)
    rowpath=find(path)
    if rowid!=None and rowpath!=None and rowid==rowpath:
        print("Already exist id: "+id+", and path: "+relpath(path))
        return
    if rowpath!=None:
        print(relpath(path)+" is already exists.")
        return
    if rowid!=None:
        overwrite(id,rowid)
    if not os.path.exists(path):
        print("File not found.")
        return
    db.create(id,path)
    return

def showall():
    cur=db.all()
    for row in cur:
        print("id: "+row[0]+"\t\tpath: "+relpath(row[1]))
    return

def retrieve(option,item):
    path=findpath(option,item)
    if path==None:
        return
    print(file.read(path))
    return

def update(option,item,id):
    path=findpath(option,item)
    if path==None:
        return
    id=id.upper()
    row=find(id)
    if path==row:
        print("Nothing changed.")
        return
    if row!=None:
        overwrite(id,row)
    db.update(id,path)
    return

def delete(option,item):
    path=findpath(option,item)
    if path==None:
        return
    db.delete(path)
    return

def help():
    print(file.read(".help.txt"))