from src import db
import platform
import sys
import signal
import subprocess
import os
from pathlib import Path

def close():
    print()
    db.close()
    sys.exit()

def handler(signal,frame):
    close()
    return

def fileexistance():
    cur=db.all()
    for item in cur:
        if not os.path.exists(item[1]):
            db.delete(item[1])
            print(str(Path(item[1]).relative_to(Path.cwd()))+" is deleted.")
    return

pip="pip"
def chardetinstall():
    try:
        subprocess.run(pip+" list|grep chardet",shell=True,capture_output=True,text=True,check=True)
    except subprocess.CalledProcessError:
        print("\"chardet\" did not found.")
        try:
            while True:
                agree=input("This program use external package \"chardet\". Do you agree to install (Y/n)?> ")
                if agree=="y":
                    agree=True
                    break
                elif agree=="n":
                    agree=False
                    break
        except EOFError:
            close()
        if not agree:
            close()
        try:
            subprocess.run(pip+" install chardet",shell=True,capture_output=True,text=True,check=True)
            print("\"chardet\" installed.")
        except subprocess.CalledProcessError:
            print("\"chardet\" could not installed.")
            close()
    return

casesensitive=False
def init():
    global casesensitive
    global pip
    p=platform.system()
    if p=="Linux":
        casesensitive=True
    try:
        subprocess.run("pip -V",shell=True,capture_output=True,text=True,check=True)
        pip="pip"
    except subprocess.CalledProcessError:
        try:
            subprocess.run("pip3 -V",shell=True,capture_output=True,text=True,check=True)
            pip="pip3"
        except subprocess.CalledProcessError:
            print("pip not found!\nThis program use pip to install \"chardet\" package for determine Character Encoding Scheme.")
            print("To install pip, use following commands.")
            print("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
            print("python get-pip.py")
            sys.exit()
    db.init()
    signal.signal(signal.SIGINT,handler)
    chardetinstall()
    return