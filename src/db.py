import sqlite3
from pathlib import Path

class NotCreatedError(sqlite3.Error):
    def __init__(self):
        super().__init__()

conn=None
cur=None
dbname=None

def init():
    global conn
    global cur
    global dbname
    if cur==None:
        dbname=".files.db"
        dbfound=False
        i=0
        while i<100000:
            db=list(Path("./").glob(dbname))
            if len(db)==0:
                i+=1
                dbname=".files"+str(i)+".db"
                continue
            else:
                db=str(db[0])
            conn=sqlite3.connect(db)
            cur=conn.cursor()
            try:
                cur.execute('CREATE TABLE IF NOT EXISTS files(id STRING,path STRING)')
            except sqlite3.Error:
                i+=1
                dbname=".files"+str(i)+".db"
            else:
                dbfound=True
                break
        if not dbfound:
            dbname=".files.db"
    i=0
    changed=False
    while True:
        conn=sqlite3.connect(dbname)
        cur=conn.cursor()
        try:
            cur.execute('CREATE TABLE IF NOT EXISTS files(id STRING,path STRING)')
            break
        except sqlite3.Error:
            i+=1
            dbname=".files"+str(i)+".db"
            changed=True
    return changed

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