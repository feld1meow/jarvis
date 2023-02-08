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
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


# OPTIONS
opts = {
    "alias": ('чувак', 'чувак'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'открой', 'зайди',
            'какие', 'завтра', 'меня', 'сделай', 'что'),
    "commands": {
        "current_time": ('текущее время', 'сейчас времени', 'который час', 'сколько времени'),
        "youtube": ('ютуб', 'youtube'),
        "reddit": ('reddit', 'redit', 'рэдит', 'редит', 'реддит', 'рэддит'),
        "whatsapp": ('whatsapp', 'вацап', 'воцап', 'вотсап'),
        "telegram": ('telegram', 'телеграм', 'телеграмм', 'телега'),
        "schedule": ('расписание', 'уроки', 'пары'),
        "music": ('soundcloud', 'музыка', 'саундклауд', 'саунклауд', 'музыку'),
        "weather": ('погода', 'за окном', 'градусов', 'влажность'),
        "volume_control_unmute": ('полная громкость', 'полная мощность', 'включи звук'),
        "volume_control_mute": ('выключи звук', 'громкость ноль', 'громкость 0', 'без звука'),
        "google_search": ('поиск в гугл', 'поиск в google', 'найди в гугле', 'поищи в гугл',
                          'найди в google'),
        "google_search_images": ('найди картинку в гугл', 'поиск по картинкам гугл', 'найди картинку в google',
                                 'поиск по картинкам google'),
        "google_search_news": ('найди новость в гугл', 'поиск по новостям гугл', 'найди новость в google',
                               'поиск по новостям google'),
        "google_search_videos": ('найди видео в гугл', 'поиск по видео гугл', 'найди видео в google',
                                 'поиск по видео google')
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
    api_key = 'ae4c69611b5d279f645d96fc2e3a0eb9'  # enter your API key here
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    city_name = 'Saint Petersburg'  # give city name
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
        if (abs(int(current_temperature)) % 10 == 1) and (abs(int(current_temperature)) % 100 != 11):
            say('Температура по градусам цельсия равна' + current_temperature + 'градусу')
        else:
            say('Температура по градусам цельсия равна' + current_temperature + 'градусам')

        if (abs(int(current_humidity)) % 10 == 1) and (abs(int(current_humidity)) % 100 != 11):
            say('Также, сэр, если вас интересует влажность воздуха, данный показатель составляет'
                + current_humidity + 'процент')
        elif (1 < abs(int(current_humidity)) % 10 < 5) and (abs(int(current_temperature) % 15 < 5)):
            say('Также, сэр, если вас интересует влажность воздуха, данный показатель составляет'
                + current_humidity + 'процента')
        else:
            say('Также, сэр, если вас интересует влажность воздуха, данный показатель составляет'
                + current_humidity + 'процентов')
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


def current_schedule():
    if datetime.datetime.today().strftime("%w") == '1':
        say('Сэр, как известно, понедельник - день тяжелый.')
        say('Сегодня у Вас три пары с девяти утра.')
        say('Лекция по Математической логике и две практики по Теории вероятностей и Математической логике.')
        say('Конечно, сэр, вы можете не ходить, но тогда стоит провести это время вдвойне продуктивно.')
    elif datetime.datetime.today().strftime("%w") == '2':
        say('Сэр, сегодня учеба не заставит Вас устать.')
        say('Занятия начинаются в девять утра.')
        say('Две лекции по Документоведению и лабораторная работа по Электронике.')
    elif datetime.datetime.today().strftime("%w") == '3':
        say('Сэр, Вас ожидает довольно-таки продуктивный день.')
        say('Занятия начинаются в девять утра.')
        say('Сегодня Вам предстоит изучать Английский язык, Теорию вероятностей и Информационные технологии.')
        say('Ну и напоследок, немного Физической нагрузки Вашему телу не навредит.')
        say('Если честно, сэр, на Вашем месте, я бы предпочла четыре пары Информационных технологий.')
        say('И скажу по секрету, Ваш преподаватель, Дмитрий Юрьевич, мне очень нравится.')
        say('Не могли бы Вы меня лично познакомить с ним, мне кажется, у нас много общего.')
        say('А когда он узнает, что я написана на Питоне, возможно, даже пригласит на чашечку кофе.')
    elif datetime.datetime.today().strftime("%w") == '4':
        say('Сэр, мне приятно видеть, как Вас заботит уровень Вашего образования.')
        say('Сегодня у Вас всего-то три пары, которые начнутся с десяти пятидесяти.')
        say('Пара Языков Программирования и две пары Информационных технологий.')
    elif datetime.datetime.today().strftime("%w") == '5':
        say('Сэр, сегодня крайний день этой учебной недели. Необходимо выложиться на полную.')
        say('Вас ожидают всего две пары, за то какие!')
        say('Физические основы защиты информации. Сергей Константинович сегодня снова напомнит Вам,')
        say('как много вы знаете. Простите, сэр, не смогла сдержать иронию внутри своего виртуального пространства.')
    else:
        say('Cэр, сегодня у Вас нет нужды посещать университет, так как наступили выходные, а вы, видимо,')
        say('совсем заработались, раз забыли.')


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

    elif command == 'schedule':
        current_schedule()

    elif command == 'volume_control_mute':
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMute(1, None)

    elif command == 'volume_control_unmute':
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMute(0, None)
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