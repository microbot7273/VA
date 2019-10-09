import os
import pandas as  pd
import librosa as lbs
import glob
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import subprocess
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

d = '/Applications'
greet = "hello"
records = []
apps = os.listdir(d)
for app in apps:
    record = {}
    record['voice_command'] = 'open ' + app.split('.app')[0]
    record['sys_command'] = 'open ' + d +'/%s' %app.replace(' ','\ ')
    records.append(record)



es = Elasticsearch(['http://localhost:9200/'])
bulk(es, records, index='voice_assistant', doc_type='text', raise_on_error=True)
def search_es(query):
    res = es.search(index="voice_assistant", doc_type="text", body={                     
    "query" :{
        "match": {
            "voice_command": {
                "query": query,
                "fuzziness": 2
            }
            }
        },
    })
    return res['hits']['hits'][0]['_source']['sys_command']

def say(text):
    subprocess.call(['say', text])

def activate(phrase=greet):
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            transcript = r.recognize_google(audio)
            if transcript.lower() == phrase:
                return True
            else:
                return False
    except:
        pass

fs=44100
duration = 1  # seconds
r = sr.Recognizer()
mic = sr.Microphone()

while(True): 
    print("loop testing")
    say("Hello Raghava")
    t = activate()
    print("you said: " +str(t))  
    if activate() == True:
        try:
            say("Hey Sai, how can I help you today?")
            with mic as source:
                print("Say Something!")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                transcript = r.recognize_google(audio)
                sys_command = search_es(transcript)
                os.system(sys_command)
                say("I opened that application for you")
        except:
            pass
    else:
        pass


#fs=44100
#duration = 1  # seconds
#r = sr.Recognizer()
#mic_name = sr.Microphone()
#d = '/Applications'
#records = []
#apps = os.listdir(d)
#for app in apps:
#    record = {}
#    record['voice_command'] = 'open ' + app.split('.app')[0]
#    record['sys_command'] = 'open ' + d +'/%s' %app.replace(' ','\ ')
#    records.append(record)
#while(True):
#    with mic_name as source:
#        r.adjust_for_ambient_noise(source) 
#        print ("Say Something")
#        audio = r.listen(source)
#        try: 
#            text = r.recognize_google(audio) 
#            print ("you said: " + text)
            
#        except sr.UnknownValueError: 
#            print("Google Speech Recognition could not understand audio") 
      
 #       except sr.RequestError as e: 
 #           print("Could not request results from Google  Speech Recognition service; {0}".format(e))
 #       say("Hello sai")        
        