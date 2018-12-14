import shutil
from pathlib import Path
import os
import re

def createInsert(pattern, filename, file_path, outputfile, trust, verbose, gui):
    #if there is no pattern add the file to a directory called unsorted
    if pattern == "":
        folder_path = str(file_path).split('\\',1)[1]
        if verbose:
            print(folder_path)
        try:
            Path(outputfile+"\\Unsorted\\"+folder_path).parent.mkdir(parents=True,exist_ok=True)
        except:
            if verbose:
                print("'"+filename+"' already exists. skip")
            else:
                pass
        try:
            shutil.copy(file_path,Path(outputfile+"\\Unsorted\\"+folder_path))
        except:
            if verbose:
                print(str(file_path)+" Was not found")
            else:
                pass
        return trust
    season = ""
    if verbose:
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
    if verbose:
        print(number[1])
    #temp splitar svo hægt sé að fá nafnið á þá fyrir folder
    temp = re.split(pattern,filename)
    series_name = temp[0]
    full_path = str(file_path).replace('\\','  ')

    if re.search(r"( |^)\d{3}([.| ])",filename):
        season = '0'+number[1]
        if verbose:
            print(series_name+" 1")

    if series_name.endswith(' '):
        spaces = re.search(r"\s{1,}$",series_name).group()
        series_name = series_name[:-len(spaces)]
        if verbose:
            print(series_name+" 2")
    #if the file does not contain the name of show within then a regex search back for the given
    # regex if its in a folder whcih has either Seasons, series or just number the get the name 
    #from folder which it is in
    elif series_name == '' :#and re.search("[Ss]eason[.| ]\d{1,2}|[Ss]eries [ -|]{0,1} \d{1,2}| \d{1,2} ",full_path):
        series_name = full_path.split('  ',2)[1]
        if verbose:
            print( full_path.split(' ',2))
            print(series_name +" 3")
    
    series_name = series_name.title()
    #foundName = True
    try:
        #býr til folder með nafninu á folderinu !!!þarf að laga !!!!!
        Path(outputfile+"\\"+series_name).mkdir()
    except:
        #lætur vit ef þegar til
        #pass
        if verbose:
            print("'"+series_name+"' already exists. skip")
        else:
            pass
    try: 
        #býr svo til season 01 etc eftir nafninu á file-num
        Path(outputfile+"\\"+series_name+"\\Season "+season).mkdir()
    except:
        if verbose:
            print("'"+series_name+"\\Season "+season+"' already exists. skip")
        else:
            pass
    try:
        if trust:
            shutil.copy(file_path,Path(outputfile+"\\"+series_name \
                        +"\\Season "+season))
        elif not gui and not trust:
            fileending = filename.split('.')[-1] ## keeps the file ending as is
            isvalid = False
            print('Do you want to rename this file?\n', filename,\
                 '\nYou do not have to type the ending defining the file type. '\
                 'Leaving the input blank will keep the original name and move'\
                 ' on to the next file')
            while not isvalid:
                userinput = input('Enter new name to rename, or just push'\
                        ' enter to skip this file.\nType CANCEL to stop'\
                        'renaming files at any time')
                if userinput == 'CANCEL':
                    trust = True
                    print('trust is now', trust)
                    isvalid = True
                    shutil.copy(file_path,Path(outputfile+"\\"+series_name+ \
                    "\\Season "+season))
                elif userinput == '':
                    isvalid = True
                    shutil.copy(file_path,Path(outputfile+"\\"+series_name \
                    +"\\Season "+season+userinput+fileending))
                else:
                    shutil.copy(file_path,Path(outputfile+"\\"+series_name \
                    +"\\Season "+season+userinput+fileending))
                
            
        #else: #if not trusted and not in guimode

            
            
    except:
        #pass
        print(str(file_path)+" Was not found")
    return trust


def clean(inputfile, outputfile, verbose, nfo, removeempty, trust, gui):
    if not os.path.isdir(inputfile):
        return "inputfile was not valid"
    try:
        #creates a directory with the given name if not tell user that it 
        # already exists
        Path(outputfile).mkdir()
    except:
        if verbose:
            print(outputfile+" already exists")
        else:
            pass
    path_lis = []
    file_lis = []
    exts = ['*.avi','*.mkv', '*.mp4','*.srt']
    for i in exts:
        path_lis.extend(Path(inputfile).glob("**/"+i))
    for path in path_lis:
        file_lis.append(os.path.basename(path))
        #print(str(path))

    for i in range(len(file_lis)):
        print('trust is', trust)
        file_ = file_lis[i]
        #i.replace('.',' ',i.count('.') - 1)
        name = file_.replace('.',' ',file_.count('.') - 1)
        name = name.replace('-',' ',1)
        name = re.sub(r"\[|\]",'',name)

        if re.search(r"[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name):
            trust = createInsert(r"[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name, path_lis[i], outputfile, trust, verbose, gui)
            #pattern = "[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}"

        elif re.search(r"\d{1,2}[x]\d{1,2}\s", name):
            trust = createInsert(r"\d{1,2}[x]\d{1,2}\s", name, path_lis[i], outputfile, trust, verbose, gui)
            
        elif re.search(r"( |^)\d{3}([.| ])",name):
            if verbose:
                print("here i am = "+ str(path_lis[i]))
            trust = createInsert(r"( |^)\d{3}([.| ])",name, path_lis[i], outputfile, trust, verbose, gui)
        #elif re.search("",name):

        else:
            trust = createInsert("", name, path_lis[i], outputfile, trust, verbose, gui)
    return 'success'
print(clean('../../downloads','../../episodes', False, False, False, False, False))
# def clean(inputfile, outputfile, verbose, nfo, removeempty, trust, gui):


#\d{3}[.| |a-b]