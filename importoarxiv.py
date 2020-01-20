#!/usr/bin/python
import os
import shutil
from latexcreation import templates,writetemp

def movefig(figdirpath,arxivdirpath,figtype,lines):
    (searfig,zlist)=searchbeginline('\\includegraphics', lines)
    for root,dirs,files in os.walk(figdirpath):
        for name in files:
            names=name.split('.')
            if names[1] in figtype:
                spath=os.path.join(root,name)
                dpath=os.path.join(arxivdirpath,'fig',name)
                if not os.path.exists(os.path.join(arxivdirpath,'fig')):
                    os.mkdir(os.path.join(arxivdirpath,'fig'))
                fig=open(dpath,'wb')
                shutil.copy(spath,dpath)
                fig.close()
                for z in zlist:
                    if lines[z].find(name)!=-1:
                        lines[z]=lines[z][0:lines[z].find(name)]+'fig/'+lines[z][lines[z].find(name):]
    return lines




def changetitle(title):
    chartable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for a in range(0, len(title)):
        if not title[a] in chartable:
            title = title.replace(title[a], '')
    return title

def importtemps(mainpath,path):
    if not os.path.exists(path):
        os.mkdir(path)
    title = input('pls insert paper name')
    tp1 = templates('main.tex', mainpath)
    tp2 = templates('math_commands.tex', mainpath)
    tp3 = templates('neurips_2019.sty', mainpath)
    tp1.loading(path)
    tp2.loading(path)
    tp3.loading(path)
    template = os.path.join(path, tp1.name)
    return template, title

def searchbeginline(beginline,lines):
    searchbl=0
    z=[]
    for line in lines:
        if line[0:len(beginline)]==beginline:
            searchbl=1
            z.append(lines.index(line))
    return (searchbl,z)


def lineindexorder(num):
    indexorder = int(num)
    return indexorder

def eqcropping(linecrops,beginline,endline,ftype,dtype):
    remadesectioncrops=[]
    eqcrops=[]
    eqnamelist = []
    print('~~~~~~'+dtype + ' are as follows:')
    b=1
    for linecrop in linecrops:
        lines=linecrop[0]
        name=linecrop[1]
        remadesectioncrop=[]
        if searchbeginline(beginline,lines)[0] ==1:
            print('~~~~'+name+' :')
        #for beginline in beginlines:
        while searchbeginline(beginline,lines)[0] ==1 :
            eqbeginpoint=min(searchbeginline(beginline,lines)[1])
            eqendpoint=min(searchbeginline(endline,lines)[1])
            eqcropofsec=lines[eqbeginpoint:eqendpoint+1]
            eqname=str(b)+'_'+ftype+'.tex'
            importeqs=['\\input{'+str(dtype)+'/'+eqname+'}\n']
            remadesectioncrop = remadesectioncrop + lines[0:eqbeginpoint]+importeqs
            b=b+1
            lines=lines[eqendpoint+1:]
            print (eqname)
            eqcrops.append((eqcropofsec,eqname))
        remadesectioncrop=remadesectioncrop+lines
        #filecreate(path, eqcrops, ftype)
        remadesectioncrops.append((remadesectioncrop,name))
    return (eqcrops,remadesectioncrops)

def seccrop(lines):
    linecrops=[]
    lineindexlist=[]
    for line in lines:
        #print(line,lines.index(line))
        if line[0:16] == '\\begin{abstract}'or line[0:16] =='\\begin{Abstract}':
            lineindexlist.append(lines.index(line))
        elif line[0:14] =='\\end{Abstract}' or line[0:14]=='\\end{abstract}':
            lineindexlist.append(lines.index(line))
        elif line[0:8]=='\\section':
            lineindexlist.append(lines.index(line))
        elif line[0:18]=='\\begin{thebibliogr' or line[0:19]=='\\bibliographystyle{':
            lineindexlist.append(lines.index(line))
    lineindexlist.sort(key=lineindexorder)
    #print(lineindexlist)
    filename=lines[lineindexlist[0]]
    filename = '0_'+filename[filename.find('{') + 1:filename.find('}')]+'.tex'
    print('~~~~~sections are as follows:')
    print(filename)
    linecrops.append((lines[lineindexlist[0]:lineindexlist[1]+1], filename))
    #print (linecrops[0])
    b=2
    while b < len(lineindexlist)-1:
        filename=lines[lineindexlist[b]]
        filename=str(b-1)+'_'+filename[filename.find('{')+1:filename.find('}')]+'.tex'
        filename=filename.replace(' ','')
        print(filename)
        linecrops.append((lines[lineindexlist[b]:lineindexlist[b+1]],filename))
        b=b+1
        #print (linecrops[b-1])
    return linecrops

def filecreate(path,linecrops,dtype):
    folderpath=os.path.join(path,dtype)
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
    for linecrop in linecrops:
        file=open(os.path.join(folderpath,linecrop[1]),'w')
        file.writelines(linecrop[0])
        file.close()




