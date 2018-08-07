import sys
import numpy as np
import getopt
import os.path
import subprocess

def check_existence(FILENAME):
    if os.path.isfile(FILENAME) == False:
        print('File', FILENAME, 'not found')
        sys.exit(2)
    else:
        return True

def download_crop_wav(name,START_TIME,STOP_TIME,link):
#--------------------------------------------------
#Downloads audio file from the provided link
#Converts downloaded m4a file into wav file
#Crops wav file according to START_TIME and STOP_TIME
#Adds to the name of the file _AI
#Takes only str objects!
#--------------------------------------------------
    command = 'youtube-dl -f 140 ' + link
    print('---------------------------\n')
    print('Invoking youtube-dl...\n') 
    print('---------------------------')
    os.system(command)
    os.system('ls')    
    print('---------------------------\n')
    print('Renaming downloaded file according with the DataBase...\n')
    print('---------------------------')
    command = 'mv *m4a ' + name + '.m4a'
    os.system(command)
    command = 'avconv -i ' + name + '.m4a ' + name + '.wav' #Converting to wav 
    os.system(command)
    print('---------------------------\n')
    print('Cropping...\n')
    print('---------------------------')
    command = 'ffmpeg -i '+ name + '.wav -ss ' + START_TIME + ' -to ' + STOP_TIME + ' ' + name + '_.wav' #cropping to START_TIME <-> STOP_TIME
    os.system(command)
    print('---------------------------\n')
    print('AI-ready file created...\n')
    print('---------------------------')
    os.system('ls')
    os.system('rm -rf *m4a') #Clean-up: all M4A files should be removed

def main(argv):
    inputfile=''
    outputfile=''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print("acesim.py <filename.wav>")
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-h":
            print("Converts Google AudioSet to the labeled A.C.E Database\nFilename structure: <label>_<id>_<duration>.wav\nUsage: acesimserver.py -i <csvname>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    outputfile = '_' + inputfile
    check_existence(inputfile)
    os.system('rm -rf *m4a') #Before we start, all M4A files should be removed
    #-----names
    START_TIME = str(50)
    STOP_TIME = str(70)
    link = 'https://www.youtube.com/watch?v=MkgR0SxmMKo'
    name = 'single'
    #-----names
    download_crop_wav('double','70','90','https://www.youtube.com/watch?v=VDHFK5b2uWw')
    #download_crop_wav(name,START_TIME,STOP_TIME,link)
    

if __name__ == "__main__":
   main(sys.argv[1:])
