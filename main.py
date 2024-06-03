from src import system
from src import action
from src import file
import glob

system.init()
while True:
    print()
    try:
        command=input("Action?> ")
    except EOFError:
        system.close()
    file.existancecheck()
    if system.casesensitive:
        commands=command.split()
    else:
        commands=command.lower().split()
    things=[]
    thing=""
    for i in range(len(commands)):
        if commands[i][-1]=="\\":
            if i==len(commands)-1:
                thing+=commands[i][:-1]+" "
                things.append(thing)
                thing=""
            else:
                thing+=commands[i][:-1]+" "
        else:
            thing+=commands[i]
            things.append(thing)
            thing=""
    num=len(things)
    if num==0:
        continue
    if things[0]=="create":
        if num>=3:
            items=[]
            for item in things[2:]:
                found=glob.glob(item)
                if len(found)==0:
                    items.append(item)
                items.extend(found)
            items=list(set(items))
            action.create(things[1],items)
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="retrieve":
        if num==1:
            action.showall()
        elif num==3:
            action.retrieve(things[1],things[2])
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="update":
        if num==4:
            action.update(things[1],things[2],things[3])
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="delete":
        if num>=3:
            items=[]
            if things[1]=="-i":
                for item in things[2:]:
                    items.append(item)
            elif things[1]=="-p":
                for item in things[2:]:
                    found=glob.glob(item)
                    if len(found)==0:
                        items.append(item)
                    items.extend(found)
                items=list(set(items))
            else:
                print("No such action. Input help for command list.")
                continue
            action.delete(things[1],items)
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="quit":
        break
    elif things[0]=="help":
        action.help()
    else:
        print("No such action. Input help for command list.")
system.close()