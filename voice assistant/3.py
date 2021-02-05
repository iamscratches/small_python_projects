from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import pyaudio
from gtts import gTTS
import speech_recognition as sr
import random


voice = 0
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

def get_events(n,service):
    # Call the calender API
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def speak(text):
    tts = gTTS(text = text, lang = "en-in")
    global voice
    #print(voice)
    filename = str(voice )+ ".mp3"
    voice = voice +1
    tts.save(filename)
    playsound.playsound(filename)

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
    return said

def get_date(text):
    text = text.lower()
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
    print('month=',month)
    print('day=',day)
    print('year=',year)
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

        return today + datetime.timedelta(dif)
        print('month=',month)
        print('day=',day)
        print('year=',year)
    return datetime.date(month = month, day = day, year = year)
#speak('2020-05-08')

#print(MONTHS.index('september'))

speak("Bakchodi Baap Kareh ya Beta gaand marana bete Ko he padta hai")
'''while(True):
    text = get_audio().lower()
    if("scratches" in text):
        date = get_date(text)
        print(date)
        if(date is not None):
            speak('The date you asked for is ' + str(date))
    elif "hello" in text:
        speak("hello, how are u?")
    elif "your name" in text:
        speak("My name is Scratches")
    elif "bye" in text:
        speak("ok! bye bye!, nice to meet you")
        break
'''
#"what do i have planned on september 9th"


'''service = authenticate_google()
get_events(2,service)'''
