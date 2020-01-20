# Autoarxiv
It's a python program help to make a latex folder for arxiv. You can make a new blank folder with template and folders of sections, equations, tables, algorithms, and figures. Also you can generate a folder for arxiv according to your own latex folder. Also it can generate a .bbl file without latex compiler due to demand of arxiv for reference (only .bbl but not .bib)
I use nips_2019's template as the template for arxiv and make some mark in the template for run my script. All sections, equations, algorithms, and tables will be in different folders, and can be iputted into latex file by \input. Figures will be in 'fig' folder. 
To run the script, you just need to run the demo.py.
When choose task 0, you can make a blank arxiv folder for your article (if you don't have a latex file yet). You just need to input your arxiv folder path, sections' titles, authors (use comma to seperate authors, don't use ' ' between two different authors), authors' emails and affliations, and amount of your equations, tables, and algorithms. Then an blank arxiv folder would be generated, and the template would be filled in. This task cannot make a .bbl file, which can be made in task 1 and task 3.
When choose task 1, you can make an arxiv file from your own latex folder. It can extract all sections, equations, tables, algorithms, and figures from a .tex file or a folder of .tex files. Your input should be:
pls insert your latex project path:/Users/username/Desktop/yourlatexfolder (your old latex folder's path)
pls insert your .tex file name or your sections folder name:yourtexfile.tex or yoursectionsfoldername(without path, only the name of sections' folder)
pls insert your arxiv folder path:/Users/yourname/Desktop/somgantest2 (your new arxiv latex folder path, it can be made automatically)
pls insert the name of .bbl file: refs.bbl (only the name of the .bbl file you wanna make)
pls insert the path of .bib file: path of your .bib file, which you can put anywhere but other computer.
['png', 'jpg', 'jpeg', 'tiff', 'pdf']
if the type of your figs are not in figure types,please insert the type: as what it asks, if you have a pdf fomat figure, you can input 'pdf'.
Other inputs are same with task 0.
When choose task 2, you can deploy two latex folders if only they have same folders tree (actually like arxiv folder made by this script). You should input your source folder path and your destination folder path. And then you can choose which folder and which file you wanna deploy. Specifically, when choose foders and files, you can input numbers with comma to seperate, like '0,1,2,3,4'.
When choose task 3, you can generate a .bbl file and save it to a path according to your .tex file and your .bib file. You should input your .tex file's path or folder of sections' path. When you input a folder of sections, you should rename your .tex file of sections with 'number_' at beginning, like '1_Introduction', or the script cannot find right order of citations.
