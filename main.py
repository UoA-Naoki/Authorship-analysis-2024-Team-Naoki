from src import system
from src import action
import unicodedata

system.init()
while True:
    print()
    try:
        command=input("Action?> ")
    except EOFError:
        print()
        system.close()
    system.dbexistance()
    system.fileexistance()
    command=unicodedata.normalize("NFKC",command)
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
    if things[0]=="create" and num>2:
        things[1]=things[1].upper()
        if things[1][0]!="Q" and things[1][0]!="K" and things[1][0]!="R":
            print("No such action. Input help for command list.")                
        elif len(things[1])>1 and not things[1][1:].isdecimal():
            print("No such action. Input help for command list.")                
        else:
            items=action.wildcard(things[2:],True)
            action.create(things[1],items)
    elif things[0]=="retrieve":
        if num==1:
            action.showall()
        elif num>2:
            if things[1]=="-i":
                items=things[2:]
            elif things[1]=="-p":
                items=action.wildcard(things[2:])
            else:
                print("No such action. Input help for command list.")
                continue
            action.retrieve(things[1],items,True)
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="update" and num==4:
        things[3]=things[3].upper()
        if (things[3][0]!="Q" and things[3][0]!="K" and things[3][0]!="R") or not things[3][1:].isdecimal():
            print("No such action. Input help for command list.")
        else:
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
    elif things[0]=="delete" and num>2:
        if things[1]=="-i":
            items=things[2:]
        elif things[1]=="-p":
            items=action.wildcard(things[2:])
        else:
            print("No such action. Input help for command list.")
            continue
        action.delete(things[1],items)
    elif things[0]=="search":
        if num>4:
            if things[1]+things[2]=="wordtoken":
                for i in range(len(things[3:])):
                    if things[i+3]=="-i":
                        items=things[i+4:]
                        break
                    elif things[i+3]=="-p":
                        items=action.wildcard(things[i+4:])
                        break
                token=""
                for word in things[3:i+3]:
                    token+=word+" "
                token=token[:-1]
                action.wordtoken(things[i+3],items,token)
            elif things[1]=="lemma":
                print("Not implemented yet.")
            elif things[1]=="pos":
                print("Not implemented yet.")
            elif things[1][-4:]=="gram":
                print("Not implemented yet.")
            elif things[1]=="regex":
                print("Not implemented yet.")
            else:
                print("No such action. Input help for command list.")
        else:
            print("No such action. Input help for command list.")
    elif things[0]=="quit":
        break
    elif things[0]=="help":
        action.help()
    else:
        print("No such action. Input help for command list.")
system.close()