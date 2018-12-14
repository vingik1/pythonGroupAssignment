import argparse
from testfileforargsandgui import testfunction

parser = argparse.ArgumentParser(description='Should clean up most of your ' \
                        'downloads folder and put it into an output folder. \n'\
                        'If the file does not exist it will be created.'\
                        'This script needs python 3.7.1 to run correctly ')
    
parser.add_argument('input', type=str, help='the folder you want to clean')
parser.add_argument('output', type=str, help='the file you want to build')
parser.add_argument('-v', '--verbose', action='store_true', default=False, \
                    help='For a more detailed view '\
                    'you can select this option.\nRecommended during '\
                    'first run to see if the script positioned the files '\
                    'in the right folders')
parser.add_argument('-r', '--removeempty', action='store_true', default=False,\
                    help='This option tells the program to remove the '\
                    'empty directories left behind when the script has '\
                    'moved the videofiles to a new permanent home')
parser.add_argument('-n', '--nforemove', action='store_true', default=False,\
                    help='An option best used with the "delete empty folders" '\
                    'option. You clean out the crappy NFO files that often ' \
                    'accomodate downloaded files. Since they are (to our '\
                    'knowledge) trash left behind when the videofile has been '\
                    'moved, this might cause the "remove empty files" '\
                    'option to leave behind a load of folders containing '\
                    'only these useless NFO files')
parser.add_argument('-d', '--disabletrust', action='store_true', default=False,\
                    help='Disables "trust mode" prompting you to rename your'\
                    'files. With a lot of files this'\
                    ' could cause you to be promted to rename a LOT of files.'\
                    'however - if you get tired midprocess, you can turn it'\
                    'off during, or accept the selected file name.')

args = parser.parse_args()



testfunction(args.input, args.output, args.verbose, args.nforemove, args.removeempty, args.disabletrust, False)

# print(type(args.input))
# print(args.output)
