import telebot
import requests
import json

bot = telebot.TeleBot("7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE")
API = 'afc83e7c69c5f3b128565b8c97d7e3c9'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напиши мне город и скажу какая погода там!')

@bot.message_handler(content_types=['text']) #декаратор - он “подключает” функцию ниже к боту. Функция будет вызываться, когда придёт текстовое сообщение.
def get_weather(message): #бот передает объект сообщение пользователя в переменную message
    city = message.text.strip().lower() #strip - удаляет пробелы, если например в скобки передать 'A', Это уберёт букву "A" с краёв строки. lower() - переводит строку в нижний регистр.
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric') #requests.get()Функция из библиотеки requests. Отправляет HTTP GET запрос. () — вызов функции.
    #res - переменная. В неё сохраняется объект ответа сервера.
    if res.status_code == 200: #res - объект ответа, status_code - атрибут, 200 - значит 'успешно'
        data = json.loads(res.text) #res.text - атрибут, содержит текст ответа от сервера, json.loads() - функция, преобразует JSON строку → в словарь Python. data - переменная, теперь это словарь
        temp = data["main"]["temp"] #Берём значение по ключу "main". Из вложенного словаря берём "temp". Сохраняем температуру в переменную temp
        bot.reply_to(message, f'Сейчас погода {temp}')
        if temp > 5.0:
            image = 'sun.png'
        else:
            image = 'sunny.jpg'
        file = open('./' + image, 'rb') #Открывает картинку из папки, чтобы бот мог её отправить. open()-встроенная функция в Python, говорит 'открой файл на этом компе'
        #'./' - это папка, говорит 'ищи файл в этой же папке, где лежит программа'; image-переменная с картинкой; + - соединеие строки, получается './sun.png'; rb - только для чтения
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан не верно')

bot.polling(non_stop=True) #чтоб бот работал постоянно