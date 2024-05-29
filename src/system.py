from src import db
import platform
import sys
import signal

def close():
    db.close()
    sys.exit()

def handler(signal,frame):
    close()
    return

casesensitive=False
def init():
    global casesensitive
    db.init()
    signal.signal(signal.SIGINT,handler)
    p=platform.system()
    if p=="Linux":
        casesensitive=True
    return