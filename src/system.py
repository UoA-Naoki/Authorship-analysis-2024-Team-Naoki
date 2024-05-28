from src import db
import platform

casesensitive=False
def init():
    global casesensitive
    db.init()
    p=platform.system()
    if p=="Linux":
        casesensitive=True
    return

def close():
    db.close()
    return