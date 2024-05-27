import sqlite3

conn=sqlite3.connect("files.db")
cur=conn.cursor()

def init():
    cur.execute('CREATE TABLE IF NOT EXISTS files(id STRING,path STRING)')
    return

def close():
    cur.close()
    conn.close()
    return

def all():
    cur.execute('SELECT * FROM files')
    return cur

def create(id,path):
    cur.execute("insert into files(id,path) values(?,?);",(str(id),str(path)))
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