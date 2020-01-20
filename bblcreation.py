#!/usr/bin/python
import os
from __init__ import folder
def citelist(file):
    linelist=file.readlines()
    citelist=[]
    citelist1=[]
    for line in linelist:
        linepartionlist=line.split('\\cite{')
        linepartionlist.remove(linepartionlist[0])
        for linepartion in linepartionlist:
            b = linepartion.find('}')
            cite = linepartion[0:b]
            if cite.find(',')==-1:
                citelist.append(cite)
            else:
                cite=cite.split(',')
                citelist=citelist+cite
    file.close()
    return citelist

def citextraction(sectionlist,sectionspath,pathk):
    citeindex=[]
    citeindex1=[]
    for section in sectionlist:
        if pathk==0:
            file=open(os.path.join(sectionspath,section),'r')
        else:
            file=open(sectionspath,'r')
        citeindex1=citeindex1+citelist(file)
    for cite in citeindex1:
        if cite not in citeindex:
            citeindex.append(cite)
    print (citeindex)
    print(str(len(citeindex))+' citations.')
    return (citeindex)

def bibcrop(bibpath):
    bibfile=open(bibpath,'r')
    biblinelist=bibfile.readlines()
    biblinecropindex=[]
    for bibline in biblinelist:
        if bibline.find('@article')!=-1:
            a= biblinelist.index(bibline)
            biblinecropindex.append(a)
        elif bibline.find('@inproceedings')!=-1:
            a=biblinelist.index(bibline)
            biblinecropindex.append(a)
        elif bibline.find('@incollection')!=-1:
            a=biblinelist.index(bibline)
            biblinecropindex.append(a)
        elif bibline.find('@book')!=-1:
            a=biblinelist.index(bibline)
            biblinecropindex.append(a)
        else:
            continue
    biblinecropindex.sort()
    biblinecroplist=[]
    for index1 in biblinecropindex:
        if biblinecropindex.index(index1)<len(biblinecropindex)-1:
            biblinecrop=biblinelist[index1:biblinecropindex[biblinecropindex.index(index1)+1]]
            biblinecroplist.append(biblinecrop)
        else:
            biblinecrop = biblinelist[index1:]
            biblinecroplist.append(biblinecrop)
    return biblinecroplist

def bibitemcreate(bibslides):
    bibitem=bibslides[0].split('{')[1]
    bibitem=bibitem[0:-2]
    author=''
    booktitle=''
    title=''
    year=''
    url = ''
    pages = ''
    month = ''
    journal = ''
    publisher=''
    note=''
    series=''
    editor=''
    volume=''
    number=''
    address=''
    for bibslide in bibslides:
        if bibslide.find('author = {')!=-1:
            z = bibslide.find('{')
            author=bibslide[z+1:-3]
            authors = author.split(' and ')
            authorlist = []
            for name in authors:
                surname = name.split(', ')[0] + ','
                prename = name.split(', ')[1]
                prenames = prename.split(' ')
                prename2 = ''
                for prenamepartion in prenames:
                    prename2 = prename2 + prenamepartion[0:1].title() + '.' + '~'
                prename2 = prename2[0:-1] + ' '
                name = prename2 + surname
                authorlist.append(name)
            if len(authorlist) >1:
                authorlist.insert(-1,'and')
                author=' '.join(authorlist)+' '
            else:
                author=authorlist[0]+' '
        elif bibslide.find('booktitle = {')!=-1:
            z=bibslide.find('{')
            booktitle = '\\emph{'+bibslide[z+1:-3]+'}, '
        elif bibslide.find('shorttitle = {')!=-1:
            continue
        elif bibslide.find('title = {') != -1 and bibslide.find('shorttitle = {')==-1 and bibslide.find('booktitle = {')==-1:
            z = bibslide.find('{')
            title = '"'+bibslide[z+1:-3]+'," '
        elif bibslide.find('year = {') != -1:
            z = bibslide.find('{')
            year = bibslide[z + 1:-3]+', '
        elif bibslide.find('url = {') != -1:
            z = bibslide.find('{')
            url = '[Online]. Available: \\url{'+bibslide[z + 1:-3]+'}'
        elif bibslide.find('pages = {') != -1:
            z = bibslide.find('{')
            pages = 'pp. '+bibslide[z + 1:-3]+', '
        elif bibslide.find('month =') != -1:
            month = bibslide[-5:-2]
            month = month.title()+'. '
        elif bibslide.find('journal = {') != -1:
            z = bibslide.find('{')
            journal = '\emph{'+bibslide[z + 1:-3]+'}, '
        elif bibslide.find('publisher = {') != -1:
            z = bibslide.find('{')
            publisher = bibslide[z + 1:-3]+', '
        elif bibslide.find('note = {') != -1:
            z = bibslide.find('{')
            note = bibslide[z + 1:-3]+', '
        elif bibslide.find('series = {') != -1:
            z = bibslide.find('{')
            series = 'ser. '+bibslide[z + 1:-3]+', '
        elif bibslide.find('editor = {') != -1:
            z = bibslide.find('{')
            editor = bibslide[z + 1:-3]+', Eds.'
        elif bibslide.find('volume = {') != -1:
            z = bibslide.find('{')
            volume = 'vol.~'+bibslide[z + 1:-3]+', '
        elif bibslide.find('number = {') != -1:
            z = bibslide.find('{')
            number = 'no.~'+bibslide[z + 1:-3]+', '
        elif bibslide.find('address = {') != -1:
            z = bibslide.find('{')
            address = bibslide[z + 1:-3]+': '
    return (bibitem,author,booktitle,title, year, month, url,pages,journal,publisher,note,series,editor,volume,number,address)

def makebblfile(bblpath,bibpath,citeindex,bblname):
    if not os.path.exists(bblpath):
        os.mkdir(bblpath)
    bblfile = open(os.path.join(bblpath, bblname), 'w')
    bblfile.write('\\begin{thebibliography}{10}\n')
    bibcropping=bibcrop(bibpath)
    bibinfolist=[]
    for bibslides in bibcropping:
        bibinfo=bibitemcreate(bibslides)
        bibinfolist.append(bibinfo)
    for cite in citeindex:
        for bibinfo in bibinfolist:
            if bibinfo[0]==cite:
                ym1 = bibinfo[5] + bibinfo[4]
                ym2 = ''
                adandpub=''
                if bibinfo[2]=='':
                    ym2 = ym1
                    ym1 = ''
                if bibinfo[15]!='' or bibinfo[9]!='':
                    adandpub='\\hskip 1em plus 0.5em minus 0.4em\\relax '+bibinfo[15]+bibinfo[9]
                bblline='\\bibitem{'+bibinfo[0]+'}\n'+bibinfo[1]+bibinfo[3]+bibinfo[2]+bibinfo[8]+bibinfo[11]+bibinfo[13]+bibinfo[14]+bibinfo[12]+adandpub+ym1+bibinfo[7]+ym2+bibinfo[10]+bibinfo[6]+'\n'
                finalnum=int(bblline.rfind(','))
                bblline=list(bblline)
                bblline[finalnum]='.'
                bblline=''.join(bblline)
                bblfile.write(bblline)
                bibinfolist.remove(bibinfo)
    bblfile.write('\\end{thebibliography}')
    bblfile.close()
    print(bblname + ' has been generated at '+bblpath+'.' )



