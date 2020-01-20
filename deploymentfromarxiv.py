#!/usr/bin/python
import os
import shutil
from __init__ import folder
class files:
    def __init__(self,path,name):
        self.path=path
        self.num=int(name.split('_')[0])

def movefile(path1,path2,dir,dtype):
    filefolder=folder(os.path.join(path1,dir))
    path3 = os.path.join(path2, dir)
    if not os.path.exists(path3):
        os.mkdir(path3)
    filelist=filefolder.folderreorder()
    print(filelist)
    filenums=eval('['+input('~~~~~pls insert the number of which u wanna deploy of '+dir+ '; if u wanna deploy all file, pls insert -1')+']')
    if -1 in filenums:
        for file in filelist:
            spath=os.path.join(path1,dir,file)
            #print(spath)
            dpath=os.path.join(path3,file)
            #print(dpath)
            try:
                open(dpath,dtype)
                shutil.copy(spath,dpath)
            except Exception:
                continue
    else:
        for file in filelist:
            fp=files(os.path.join(path1,dir,file),file)
            if fp.num in filenums:
                spath = fp.path
                dpath = os.path.join(path3, file)
                try:
                    open(dpath,dtype)
                    shutil.copy(spath,dpath)
                except Exception:
                    continue



