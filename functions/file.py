def read(path):
    try:
        f=open(path,'r')
    except OSError:
        print("No such file or directory.")
        return 0
    else:
        text=f.read()
        f.close()
        return text