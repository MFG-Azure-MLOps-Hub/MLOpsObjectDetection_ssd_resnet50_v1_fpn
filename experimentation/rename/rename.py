import os
def rename():
    count = 0
    path='C:/Users/bwa/Desktop/MSLogoImages'
    filelist=os.listdir(path)
 
    for files in filelist:
        Olddir=os.path.join(path,files)
        if os.path.isdir(Olddir):
            continue
        # 重命名
        name=str(count)
        while len(name)<6:
            name='0'+name
        name=name+'.jpg'
 
        Newdir=os.path.join(path,name)
        os.rename(Olddir,Newdir)
        count+=1
 
rename()