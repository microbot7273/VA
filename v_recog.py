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
from selenium import webdriver

d = '/Applications'
greet = "hi"
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

def web_search(input):
    driver = webdriver.chrome()
    driver.implicitly_wait(1)
    driver.maximize_window()
    if 'youtube' in input.lower():
        say("opening Youtube for you")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx+1:]
        driver.get('http://www.youtube.com/results?search_query='+'+'.join(query))
        say('here you go')
        return
    elif 'wikipedia' in input.lower():
        say("Opening wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1: ]
        driver.get('http://en.wikipedia.org/wiki/'+'_'.join(query))
        say("Here is your information from wikipedia")
        return
    else: 
        if 'google' in input.lower():
            say("on it")
            indx = input.lower().split().index('google')
            query = inpit.split()[indx + 1: ]
            driver.get('http://www.google.com/search?q='+ '+'.join(query))
            say("Here are your google search results")
            return
        elif 'search' in input.lower():
            say("on it")
            indx = input.lower().split().index('google')
            query = inpit.split()[indx + 1: ]
            driver.get('http://www.google.com/search?q='+ '+'.join(query))
            say("Here are your google search results")
            return
        else:
            driver.get('http://www.google.com/search?q='+ '+'.join(input.split()))
            say("These are your quick websearch results")
fs=16000
duration = 1  # seconds
r = sr.Recognizer()
mic = sr.Microphone()

while(True): 
    #print("loop testing")
    #say("Hello Raghava")
    #t = activate()
    #print("you said: " +str(t))
    print("listening.....")
    say("Ahem")
    if activate() == True:
        try:
            say("Hey Sai, how can I help you today?")
            with mic as source:
                print("Say Something!")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                print("listened, working on it now")
                transcript = r.recognize_google(audio)
                if 'open' in transcript.lower():
                    sys_command = search_es(transcript)
                    os.system(sys_command)
                    say("I opened that application for you")
                elif 'close' in str(transcript) or 'exit' in str(transcript):
                    say("ok then, Bye")
                    close_condition = 1
                    break
                else:
                    web_search(transcript)
        except:
            pass
    else:
        say("could you please repeat")
        #print("Did you say something")
        #print(t)



        