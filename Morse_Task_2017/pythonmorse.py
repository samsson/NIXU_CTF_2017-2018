import pyaudio
import struct
import math
from datetime import datetime
import requests
#0.034 small one
#0.1 long one
#0.03 small gap
#0.13 long gap

thresh = 0.023
sample_period = 0.001
RATE = 44100
sample_cycles = int(RATE*sample_period)
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
FORMAT=pyaudio.paInt16
pa=pyaudio.PyAudio()
stream = pa.open(format = FORMAT,
         channels = CHANNELS,
         rate = RATE,
         input = True,
         frames_per_buffer = sample_cycles)

thresh_final=thresh
list1=""
counter=0
count = 0

CODE ={
        "A" : ".-",     "B" : "-...",       "C" : "-.-.",
        "D" : "-..",    "E" : ".",          "F" : "..-.",
        "G" : "--.",    "H" : "....",       "I" : "..",
        "J" : ".---",   "K" : "-.-",        "L" : ".-..",
        "M" : "--",     "N" : "-.",         "O" : "---",
        "P" : ".--.",   "Q" : "--.-",       "R" : ".-.",
        "S" : "...",    "T" : "-",          "U" : "..-",
        "V" : "...-",   "W" : ".--",        "X" : "-..-",
        "Y" : "-.--",   "Z" : "--..",       " " : "/",

        "1" : ".----",  "2" : "..---",      "3" : "...--",
        "4" : "....-",  "5" : ".....",      "6" : "-....",
        "7" : "--...",  "8" : "---..",      "9" : "----.",
        "0" : "-----"
        }

CODE_REVERSED = {value:key for key,value in CODE.items()}
def decodeMorse(s):
    return ''.join(CODE_REVERSED.get(i) for i in s.split())
        #if i != None:


def rms(sample):
    count = len(sample)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, sample )

    sum_squares = 0.0
    for i in shorts:

        n = i * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

for i in range(26000):
    try:
        sample=stream.read(sample_cycles)
    except IOError:
        print("Error Recording")

    amp=rms(sample)

    if amp>thresh:
        list1+="1"
    else:
        list1+="0"
list1=list1.split("0")
list2 = ""
#print(list1)

for i in range(len(list1)):
    if len(list1[i])<=52 and len(list1[i])>=15:
        list2 = list2 + "."
        count = 0
    elif len(list1[i])>=53:
        list2 = list2 + "-"
        count = 0
    elif list1[i]==list1[i-1]:
        count = count + 1
        if count > 100:
            list2 = list2 + " "
            count = 0
print(list2)
print(decodeMorse(list2))
r = requests.post("http://bagbounty17.science/morse", data={'code': '{0}'.format(decodeMorse(list2))})
print(r.status_code, r.reason)
print(r.text[:300] + '...')
