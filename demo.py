import os
import shutil
from __init__ import add_path,folder
from latexcreation import makelatexdir,writetemp,templates
from deploymentfromarxiv import movefile
from importoarxiv import importtemps,searchbeginline,lineindexorder,eqcropping,seccrop,filecreate,movefig
from bblcreation import citelist,citextraction,bibcrop,bibitemcreate,makebblfile

def makefile(linecrops,path):
    # extracts equations, tables, and algorithms from latex file and remakes latexfile by sections
    enr = eqcropping(linecrops, '\\begin{equation}\n', '\\end{equation}\n', 'eq', 'equations')
    tnr = eqcropping(enr[1], '\\begin{table', '\\end{table', 'table', 'tables')
    anr = eqcropping(tnr[1], '\\begin{algo', '\\end{algo', 'algorithm', 'algorithms')
    #write equations, tablies, algorithms, and sections into different tex file
    filecreate(path, enr[0], 'equations')
    print ('~~~~~equations have been imported to '+os.path.join(path,'equations'))
    filecreate(path, tnr[0], 'tables')
    print('~~~~~tables have been imported to ' + os.path.join(path, 'tables'))
    filecreate(path, anr[0], 'algorithms')
    print('~~~~~algorithms have been imported to ' + os.path.join(path, 'algorithms'))
    filecreate(path, tnr[1], 'sections')
    print('~~~~~sections have been imported to ' + os.path.join(path, 'sections'))
    #imports arxiv template and style file
    (template, title) = importtemps(mainpath, path)
    sectionfolder = folder(os.path.join(path, 'sections'))
    filenames = sectionfolder.folderreorder()
    #input title, authors, authors' infomation, and sections into imported arxiv template
    writetemp(template, title, filenames)
    return template,title,filenames#

def writeeqs(path,types):
    #this function is to write \begin, \label, and \end order of latex into blank flie of equations, tables, and algorithms.
    eqlist = os.listdir(os.path.join(path, types[0]))
    for eq in eqlist:
        eqfile = open(os.path.join(path, types[0], eq), 'w')
        eqnum = eq.split('_')
        eqnum = eqnum[0]
        if types[0] == 'equations':
            eqfile.write('\\begin{'+types[1]+'}\n\\begin{aligned}\n\\label{' + types[1]+str(eqnum) + '}\n%write '+types[1]+' here\n\\end{aligned}\n\\end{'+types[1]+'}')
        else:
            eqfile.write(
                '\\begin{' + types[1] + '}\n\\label{' + types[1] + str(eqnum) + '}\n%write ' + types[
                    1] + ' here\n\\end{' + types[1] + '}')
        eqfile.close()

