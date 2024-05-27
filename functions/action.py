from functions import db
from functions import file
from pathlib import Path
import os

def find(find):
    cur=db.all()
    for row in cur:
        for i in row:
            if str(i)==str(find):
                return Path(row[1])
    return None

def findpath(option,item):
    if option=="-i":
        path=find(item)
    elif option=="-p":
        path=find(Path(item).resolve())
    else:
        return None,0
    if path==None:
        print("Not Found: "+item)
        return None,1
    return path,None

def create(id,path):
    rowid=find(id)
    abspath=Path(path).resolve()
    rowpath=find(abspath)
    if rowid!=None and rowpath!=None and rowid==rowpath:
        print("Already exist id: "+id+", and path: "+path)
        return
    if rowpath!=None:
        print(path+" is already exists as "+str(abspath.relative_to(Path.cwd())))
        return
    if rowid!=None:
        while True:
            overwrite=input(id+" is already exists. Do you want to overwrite? [y or n]> ")
            if overwrite=="y":
                db.delete(rowid)
                break
            elif overwrite=="n":
                print("Create canceled.")
                return
    if not os.path.exists(abspath):
        print("File not found.")
        return
    db.create(id,abspath)
    return

def showall():
    cur=db.all()
    for row in cur:
        path=Path(row[1])
        print("id: "+row[0]+"\t\tpath: "+str(path.relative_to(Path.cwd())))
    return

def retrieve(option,item):
    path,e=findpath(option,item)
    if e==0:
        print("No such action. Input help for command list.")
        return
    elif e==1:
        return
    print(file.read(path))
    return

def update(option,item,id):
    path,e=findpath(option,item)
    if e==0:
        print("No such action. Input help for command list.")
        return
    elif e==1:
        return
    row=find(id)
    if path==row:
        print("Nothing changed.")
        return
    if row!=None:
        while True:
            overwrite=input(id+" is already exists. Do you want to overwrite? [y or n]> ")
            if overwrite=="y":
                db.delete(row)
                break
            elif overwrite=="n":
                print("Update canceled.")
                return
    db.update(id,path)
    return

def delete(option,item):
    path,e=findpath(option,item)
    if e==0:
        print("No such action. Input help for command list.")
        return
    elif e==1:
        return
    db.delete(path)
    return

def help():
    print("----------")
    print("Options\t\t\t\t-i -p")
    print("Variables\t\t\t[id] [file] [id1] [id2]")
    print("[id] [id1] [id2]\t\tPut id such as Q1, Q2, K1, K2, R1, R2...")
    print("[file]\t\t\t\tPut file name or path.")
    print("----------")
    print()
    print("create [id] [file]\t\tCreate [file] in DB with name [id].")
    print("retrieve\t\t\tShow all id and file.")
    print("retrieve -i [id]\t\tRead text which named [id].")
    print("retrieve -p [file]\t\tRead text in [file].")
    print("update -i [id1] [id2]\t\tUpdate [id1] with [id2].")
    print("update -p [file] [id]\t\tUpdate id of [file] with [id].")
    print("delete -i [id]\t\t\tDelete file named [id].")
    print("delete -p [file]\t\tDelete [file].")
    print("quit\t\t\t\tQuit.")
    print("help\t\t\t\tShow help.")