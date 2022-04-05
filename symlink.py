import os
import shutil
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    #takes absolute path of r2modman plugins folder
    masterpath = input("enter absolute path to r2 modman plugins folder\n")
    childpath = []
    while True:
        x = input("enter paths to the plugins folder of the profile to be replaced or type \"exit\" to stop adding\n")
        if x.lower() == "exit":
            break
        #checks input for path to be replaced isn't child path - makes sure not to link profile to itself
        elif x != masterpath:
            childpath.append(x)
        else:
            print("invalid input")

    #creates list of files in master directory
    masterlist = []

    #iterates over every directory in the master path specified and adds it to masterlist
    for i in os.listdir(masterpath):
        masterlist.append(i)

    #iterates over every directory name given
    for i in range(len(childpath)):
        templist = []

        #iterates over every directory in the childpath at parent loop, adds files to templist
        for j in os.listdir(childpath[i]):
            templist.append(j)

        #iterates over every directory name in masterlist  
        for k in range(len(masterlist)):
            #checks if the current directory is also in the profile to be replaced
            if masterlist[k] in templist:
                #checks if file is already a symlink - if it is already a symlink it is ignored
                if os.path.islink(childpath[i]+"\\"+masterlist[k]) == False:
                    #deletes current mod folder in the profile being replaced
                    shutil.rmtree(childpath[i]+"\\"+ masterlist[k])
                    #creates symlink
                    os.symlink(f"{masterpath}\{masterlist[k]}",f"{childpath[i]}\{masterlist[k]}")
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            
