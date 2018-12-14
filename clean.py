import shutil
from pathlib import Path
import os
import re

def createInsert(pattern, filename, file_path, target):
    #if there is no pattern add the file to a directory called unsorted
    if pattern == "":
        #split on the first slash to get the path
        folder_path = str(file_path).split('\\',1)[1]
        #print(folder_path+ " empty pattern")
        try:
            # creates a folder so as to reduce the manual work that the user
            #might be subjected to 
            Path(target+"\\Unsorted\\"+folder_path).parent.mkdir(parents=True,exist_ok=True)
        except:
            print("'"+filename+"' already exists. skip Creation")
        try:
            #shutil.move(file_path,Path(target+"\\Unsorted\\"+folder_path+"\\"))
            shutil.copy(file_path,Path(target+"\\Unsorted\\"+folder_path))
        except:
            print(str(file_path)+" Was not found")
        return
    season = ""
    filename = filename.replace('-',' ',1)

    #creates the number for the season 
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
    # split the file name in the hopes to get the name of the series
    temp = re.split(pattern,filename)
    series_name = temp[0]
    full_path = str(file_path).replace('\\','  ')
    #if file contains something like 501.avi or series 101 "some title".avi 
    # then overwrite the season and rename it 
    if re.search("( |^)\d{3}([.| ])",filename) and pattern == "( |^)\d{3}([.| ])":
        if re.search("^\d{3}.",filename):
            season = '0'+number[0]
        else:
            season = '0'+number[1]
        print(series_name+" here it is 1")

    if series_name.endswith(' '):
        spaces = re.search(r"\s{1,}$",series_name).group()
        series_name = series_name[:-len(spaces)]
        print(series_name+" 2")
    
    #if the file does not contain the name of show within then a regex search back 
    # for the given regex if its in a folder whcih has either Seasons, series or
    #  just number the get the name from the folder which it is in
    elif series_name == '' :#and re.search("[Ss]eason[.| ]\d{1,2}|[Ss]eries [ -|]{0,1} \d{1,2}| \d{1,2} ",full_path):
        series_name = full_path.split('  ',2)[1]

    # 
    series_name = series_name.title()
    
    try:
        #býr til folder með nafninu á folderinu !!!þarf að laga !!!!!
        Path(target+"\\"+series_name).mkdir()
    except:
        #lets you know if it already exists
        print("'"+series_name+"' already exists. skip Creation!")
    try: 
        #creates season 01 etc depending on the name of the file
        Path(target+"\\"+series_name+"\\Season "+season).mkdir()
    except:
        print("'"+series_name+"\\Season "+season+"' already exists. skip Creation!")
    try:
        #shutil.move(file_path,Path(target+"\\"+series_name+"\\Season "+season+"\\"))
        shutil.copy(file_path,Path(target+"\\"+series_name+"\\Season "+season))
    except:
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
        name = file_lis[i].replace('.',' ',file_lis[i].count('.') - 1)
        name = re.sub("[;\/:*?""<>|&']",'',name)# replaces special characters 
        # for ease of naming and reduce duplication
        name = name.replace("_",' ',1)# same as the aboves

        #searches for pattern with s04e04, s1e02, s1 e02 , s01 e 03 or 01 E01 
        if re.search("[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name):
            createInsert("[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name, path_lis[i], target)

        #searches for pattern with [1 12], [12x31] or 12x01 and then removes the
        #brackets for ease of naming in createInsert function
        elif re.search("\s[\[]{0,1}\d{1,2}[(x| )]\d{1,2}[\]]{0,1}\s", name):
            name = re.sub("\[|\]",'',name)
            createInsert("\d{1,2}[(x| )]\d{1,2}\s", name, path_lis[i], target)
        
        # matches a pattern 501.avi, Friends 312 - the one where monica blab.avi
        elif re.search("( |^)\d{3}([.| ])",name):
            createInsert("( |^)\d{3}([.| ])",name, path_lis[i], target)
        
        #use an empty pattern to the notify createInsert function to add the file
        # to unsorted folder
        else:
            createInsert("", name, path_lis[i], target)
    return 'success'
print(clean('C:\\Users\\vingi\\Documents\\downloads','C:\\Users\\vingi\\Documents\\fuckit3'))


#\d{3}[.| |a-b]