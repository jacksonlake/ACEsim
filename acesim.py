import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import numpy as np
import getopt
import os.path
import time
import threading

def check_existence(FILENAME):
    if os.path.isfile(FILENAME) == False:
        print('File', FILENAME, 'not found')
        sys.exit(2)
    else:
        return True

def play_wav_file(WAVE_FILENAME,stam):
    wf = wave.open(WAVE_FILENAME, 'rb')
    p = pyaudio.PyAudio()
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,stream_callback=callback)
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

def plot_wav_file(WAVE_FILENAME,RECORD_SECONDS):
    input_data = read(WAVE_FILENAME)
    audio = input_data[1]
    plt.plot(audio[0:RECORD_SECONDS*1024])
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title(WAVE_FILENAME)
    plt.show()

def record_wav_file(WAVE_OUTPUT_FILENAME,RECORD_SECONDS):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_record_draw(WAVE_INPUT, WAVE_OUTPUT,RECORD_SECONDS): #simultaneously plays, records and draws wav file with multithreading
    p = pyaudio.PyAudio()
    t_play = threading.Thread(target = play_wav_file,args =(WAVE_INPUT,1))
    t_record = threading.Thread(target = record_wav_file,args = (WAVE_OUTPUT,RECORD_SECONDS))
    t_play.start()
    t_record.start()
    time.sleep(11)
    plot_wav_file(WAVE_OUTPUT,RECORD_SECONDS)
    plot_wav_file(WAVE_INPUT,RECORD_SECONDS)
    p.terminate()




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
            print("Plays, recors and analyzes a single wav file for the A.C.E Software.\nUsage: acesim.py -i <inputfilename>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    outputfile = '_' + inputfile
    check_existence(inputfile)
    play_record_draw(inputfile,outputfile,5)


    


if __name__ == "__main__":
   main(sys.argv[1:])
