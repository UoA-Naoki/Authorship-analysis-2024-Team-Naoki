import sqlite3

class File:
    def __init__(self,name):
        self.name=name

    def read(self):
        try:
            f=open(self.name,'r')
        except OSError:
            print("No such file or directory.")
            return 0
        else:
            text=f.read()
            f.close()
            return text

class Actions:
    def show(self,row):
        print("id: "+row[0])
        print("name: "+row[1])
        print()
        print(row[2])
    
    def find(self, find):
        actions=Actions()
        cur.execute('SELECT * FROM files')
        for row in cur:
            if find=="all":
                print("----------")
                actions.show(row)
                print()
            else:
                for i in row:
                    if i==find:
                        return row
        return 0
    
    def create(self):
        actions=Actions()
        name=input("Name?> ")
        row=actions.find(name)
        if row!=0:
            print(name+" is already exists")
            return
        id=input("id?> ")
        row=actions.find(id)
        if row!=0:
            print(id+" is already exists")
            return
        file=File(name)
        text=file.read()
        if text==0:
            return
        cur.execute("insert into files(id,name,text) values(?,?,?);",(id,name,text))
        conn.commit()

    def retrieve(self):
        actions=Actions()
        file=input("Which or all?> ")
        if file=="all":
            actions.find("all")
        else:
            row=actions.find(file)
            if row==0:
                print("Not found")
                return
            actions.show(row)

    def update(self):
        find=input("Which?> ")
        actions=Actions()
        row=actions.find(find)
        if row==0:
            print("Not found")
            return
        type=input("Type?> ")
        if type=="id":
            id=input("New id?> ")
            row=actions.find(id)
            if row!=0:
                print(id+" is already exists")
                return
            cur.execute('UPDATE files SET id=? WHERE id=?',(id,row[0]))
        elif type=="name":
            name=input("New name?> ")
            row=actions.find(name)
            if row!=0:
                print(name+" is already exists")
                return
            cur.execute('UPDATE files SET name=? WHERE id=?',(name,row[0]))
        elif type=="text":
            text=input("New text?> ")
            cur.execute('UPDATE files SET text=? WHERE id=?',(text,row[0]))
        elif type=="help":
            print("id")
            print("name")
            print("text")
            print("help")
            return
        else:
            print("No such type. Input help for type list.")
            return
        conn.commit()

    def delete(self):
        find=input("Which?> ")
        actions=Actions()
        row=actions.find(find)
        if row==0:
            print("Not found")
            return
        cur.execute('DELETE FROM files WHERE id=?',(row[0],))
        conn.commit()

    def help(self):
        print("create")
        print("retrieve")
        print("update")
        print("delete")
        print("quit")
        print("help")

dbname="files.db"
conn=sqlite3.connect(dbname)
cur=conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables=cur.fetchall()
exist=False
for table in tables:
    if table[0]=="files":
        exist=True
        break
if not exist:
    cur.execute('create table files(id STRING,name STRING,text STRING)')
actions=Actions()

while True:
    action=input("Action?> ")
    if action=="create":
        actions.create()
    elif action=="retrieve":
        actions.retrieve()
    elif action=="update":
        actions.update()
    elif action=="delete":
        actions.delete()
    elif action=="quit":
        break
    elif action=="help":
        actions.help()
    else:
        print("No such action. Input help for command list.")

cur.close()
conn.close()