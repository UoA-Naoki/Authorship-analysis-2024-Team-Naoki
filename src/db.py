import sqlite3
import glob
import re

class NotCreatedError(sqlite3.Error):
    def __init__(self):
        super().__init__()

class NotTableRestoredError(sqlite3.Error):
    def __init__(self):
        super().__init__()

conn=None
cur=None
dbnum=None

def init():
    global conn
    global cur
    global dbnum
    dbcandlist=glob.glob(".files*.db")
    dbcandpatt=re.compile("\.files\d+\.db")
    dbcands=[]
    for dbcand in dbcandlist:
        if dbcandpatt.fullmatch(dbcand)!=None:
            dbcands.append(dbcandpatt.match(dbcand).group())
    found=False
    for dbcand in dbcands:
        conn=sqlite3.connect(dbcand)
        cur=conn.cursor()
        try:
            cur.execute('CREATE TABLE IF NOT EXISTS files(id STRING,path STRING)')
        except sqlite3.Error:
            continue
        else:
            found=True
            break
    dbnum=0
    while not found:
        dbname=".files"+str(dbnum)+".db"
        conn=sqlite3.connect(dbname)
        cur=conn.cursor()
        try:
            cur.execute('CREATE TABLE IF NOT EXISTS files(id STRING,path STRING)')
        except sqlite3.Error:
            dbnum+=1
        else:
            found=True
    return

def restore(dbname):
    global conn
    global cur
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    try:
        cur.execute('CREATE TABLE IF NOT EXISTS files(id STRING,path STRING)')
    except sqlite3.Error:
        raise NotTableRestoredError
    return

def close():
    cur.close()
    conn.close()
    return

def all():
    cur.execute('SELECT * FROM files ORDER BY LENGTH(id),id ASC')
    return cur

def create(id,path):
    try:
        cur.execute('insert into files(id,path) values(?,?);',(str(id),str(path)))
    except sqlite3.Error:
        raise NotCreatedError
    conn.commit()
    return

def update(id,path):
    cur.execute('UPDATE files SET id=? WHERE path=?',(str(id),str(path)))
    conn.commit()
    return

def delete(path):
    cur.execute('DELETE FROM files WHERE path=?',(str(path),))
    conn.commit()
    return

def deleteall():
    cur.execute('DELETE FROM files')
    conn.commit()
    return