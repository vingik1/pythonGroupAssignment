import sys
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from tkinter import BooleanVar
from tkinter import Button
from tkinter import Checkbutton
from tkinter import Label
from tkinter.constants import NW, N, W, E, SW, NSEW, INSERT, DISABLED, END
from clean import clean
import os
from tkinter.scrolledtext import ScrolledText
from threading import Thread
import time
root = Tk()
root.title('Download Folder Cleaner ATTATCHED!!!')

#center gui on screen
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry("+{}+{}".format(positionRight, positionDown))

# finalize root and make expandable in a way that only the textbox gets bigger
root.grid()
root.grid_rowconfigure(9, weight=1)
root.grid_columnconfigure(1, weight=1)
root.minsize(600,350)
root.update()

#### esc closing bind
# top-text for closing with esc
closetext = Label(root, text="(ESC to close)", height=1)
closetext.grid(column=1, row=0, columnspan=2, pady=5, sticky=SW)
def close(event):
    '''escape closes window'''
    sys.exit() 
root.bind('<Escape>', close)

### select input button
root.inputpath = StringVar()

def input_button():
    root.inputpath = filedialog.askdirectory(initialdir=os.getcwd())
    inputlabel.config(text=root.inputpath)

inputlabel = Label(root, text="Dirty Download Folder",\
                    background='white', anchor=W)
inputlabel.grid(row=1, column=1, sticky=NW+E, padx=(5, 10), pady=5)
inputbutton = Button(root, text="Folder to sort",\
                    command=input_button, width=18)
inputbutton.grid(row=1, column=0, sticky=N, padx=5, pady=5)

### select output button
root.outputpath = StringVar() 

def output_button():
    root.outputpath = filedialog.askdirectory(initialdir=os.getcwd())
    outputlabel.config(text=root.outputpath)

outputlabel = Label(root, text="Destination folder",\
                    background='white', anchor=W)
outputlabel.grid(row=2, column=1, sticky=NW+E, padx=(5, 10), pady=5)
outputbutton = Button(root, text="Your clean library",\
                    command=output_button, width=18)
outputbutton.grid(row=2, column=0, padx=5, pady=5)

### option checkboxes --- verbose inactive in gui
# option to see whats happening under the hood
root.verbose = BooleanVar()
root.verbose.set(False) 
verbosebox = Checkbutton(root, text='Verbose mode ! works to some extent, will be more definite when most debugging is over)',\
                            var=root.verbose)
verbosebox.grid(row=3, column=1, columnspan=2, sticky=NW)

# Option to remove empty directories left behind
root.remove_empty = BooleanVar()
root.remove_empty.set(False)  # set check state
remove_empty_box = Checkbutton(root, text='Delete empty folders !!! NOT IMPLEMENTED',\
                            var=root.remove_empty)
remove_empty_box.grid(row=4 , column=1, sticky=NW)
# Option to delete nfos from directories
root.nfo_remove = BooleanVar()
root.nfo_remove.set(False)  # set check state
nfo_remove_box = Checkbutton(root, text='Delete NFO files !!! NOT IMPLEMENTED',\
                            var=root.nfo_remove)
nfo_remove_box.grid(row=5 , column=1, columnspan=2, sticky=NW)

# trust the program to rename files appropriatly 
root.trust = BooleanVar()
root.trust.set(True)  # set check state
trust_box = Checkbutton(root, text='Trust mode - Disabling this will allow '\
                                    'you to manually name your files !!! NOT IMPLEMENTED',\
                                    var=root.trust)
trust_box.grid(row=6 , column=1, columnspan=2, sticky=NW)

### start process button
def start_process_button(): 
    # if input is empty or output is empty display error
    
    if os.path.isdir(str(root.inputpath))\
        and os.path.isdir(str(root.outputpath))\
        and root.inputpath != root.outputpath:
        startbtn.config(state=DISABLED, text="Working, like... so hard")
        startbtn.update()
        # if verbose is on, it redirects the stdout to the texbox,
        # making the printed text show up in textbox
        if root.verbose.get():
            sys.stdout.write = redirect_print_to_textbox
        ## threading was first implemented as a way to let the OS know that
        # the gui was still working (fix a "program not responding" error
        # while funtion was running)
        t1 = Thread(target=clean, args=(str(root.inputpath), str(root.outputpath),\
            root.verbose.get(), root.nfo_remove.get(),\
            root.remove_empty.get(), root.trust.get(), True))
        root.config(cursor="pirate")
        root.update()
        t1.start()
        #in verbose mode the textbox is constantly showing the stream
        #out of verbose it will show a 'Working' and add dots to the screem
        #to show that the function is still working on another thread.
        if not root.verbose:
            while Thread.isAlive(t1):
                textbox.insert(INSERT, 'Working')
                time.sleep(0.1)
                textbox.insert(INSERT, '.')
                textbox.update()
                textbox.see(END)
        else:
            while Thread.isAlive(t1):
                #time.sleep(0.1)
                #textbox.insert(INSERT, '.')
                textbox.update()
                textbox.see(END)
        textbox.insert(INSERT, '\nAll done!!! :D ')
        #Sets the textbox to see the bottom where all the new stuff is 
        root.config(cursor="")
        root.update()
        textbox.see('end')
        startbtn.config(text='Finished!')
    else:
        messagebox.showinfo('Required field(s) missing', 'At the minimum,'\
                        'the input and output folders must be selected'\
                        " Also: you can't select same folder as both paths"\
                        ' you silly ')

startbtn = Button(root, text='Clean up!', command=start_process_button,\
                        width=25, height=2)
startbtn.grid(row=7, column=1, rowspan=2, padx=5, pady=10, sticky=NW)

### Textbox and output
textbox = ScrolledText(root, height=5, width=50)
textbox.config(wrap='word')
textbox.grid(row=9, column=0,columnspan=2, padx=5, pady=5, sticky=NSEW)

# enables printing into textbox with verbose
def redirect_print_to_textbox(stream):
    textbox.insert(INSERT, stream)

root.mainloop()