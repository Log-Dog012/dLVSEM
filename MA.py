import os
import pandas as pd

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.ppm', '.pgm', '.pbm')
def MakeAnno(dir,label):
    names=[]
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(IMAGE_EXTENSIONS):
                names.append(entry.name)
##            elif entry.is_dir():
##                subdir_path = os.path.join(dir, entry.name)
##                MakeAnno(subdir_path, label)# 不够智能
    df=pd.DataFrame({'name':names})
    df['label'] = label
    if not df.empty:
        df.to_csv(os.path.join(dir,'annotation.csv'))

def MakeAnno_2(dir,key):
    names=[]
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(IMAGE_EXTENSIONS):
                names.append(entry.name)
            elif entry.is_dir():
                subdir = os.path.join(dir, entry.name)
                MakeAnno_2(subdir, key)
    df=pd.DataFrame({'name':names})
    g=lambda x:key(os.path.basename(dir),x)
    df['label'] = df['name'].apply(g)
    if not df.empty:
        df.to_csv(os.path.join(dir,'annotation.csv'))

def test():
    MakeAnno('Test','test')
    df=pd.read_csv('Test/annotation.csv')
    print(df)

def main():
    import sys
    if '-l'==sys.argv[-1]:
        if len(sys.argv)==3:
            dir=sys.argv[1]
        elif len(sys.argv)==2:
            dir=os.getcwd()
            temp=input(f'{dir=}?(No input means confirmation.)')
            if temp:
                dir=temp
        else:
            raise ValueError
        f=input('label function,for example\nlambda dirname,filename:filename[:3]')
        if f:
            import re
            if f.startswith('lambda') and not (';' in f):
                f=eval(f)
        else:
            raise ValueError
        MakeAnno_2(dir,f)
    else:
        if len(sys.argv)==3:
            dir,label=sys.argv[1:3]
        elif len(sys.argv)==2:
            dir=sys.argv[1]
            label=os.path.basename(dir)
            temp=input(f'{label=}?(No input means confirmation.)')
            if temp:
                label=temp
        elif len(sys.argv)==1:
            dir=os.getcwd()
            temp=input(f'{dir=}?(No input means confirmation.)')
            if temp:
                dir=temp
            label=os.path.basename(dir)
            temp=input(f'{label=}?(No input means confirmation.)')
            if temp:
                label=temp
        else:
            raise ValueError
        MakeAnno(dir,label)

## if __name__=='__main__':
##     test()

if __name__=='__main__':
    main()