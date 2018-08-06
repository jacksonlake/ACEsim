# ACEsim

Processes Google AudioSet and converts it to the DataBase for the ACE system. 

#acesimserver.py

Works under linux. Reads Google AudioSet csv file in series, for each video does the following:
1) Downloads youtube-video into m4a format using youtube-dl.
2) Converts m4a into wav with avconv.
3) Cropps wav according to start and stop time. 
4) Plays each file to the system and re-records it without substantial signal delay. 


#acesim.py

Plays and recordsat the sime time a SINGLE wav file. Plots the resullting wav files (time-amplitude). Works everywhere.
