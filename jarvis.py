# Tony Stark as standard
# Voice assistant
# My project on the subject of information technology

import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import time
import webbrowser
import os
import requests
import json


# OPTIONS
opts = {
    "alias": ('Чувак', 'чувак'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'открой', 'зайди', 'включи'),
    "commands": {
        "current_time": ('текущее время', 'сейчас времени', 'который час', 'сколько времени'),
        "youtube": ('ютуб', 'youtube'),
        "reddit": ('reddit', 'redit', 'рэдит', 'редит', 'реддит', 'рэддит'),
        "whatsapp": ('whatsapp', 'вацап', 'воцап', 'вотсап'),
        "music": ('soundcloud', 'музыка', 'саундклауд', 'саунклауд', 'музыку'),
        "weather": ('погода', 'за окном', 'градусов', 'влажность')
    }
}


# FUNCTIONS
def say(audio):  # translate text into voice (pyttsx3)
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()
    engine.stop()


def greet_me():  # welcomes user based on time
    current_hour = int(datetime.datetime.now().hour)
    if 0 <= current_hour <= 10:
        say('Доброе утро, сэр.')
    elif 11 <= current_hour <= 16:
        say('Добрый день, сэр.')
    else:
        say('Добрый вечер, сэр.')
    say('Я к вашим услугам.')


def current_weather():  # to find current weather details of any city using openweathermap api
    api_key = ''  # enter your API key here
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    city_name = ''  # give city name
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url, params={'units': 'metric', 'lang': 'ru'})
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = str(int(y["temp"]))
        current_humidity = str(int(y["humidity"]))
        z = x["weather"]
        weather_description = z[0]["description"]

        say('В данный момент за окном' + weather_description)
        say('Температура по градусам цельсия равна' + current_temperature)
        say('Также, сэр, если вас интересует влажность воздуха, данный показатель составляет'
            + current_humidity + 'процента')
    else:
        say('Сэр, произошла ошибка инициализации запроса. Пожалуйста, повторите еще раз')


def callback(recognizer, audio):
    try:
        query = recognizer.recognize_google(audio, language='ru-RU').lower()
        print(query)
        if query.startswith(opts['alias']):  # If the phrase begins with the name of the assistant
            command = query

            for x in opts['alias']:
                command = command.replace(x, '').strip()

            for x in opts['tbr']:
                command = command.replace(x, '').strip()

            # recognize(fuzzywuzzy) and execute command
            command = recognize_command(command)
            print(command)
            execute_command(command['command'])

    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        say('Сэр, возникла неизвестная ошибка. Начинаю диагностику системы.')


def recognize_command(command):
    rc = {'command': '', 'percent': 0}
    for c, v in opts['commands'].items():

        for x in v:
            vrt = fuzz.ratio(command, x)
            if vrt > rc['percent']:
                rc['command'] = c
                rc['percent'] = vrt
    return rc


def execute_command(command):
    if command == 'current_time':
        # say current time
        now = datetime.datetime.now()
        say('Сейчас' + str(now.hour) + ':' + str(now.minute))
    elif command == 'youtube':
        webbrowser.open('https://www.youtube.com')
    elif command == 'reddit':
        webbrowser.open('https://www.reddit.com')
    elif command == 'whatsapp':
        os.system(r'C:\Users\seric\AppData\Local\WhatsApp\WhatsApp.exe')
    elif command == 'music':
        webbrowser.open('https://soundcloud.com/discover')
    elif command == 'weather':
        current_weather()
    else:
        say('Повторите команду.')


# LAUNCH
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)

greet_me()
stop_listening = r.listen_in_background(m, callback)
while True:
    time.sleep(0.1)
