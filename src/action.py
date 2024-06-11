from src import db
from src import file
from src import system
from pathlib import Path
import os
import glob
import fnmatch
import shutil
import datetime
import unicodedata

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
    items=sorted(list(set(items)))
    returnitems=[]
    for item in items:
        if system.casesensitive:
            returnitems.append(item)
        else:
            returnitems.append(item.lower())
    return returnitems

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
            overwrite=input(id+" is already exist. Do you want to overwrite (Y/n)?> ")
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
        print(relpath(path)+" is already exist.")
        return None
    if not os.path.exists(item):
        print("Not found: "+relpath(item))
        return None
    return abspath(item)

def create(idtype,items):
    selected=False
    idtype=str(idtype).upper()
    if len(idtype)>1:
        idnum=int(idtype[1:])
        idtype=idtype[0]
        selected=True
    else:
        idnum=1
    id=idtype+str(idnum)
    i=0
    for item in items:
        i+=1
        j=0
        while findid(id):
            j+=1
            if i==1 and j==1 and selected:
                print(id+" is already exist.")
            idnum+=1
            id=idtype+str(idnum)
        path=creatable(item)
        if path!=None:
            db.create(id,path)
            print(relpath(path)+" is created as \""+id+"\".")
    return

def showall():
    cur=db.all()
    for row in cur:
        print("id: "+row[0]+"\t\tpath: "+relpath(row[1]))
    return

def retrieve(option,items,show=False):
    wholetext=""
    for item in items:
        path=findpath(option,item)
        if path==None or path==0:
            return None
        text=file.read(path)
        wholetext+=text
        if show:
            print(text)
    return wholetext

def update(option,item,id):
    path=findpath(option,item)
    if path==None or path==0:
        return
    id=str(id).upper()
    id=id[0]+str(int(id[1:]))
    row=find(id)
    if path==row:
        print("Nothing changed.")
        return
    if row!=None:
        overwrite(id,row)
    db.update(id,path)
    print("Update complete.")
    return

def delete(option,items):
    for item in items:
        path=findpath(option,item)
        if path==None or path==0:
            continue
        db.delete(path)
    print("Delete complete.")
    return

def zenlen(text):
    count=0
    for c in text:
        if unicodedata.east_asian_width(c) in "FW":
            count+=2
        else:
            count+=1
    return count

RED='\033[31m'#red
GREEN='\033[32m'#green
YELLOW='\033[33m'#yerrow
BLUE='\033[34m'#blue
RESET='\033[0m'#reset

def wordtoken(option,items,token):
    text=retrieve(option,items)
    if text==None:
        return
    token=" "+token.lower()+" "
    long=len(token)
    tokenlist=token.split()
    tokenlistlong=len(tokenlist)
    characters=200
    lowertext=text.lower()
    start=0
    width=shutil.get_terminal_size().columns
    result=""
    while True:
        start=lowertext.find(token,start+1)
        if start==-1:
            break
        aftersurround="".join(c for c in text[start:start+long+characters] if c.isprintable())
        aftersurroundlist=aftersurround.split()[tokenlistlong:-1]
        if len(aftersurroundlist)>10:
            aftersurroundlist=aftersurroundlist[:10]
        if len(aftersurroundlist)>0:
            aftersurroundlist[0]=BLUE+aftersurroundlist[0]+RESET
        if len(aftersurroundlist)>1:
            aftersurroundlist[1]=GREEN+aftersurroundlist[1]+RESET
        if len(aftersurroundlist)>2:
            aftersurroundlist[2]=RED+aftersurroundlist[2]+RESET
        while True:
            aftersurroundword=""
            for word in aftersurroundlist:
                aftersurroundword+=word+" "
            if len(aftersurroundword)<int(width/2-long/2):
                aftersurroundword=aftersurroundword[:-1]
                break
            else:
                aftersurroundlist=aftersurroundlist[:-1]
        beforesurround="".join(c for c in text[start-characters:start] if c.isprintable())
        beforesurroundlist=beforesurround.split()[1:]
        if len(beforesurroundlist)>=10:
            beforesurroundlist=beforesurroundlist[-10:]
        while True:
            beforesurroundword=""
            for word in beforesurroundlist:
                beforesurroundword+=word+" "
            if len(beforesurroundword)<int(width/2-long/2):
                beforesurroundword=beforesurroundword[:-1]
                break
            else:
                beforesurroundlist=beforesurroundlist[1:]
        for i in range(int(width/2)-zenlen(beforesurroundword)-int(long/2)):
            beforesurroundword=" "+beforesurroundword
        resultline=beforesurroundword+YELLOW+token+RESET+aftersurroundword
        print(resultline)
        result+=resultline+"\n"
    if system.casenum==None:
        system.casenum=1
    else:
        system.casenum+=1
    casestr=str(system.casenum).zfill(6)
    now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    y=str(now.year)
    mo=str(now.month).zfill(2)
    d=str(now.day).zfill(2)
    h=str(now.hour).zfill(2)
    mi=str(now.minute).zfill(2)
    s=str(now.second).zfill(2)
    micro=str(now.microsecond).zfill(6)
    path="./results/"+casestr+"-"+y+mo+d+"-"+h+mi+s+"-"+micro+"-"
    for part in tokenlist:
        path+=part+" "
    path=path[:-1]+".txt"
    file.write(path,result)
    return

def hyphenation(texts):
    width=int(shutil.get_terminal_size().columns/len(texts))
    alllen=0
    for text in texts:
        alllen+=zenlen(text)
    output=""
    while alllen:
        for i in range(len(texts)):
            space=""
            if zenlen(texts[i])>width-1:
                output+=texts[i][:width-2]+"- "
                texts[i]=texts[i][width-2:]
                alllen-=(width-2)
            else:
                while zenlen(texts[i])+len(space)<width:
                    space+=" "
                output+=texts[i]+space
                alllen-=zenlen(texts[i])
                texts[i]=""
        output+="\n"
    return output[:-1]

def compare(option,questioned,known):
    qtext=retrieve(option,questioned)
    ktext=retrieve(option,known)
    if qtext==None or ktext==None:
        return
    qtext="".join(c for c in qtext if c.isprintable())
    qtext=qtext.split()
    qdict={}
    for word in qtext:
        if word in qdict:
            qdict[word]+=1
        else:
            qdict[word]=1
    qdict=sorted(qdict.items(),key=lambda x:x[1],reverse=True)
    qmax=len(qdict)-len(qdict)%20
    ktext="".join(c for c in ktext if c.isprintable())
    ktext=ktext.split()
    kdict={}
    for word in ktext:
        if word in kdict:
            kdict[word]+=1
        else:
            kdict[word]=1
    kdict=sorted(kdict.items(),key=lambda x:x[1],reverse=True)
    kmax=len(kdict)-len(kdict)%20
    max=qmax if qmax<kmax else kmax
    questioned=questioned[0].upper() if option=="-i" else relpath(questioned[0])
    known=known[0].upper() if option=="-i" else relpath(known[0])
    output=hyphenation([questioned,known])
    for i in range(max):
        output+=hyphenation([qdict[i][0],kdict[i][0]])
        if i%20==19:
            print(output)
            if i!=max-1:
                while True:
                    try:
                        showmore=input("Just push enter to show 20 words more. Push q and enter to quit> ")
                    except EOFError:
                        system.close()
                    else:
                        if showmore=="q" or showmore=="Q":
                            return
                        elif showmore=="":
                            break
    return

def help():
    print(file.read(".help.txt"))