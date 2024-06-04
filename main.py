from src import system
from src import action

system.init()
while True:
    print()
    try:
        command=input("Action?> ")
    except EOFError:
        print()
        system.close()
    system.fileexistance()
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
            items=action.wildcard(things[2:],True)
            action.create(things[1],items)
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="retrieve":
        if num==1:
            action.showall()
        elif num>=3:
            if things[1]=="-i":
                items=things[2:]
            elif things[1]=="-p":
                items=action.wildcard(things[2:])
            else:
                print("No such action. Input help for command list.")
                continue
            action.retrieve(things[1],items)
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="update":
        if num==4:
            if things[1]=="-i":
                item=[things[2]]
            elif things[1]=="-p":
                item=action.wildcard([things[2]])
                if len(item)>1:
                    print("You cannot update multiple files at once.")
                    continue
            else:
                print("No such action. Input help for command list.")
                continue
            action.update(things[1],item[0],things[3])
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="delete":
        if num>=3:
            if things[1]=="-i":
                items=things[2:]
            elif things[1]=="-p":
                items=action.wildcard(things[2:])
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