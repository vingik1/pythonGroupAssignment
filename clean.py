import shutil
from pathlib import Path
import os
import re
import time
from tkinter import simpledialog
from tkinter import messagebox

def createInsert(pattern, filename, file_path, outputfile, verbose, trust, gui):
    #if there is no pattern add the file to a directory called unsorted
    if pattern == "":
        #split on the first slash to get the path
        folder_path = str(file_path).split('\\',1)[1]
        #print(folder_path+ " empty pattern")
        try:
            # creates a folder so as to reduce the manual work that the user
            #might be subjected to 
            Path(outputfile+"\\Unsorted\\"+folder_path).parent.mkdir(parents=True,exist_ok=True)
        except:
            print("'"+filename+"' already exists. skip Creation")
        try:
            #shutil.move(file_path,Path(outputfile+"\\Unsorted\\"+folder_path+"\\"))
            shutil.copy(file_path,Path(outputfile+"\\Unsorted\\"+folder_path))
        except:
            print(str(file_path)+" Was not found")
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
    # split the file name in the hopes to get the name of the series
    temp = re.split(pattern,filename)
    series_name = temp[0]
    full_path = str(file_path).replace('\\','  ')
    #if file contains something like 501.avi or series 101 "some title".avi 
    # then overwrite the season and rename it 
    if re.search(r"( |^)\d{3}([.| ])",filename) and pattern == r"( |^)\d{3}([.| ])":
        if re.search(r"^\d{3}.",filename):
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
        Path(outputfile+"\\"+series_name).mkdir()
    except:
        #lets you know if it already exists
        print("'"+series_name+"' already exists. skip Creation!")
    try: 
        #creates season 01 etc depending on the name of the file
        Path(outputfile+"\\"+series_name+"\\Season "+season).mkdir()
    except:
        print("'"+series_name+"\\Season "+season+"' already exists. skip Creation!")
    try:
        if trust:
        ### Program is trusted to rename everything
            shutil.copy(file_path,Path(outputfile+"\\"+series_name+"\\Season "+season))
        elif not trust and not gui:
        ### Program is not trusted and is running in console
            file_ending_keepsafe = filename.split('.')[-1] #aetti ad vista filetype
            is_valid = False # tekur vid input thar til file name er acceptable
            print('Type a new name (without filetype (ending)) to rename.\n'
                'To keep the file name as is, just press Enter\n'\
                'Type CANCEL to stop renaming, and let the program finish'\
                ' renaming. \n Type QUIT to close program \n'\
                'Do you want to rename this file?\n', filename,)
            while not is_valid:
                userinput = input("Enter new file name:")
                if userinput == 'CANCEL':
                    trust = True
                    is_valid = True
                    print('Exiting manual renaming mode')
                    time.sleep(1) ## to show user that they have exited renaming
                    shutil.copy(file_path,Path(outputfile+"\\"+series_name+"\\Season "+season))
                elif userinput == '':
                    is_valid = True
                    shutil.copy(file_path,Path(outputfile+"\\"+series_name+"\\Season "+season))
                else:
                ######## Herna tharf ad implementa ad rett nafn fari inn i breytuna og lika file-ending breyta
                    newfilename = userinput+file_ending_keepsafe
                    #shutil command "moving" the file with its new name
        elif not trust and gui:
        ### Program is not trusted and running in GUI
            is_valid = False
            while not is_valid:
                #### tharf ad vera keepsafe sem heldur utan um nafn ef user gerir cancel
                keepsafe = filename
                # promptar input glugga
                prompt = simpledialog.askstring('Enter File Name', 'Pushing cancel will stop manual renaming', initialvalue=filename)
                if prompt is None:
                    prompt = keepsafe
                    trust = True
                    is_valid = True
                elif prompt == '': ### þarf að bæta við að laga þannig að það sé bara hægt að rename-a í eitthvað sem file má heita
                    # Warning prompt to input a valid file name
                    messagebox.showinfo("You're doing it wrong", 'Please enter a valid folder name')
                else:
                    filename = prompt
                    is_valid = True
                    shutil.copy(file_path,Path(outputfile+"\\"+series_name+"\\Season "+season))
                if verbose:
                    print('Renamed the file', keepsafe, 'to', filename)
        ### just a debug print, should never get here
        else:
            print('not sure how this got here... my ifelses are not good enough')
#
#
        #shutil.move(file_path,Path(outputfile+"\\"+series_name+"\\Season "+season+"\\"))
    except:
        if verbose:
            print(str(file_path)+" Was not found")
        else:
            pass
    
    return trust


def clean(inputfile, outputfile, verbose, nfo, removeempty, trust, gui):
    print(os.path.isdir(str(inputfile)), os.path.isdir(str(outputfile)), inputfile != outputfile)
    print('trust is set on ', trust)
    ### þetta hér fyrir neðan þarf að fara í kringum functinið r sum til að kasta villu
    # if os.path.isdir(str(inputfile))\
    #     and os.path.isdir(str(outputfile))\
    #     and inputfile != outputfile:
    #     return "folders are the same or not directories"
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
        name = re.sub(r"[;\/:*?""<>|&']",'',name)# replaces special characters 
        # for ease of naming and reduce duplication
        name = name.replace("_",' ',1)# same as the aboves

        #searches for pattern with s04e04, s1e02, s1 e02 , s01 e 03 or 01 E01 
        if re.search(r"[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name):
            trust = createInsert(r"[sS]{0,1}\d{1,2}[ ]{0,1}[eE][ ]{0,1}\d{2}", name, path_lis[i], outputfile, verbose, trust, gui)

        #searches for pattern with [1 12], [12x31] or 12x01 and then removes the
        #brackets for ease of naming in createInsert function
        elif re.search(r"\s[\[]{0,1}\d{1,2}[(x| )]\d{1,2}[\]]{0,1}\s", name):
            name = re.sub(r"\[|\]",'',name)
            trust = createInsert(r"\d{1,2}[(x| )]\d{1,2}\s", name, path_lis[i], outputfile, verbose, trust, gui)
        
        # matches a pattern 501.avi, Friends 312 - the one where monica blab.avi
        elif re.search(r"( |^)\d{3}([.| ])",name):
            trust = createInsert(r"( |^)\d{3}([.| ])",name, path_lis[i], outputfile, verbose, trust, gui)
        
        #use an empty pattern to the notify createInsert function to add the file
        # to unsorted folder
        else:
            trust = createInsert("", name, path_lis[i], outputfile, verbose, trust, gui)
    return 'success'
#print(clean('C:\\Users\\vingi\\Documents\\downloads','C:\\Users\\vingi\\Documents\\fuckit3'))
#print(clean('../../downloads','../../episodes', False, False, False, False, False))

#createInsert(pattern, filename, file_path, outputfile, verbose, trust, gui)

#\d{3}[.| |a-b]