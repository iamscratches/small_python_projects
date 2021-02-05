from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
#import playsound
#import pyaudio
#from gtts import gTTS
import speech_recognition as sr
import random
import pyttsx3
import pytz
import subprocess


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ["nd", "rd", "th", "st"]

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day,service):
    # Call the calender API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(),singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day. ")
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12 :
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + "at" + start_time)

def speak(text):
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 125)     # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male

    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    print('listening...')
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said.lower()

def get_date(text):
    text = text
    print(text)
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    print(text.split())
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
            print('month found')
        elif word in DAYS:
            day_of_week = DAYS.index(word)
            print('day found')
        elif word.isdigit():
            day = int(word)
            print('day found 2')
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                        print('day found 3')
                    except:
                        pass
    #print('month=',month)
    #print('day=',day)
    #print('year=',year)
    if month < today.month and month != -1:
        year = year + 1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week
        if dif< 0:
            dif += 7
            if text.count("next") >= 1:
                dif +=7
        #print('month=',month)
        #print('day=',day)
        #print('year=',year)
        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None
    return datetime.date(month = month, day = day, year = year)
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open(file_name,"w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe",file_name])

SERVICE = authenticate_google()
CALENDER_STRS = ["what do i have","have plans","am i busy"]
NOTE_STRS = ["make a note","write this down"]
NAMES = ["dude","scratches","darling","beautiful","mom"]
TIME = ["tell","time"]
D_FLAG = 0
while(True):
    text = get_audio()
    if(set(text.split())&set(NAMES)):
        if(D_FLAG==0):
            for phrase in CALENDER_STRS :
                if phrase in text:
                    D_FLAG = 1
                    date = get_date(text)
                    print(date)
                    if date:
                        speak('The date you asked for is ' + str(date))
                        get_events(date,SERVICE)
                    else:
                        speak("i can't hear you please try again!!")
                        break
                    
        if(D_FLAG==0):   
            for phrase in NOTE_STRS:
                if phrase in text:
                    D_FLAG = 1
                    speak("what would you like me to write down?")
                    note_text = get_audio()
                    note(note_text)
                    speak("I've made a note of that.")
                    break
            
        if(set(text.split())&set(TIME) and D_FLAG==0):
            D_FLAG = 1
            print(str(datetime.datetime.now()))
            speak(str(datetime.datetime.now()))
            
        D_FLAG = 0
    elif "hello" in text:
        speak("hello, how are u?")
    elif "your name" in text:
        speak("My name is Scratches")
    elif "bye" in text or "tata" in text:
        speak("ok! bye bye!, nice to meet you")
        break










    

