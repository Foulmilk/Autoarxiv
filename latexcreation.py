#!/usr/bin/python
import os
import shutil

def writetemp(template,title,filenames):
    authorlist = input('pls insert authors with \',\' but not space to separate ')
    authorlist = authorlist.split(',')
    authorinfolist = []
    for author in authorlist:
        email = input('pls insert the email of ' + author)
        affiliation = input('pls insert the affliation of ' + author)
        if email.find('@') == -1:
            authorinfo = author + '\\thanks{' + affiliation + '}'
        else:
            authorinfo = author + '\\thanks{' + email + ', ' + affiliation + '}'
        authorinfolist.append(authorinfo)
    n = 0
    authorline = '\\author{'
    while n < len(authorinfolist) - 1:
        authorline = authorline + authorinfolist[n] + ', '
        n = n + 1
    authorline = authorline + authorinfolist[-1] + '}\n'
    titleline = '\\title{' + title + '}' + '\n'
    file1 = open(template, 'r')
    linelist = file1.readlines()
    p = linelist.index('\\title{}\n')
    n = linelist.index('\\author{}\n')
    m = linelist.index('%inputsectionshere\n')
    linelist[p] = titleline
    linelist[n] = authorline
    file1 = open(template, 'w')
    linelist_add = []
    for filename in filenames:
        linelist_add.append('\\input{sections/' + filename + '}\n')
    content1 = linelist[0:m + 1]
    content2 = linelist[m + 1:len(linelist)]
    file1.writelines(content1 + linelist_add + content2)
    file1.close()
    print ('title, authors, and sections have been imported into arxiv template.')

class templates():
    def __init__(self,name,mainpath):
        self.name=name
        self.path=os.path.join(mainpath,name)
    def loading(self,path):
        template = os.path.join(path,self.name)
        tpfile = open(template, 'w')
        shutil.copy(self.path, template)
        tpfile.close()
        print (self.name  +' has been loaded to '+path)
        return template

def makelatexdir (path,template,title):
    list = ['sections', 'fig','equations','tables','algorithms']
    for a in list:
        if not os.path.exists(os.path.join(path,a)):
            os.mkdir(os.path.join(path,a))
    sections=input('pls insert sections with \',\' without space to separate ')
    sectionlist=sections.split(',')
    if sectionlist==['']:
        sectionlist=[]
    try:
        eqnum = int(input('pls insert eqautions amount'))
    except Exception:
        eqnum=0
    try:
        tablenum = int(input('pls insert tables amount'))
    except Exception:
        tablenum=0
    try:
        algorithmnum=int(input('pls insert algorithm amount'))
    except Exception:
        algorithmnum=0
    dirtype = [('eq',eqnum), ('table',tablenum), ('algorithm',algorithmnum)]
    filenames=[]
    for section in sectionlist:
        section1=section.replace(' ','_')
        filename=str(sectionlist.index(section)+1)+'_'+section1+'.tex'
        file=open(os.path.join(path,'sections',filename),'w')
        file.close()
        filenames.append(filename)
    acknowledgement = open(os.path.join(path, 'sections', str(len(sectionlist)+1)+'_acknowledgement.tex'), 'w')
    acknowledgement.write('\\section*{Acknowledgements}')
    acknowledgement.close()
    writetemp(template,title,filenames)
    def makefile(dir):
        num=dir[1]
        dir2=dir[0]
        for number in range(1, num + 1):
            filename = str(number)+'_'+dir2 + '.tex'
            file = open(os.path.join(path, list[dirtype.index(dir)+2], filename), 'a+')
            file.close()
    for dir in dirtype:
        makefile(dir)