if __name__=='__main__':
    mainpath = add_path()
    #we have four tasks, choose one
    task_index=int(input('pls choose task:\n[0] generate a blank arxiv folder.\n[1] Generate an arxiv latex folder according to your other template.\n[2] deploy your other template folder with your arxiv file.\n[3] Create .bbl file according your .bib file and .tex file'))
    #this task is to make a blank arxiv template folder, for an article without any latex file.
    if task_index==0:
        path = input('pls insert your arxiv directory path')
        (template,title)=importtemps(mainpath,path)
        makelatexdir(path,template,title)
        typelist=[('equations','equation'),('tables','table'),('algorithms','algorithm')]
        for types in typelist:
            writeeqs(path,types)
    #this task is to generate an arxiv template folder from a latex folder with other template. It can extract all figures, equations, tables, algorithms, and sections from a latex file, and put them into different files and folders. Also it can generate a .bbl file according to the latex file and .bib file (for arxiv only accept .bbl file)
    elif task_index==1:
        path1=input('pls insert your latex project path:')
        path3 = input('pls insert your .tex file name or your sections folder name:')
        path=os.path.join(path1,path3)
        if not os.path.exists(path):
            print('~~~~~cannot find your latex file.')
            quit()
        path2 = input('pls insert your arxiv folder path:')
        bblname = input('pls insert the name of .bbl file:')
        bibpath = input('pls insert the path of .bib file:')
        if not os.path.exists(path2):
            os.mkdir(path2)
        linecrops=[]
        figtype = ['png', 'jpg', 'jpeg', 'tiff', 'pdf']
        print('~~~~~Figure types are as follows: ')
        print(figtype)
        extrafigtype = input('~~~~~if the type of your figs are not in figure types,please insert the type:')
        # if not your figures' type in the list, you can insert yours.
        figtype.append(extrafigtype)
        if path.find('.tex')!=-1:
            file = open(path, 'r')
            lines = file.readlines()
            lines=movefig(path1,path2,figtype,lines)
            linecrops = seccrop(lines)
        else:
            sectionfolder=folder(path)
            filelist=sectionfolder.folderreorder()
            print ('~~~~~sections are as follows:')
            i=0
            while i < len(filelist):
                print(filelist[i])
                i=i+1
            for filename in filelist:
                file=open(os.path.join(sectionfolder.path,filename),'r')
                linecrop=(file.readlines(),filename)
                linecrop=movefig(path1,path2,figtype,linecrop)
                linecrops.append(linecrop)
        #extract all figures from your old latex folder and put them into new 'fig' folder. The latex file will import figures automatically.
        print('~~~~~figures has been imported to ' + os.path.join(path2, 'fig'))
        fileinfo=makefile(linecrops,path2)
        sectionspath = os.path.join(path2,'sections')
        sectionlist=[]
        for linecrop in linecrops:
            sectionlist.append(linecrop[1])
        citeindex = citextraction(sectionlist,sectionspath,0)
        makebblfile(path2, bibpath, citeindex, bblname)
        template=fileinfo[0]
        tpfile=open(template,'r')
        tplinelist=tpfile.readlines()
        tpfile=open(template,'w')
        z=searchbeginline('%\\input{refs.bbl}',tplinelist)[1]
        z=z[0]
        tpfile.writelines(tplinelist[0:z]+['\\input{'+bblname+'}\n']+tplinelist[z+1:])
        tpfile.close()



    elif task_index == 2:
        #this task can help you update your latex file using other templates with your arxiv folder.
        path1 = input('~~~~~pls insert the path of your arxiv dir')
        if not os.path.exists(path1):
            print(path1+' not exist')
        path2 = input('~~~~~pls insert the path of your other template dir')
        if not os.path.exists(path2):
            os.mkdir(path2)
        typelist = ['fig', 'sections', 'equations', 'algorithms', 'tables']
        typenums = eval('[' + input(
            '~~~~~pls select the number of which type u wanna deploy:fig(0),sections(1),equations(2),algorithms(3),tables(4)') + ']')
        for typenum in typenums:
            if typenum == 0:
                figlist=os.listdir(os.path.join(path1,'fig'))
                for fig in figlist:
                    spath=os.path.join(path1,'fig',fig)
                    dpath=os.path.join(path2,'fig')
                    if not os.path.exists(dpath):
                        os.mkdir(dpath)
                    dpath = os.path.join(dpath,fig)
                    open(dpath,'wb')
                    shutil.copy(spath,dpath)

            else:
                dtype = 'w'
                dir = typelist[typenum]
                movefile(path1, path2, dir, dtype)
    elif task_index == 3:
        #this task is to generate a .bbl file according to your latex file and .bib file.
        sectionspath = input('~~~~~pls insert the path of sections or the path of your .tex file')
        bblpath = input('~~~~~pls insert the path where u wanna save the .bbl file')
        bblname = input('~~~~~pls insert the name of .bbl file')
        bibpath = input('~~~~~pls insert the path of bib file')
        sectionlist = []
        if sectionspath.find('.tex') == -1:
            sectionsfolder = folder(sectionspath)
            sectionlist = sectionsfolder.folderreorder()
            pathk = 0
        else:
            sectionlist = sectionspath[sectionspath.find('/') + 1:]
            pathk = 1
        citeindex = citextraction(sectionlist,sectionspath, pathk)
        makebblfile(bblpath, bibpath, citeindex, bblname)
    else:
        print ('~~~~~no this choose')

    print ('~~~~~Finish Task '+str(task_index))