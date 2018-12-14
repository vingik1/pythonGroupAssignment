import shutil
from pathlib import Path
import shutil
import os
import re

def createInsert(pattern, filename, file_path, target):
    #if there is no pattern add the file to a directory called unsorted
    if pattern == "":
        folder_path = str(file_path).split('\\',1)[1]
        print(folder_path)
        try:
            Path(target+"\\Unsorted\\"+folder_path).parent.mkdir(parents=True,exist_ok=True)
        except:
            print("'"+filename+"' already exists. skip")
        try:
            shutil.copy(file_path,Path(target+"\\Unsorted\\"+folder_path))
        except:
            print(str(file_path)+" Was not found")
        return
    season = ""
    print(file_path)
    #creates the number  
    number = re.search(pattern,filename).group()
    for j in number:
        if re.match("[sS]",j):
            continue
        #athuga pattern-ið!!!!
        elif re.match("[sSeEx ]",j):
            if len(season) == 1:
                season = '0'+season
            break
        else:
            season += j
    print(number[1])
    #temp splitar svo hægt sé að fá nafnið á þá fyrir folder
    temp = re.split(pattern,filename)
    series_name = temp[0]
    full_path = str(file_path).replace('\\','  ')

    if re.search("( |^)\d{3}([.| ])",filename):
        season = '0'+number[1]
        print(series_name+" 1")

    if series_name.endswith(' '):
        spaces = re.search(r"\s{1,}$",series_name).group()
        series_name = series_name[:-len(spaces)]
        print(series_name+" 2")
    #if the file does not contain the name of show within then a regex search back for the given
    # regex if its in a folder whcih has either Seasons, series or just number the get the name 
    #from folder which it is in
    elif series_name == '' :#and re.search("[Ss]eason[.| ]\d{1,2}|[Ss]eries [ -|]{0,1} \d{1,2}| \d{1,2} ",full_path):
        series_name = full_path.split('  ',2)[1]
        print( full_path.split(' ',2))
        print(series_name +" 3")
    
    series_name = series_name.title()
    #foundName = True
    try:
        #býr til folder með nafninu á folderinu !!!þarf að laga !!!!!
        Path(target+"\\"+series_name).mkdir()
    except:
        #lætur vit ef þegar til
        #pass
        print("'"+series_name+"' already exists. skip")
    try: 
        #býr svo til season 01 etc eftir nafninu á file-num
        Path(target+"\\"+series_name+"\\Season "+season).mkdir()
    except:
        #pass
        print("'"+series_name+"\\Season "+season+"' already exists. skip")
    try:
        shutil.copy(file_path,Path(target+"\\"+series_name+"\\Season "+season))
    except:
        #pass
        print(str(file_path)+" Was not found")
    return 'success'


def clean(downloads, target):
    try:
        #creates a directory with the given name if not tell user that it 
        # already exists
        Path(target).mkdir()
    except:
        print(target+" already exists")
    path_lis = []
    file_lis = []
    exts = ['*.avi','*.mkv', '*.mp4','*.srt']
    for i in exts:
        path_lis.extend(Path(downloads).glob("**/"+i))
    for path in path_lis:
        file_lis.append(os.path.basename(path))
        print(path)

    for i in range(len(file_lis)):
        file_ = file_lis[i]
        #i.replace('.',' ',i.count('.') - 1)
        name = file_.replace('.',' ',file_.count('.') - 1)
        name = name.replace('-',' ',1)
        name = re.sub("\[|\]",'',name)

        if re.search("[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name):
            createInsert("[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name, path_lis[i], target)
            #pattern = "[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}"

        elif re.search("\d{1,2}[x]\d{1,2}\s", name):
            createInsert("\d{1,2}[x]\d{1,2}\s", name, path_lis[i], target)
            
        elif re.search("( |^)\d{3}([.| ])",name):
            print("here i am = "+ str(path_lis[i]))
            createInsert("( |^)\d{3}([.| ])",name, path_lis[i], target)
        #elif re.search("",name):

        else:
            createInsert("", name, path_lis[i], target)
    return 'success'
print(clean('downloads','C:\\Users\\vingi\\Documents\\episodes'))


#\d{3}[.| |a-b]