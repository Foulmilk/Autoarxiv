import os
def add_path():
    this_dir=os.path.dirname(__file__)
    return this_dir
class folder:
    def __init__(self,path):
        self.path=path
    def folderreorder(self):
        filelist=os.listdir(self.path)
        def order(file):
            order=int(file.split('_')[0])
            return order

        for file in filelist:
            if file.find('.tex') == -1:
                filelist.remove(file)
            else:
                try:
                    order(file)
                except Exception:
                    filelist.remove(file)
        filelist.sort(key=order)
        return filelist




