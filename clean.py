import shutil
from pathlib import Path
import os
import re

def createInsert(pattern, filename, file_path, outputfile, trust, verbose, gui, inputfile):
    #if there is no pattern add the file to a directory called unsorted
    if pattern == "":
        #split the input file and get last element and use it split the path
        # this is done to mimic a relative path from absolute path
        try:
            input_location = inputfile.split('\\')[-1]
            folder_path = str(file_path).split(input_location)[1]
        except:
            return trust
        #print(folder_path+ " empty pattern")
        try:
            # creates a folder so as to reduce the manual work that the user
            #might be subjected to 
            Path(outputfile+"\\Unsorted"+folder_path).parent.mkdir(parents=True,exist_ok=True)
        except:
            if verbose:
                print("'"+filename+"' already exists. skip Creation")
            else:
                pass
        try:
            #shutil.move(file_path,Path(outputfile+"\\Unsorted\\"+folder_path+"\\"))
            shutil.copy(file_path,Path(outputfile+"\\Unsorted\\"+folder_path))
        except:
            if verbose:
                print(str(file_path)+" Was not found")
            else:
                pass
        return trust
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
    #split the input file and get last element and use it split the path
    # this is done to mimic a relative path from absolute path
    try:
            input_location = inputfile.split('\\')[-1]
            path_ = str(file_path).split(input_location)[1]
            file_path = input_location + path_
            print(file_path+" pepega")
    except:
        pass
    temp = re.split(pattern,filename)
    print(filename+" !")
    print(str(file_path)+" ?")
    series_name = temp[0]
    full_path = str(file_path).replace('\\','  ')
    print(full_path)
    #if file contains something like 501.avi or series 101 "some title".avi 
    # then overwrite the season and rename it 
    if re.search("( |^)\d{3}([.| ])",filename) and pattern == "( |^)\d{3}([.| ])":
        if re.search("^\d{3}.",filename):
            season = '0'+number[0]
        else:
            season = '0'+number[1]
        if verbose:
            print(series_name+" here it is 1")

    if series_name.endswith(' '):
        spaces = re.search("\s{1,}$",series_name).group()
        series_name = series_name[:-len(spaces)]
        if verbose:
            print(series_name+" 2")
    
    #if the file does not contain the name of show within then a regex search back 
    # for the given regex if its in a folder whcih has either Seasons, series or
    #  just number the get the name from the folder which it is in
    if series_name == '' :#and re.search("[Ss]eason[.| ]\d{1,2}|[Ss]eries [ -|]{0,1} \d{1,2}| \d{1,2} ",full_path):
        series_name = full_path.split('  ',2)[1]
        print(series_name+ " 3")
    # 
    series_name = series_name.title()
    
    try:
        #Creates a folder with the name of the folder 
        Path(outputfile+"\\"+series_name).mkdir()
    except:
        #lets you know if it already exists
        if verbose:
            print("'"+series_name+"' already exists. skip Creation!")
        else:
            pass
    try: 
        #creates season 01 etc depending on the name of the file
        Path(outputfile+"\\"+series_name+"\\Season "+season).mkdir()
    except:
        if verbose:
            print("'"+series_name+"\\Season "+season+"' already exists. skip Creation!")
        else:
            pass
    try:
        #shutil.move(file_path,Path(outputfile+"\\"+series_name+"\\Season "+season+"\\"))
        shutil.copy(file_path,Path(outputfile+"\\"+series_name+"\\Season "+season))
    except:
        if verbose:
            print(str(file_path)+" Was not found")
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
    try:
        #creates a directory with the given name if not tell user that it 
        # already exists
        Path(outputfile).mkdir()
    except:
        print(outputfile+" already exists")
    path_lis = []
    file_lis = []
    exts = ['*.avi','*.mkv', '*.mp4','*.srt']
    for i in exts:
        path_lis.extend(Path(inputfile).glob("**/"+i))
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
            trust = createInsert("[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name, path_lis[i], outputfile, trust, verbose, gui,inputfile)

        #searches for pattern with [1 12], [12x31] or 12x01 and then removes the
        #brackets for ease of naming in createInsert function
        elif re.search("\s[\[]{0,1}\d{1,2}[(x| )]\d{1,2}[\]]{0,1}\s", name):
            name = re.sub("\[|\]",'',name)
            trust = createInsert("\d{1,2}[(x| )]\d{1,2}\s", name, path_lis[i], outputfile, trust, verbose, gui,inputfile)
        
        # matches a pattern 501.avi, Friends 312 - the one where monica blab.avi
        elif re.search("( |^)\d{3}([.| ])",name):
            print("i is here boss")
            trust = createInsert("( |^)\d{3}([.| ])",name, path_lis[i], outputfile, trust, verbose, gui, inputfile)
        
        #use an empty pattern to the notify createInsert function to add the file
        # to unsorted folder
        else:
            trust = createInsert("", name, path_lis[i], outputfile, trust, verbose, gui, inputfile)
    return 'success'
#print(clean('C:\\Users\\vingi\\Documents\\downloads','C:\\Users\\vingi\\Documents\\fuckit3'))
#print(clean('E:\Onedrive\HRHaustonn2018\PRLA\GroupAssignment\downloads','C:\\Users\\Viktor\\Documents\\fuckit2', True, False, False, True, False))

#\d{3}[.| |a-b]