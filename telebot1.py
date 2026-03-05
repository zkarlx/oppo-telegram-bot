import telebot
import webbrowser

bot = telebot.TeleBot("7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE") #токен тг-бота

@bot.message_handler(commands=['site', 'website']) #при введении этих команд будет открываться сайт
def site(message):
    webbrowser.open('https://www.youtube.com/')

@bot.message_handler(commands=['start']) #message_handler - это обработчик сообщений. Запускается при командах которые находятся в 'command'
def main(message): #message - параметр который принимает информацию о конкретном сообщении, которую прислал пользователь.
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!') #message.chat.id - сохраняет id чата и при вызове функции понимает куда отправлять сообщение

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id,'<b>Help information</b>', parse_mode='html') #с помошью 3 аргумента "parse_mode='html'" мы можем редактировать текст с помощью html команд

@bot.message_handler() #это обработчик всех сообщений. Он говорит боту: «Когда придёт любое сообщение — вызывай функцию info
def info(message): #message — это объект сообщения от пользователя.
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')
    elif message.text.lower() == 'id': #ставим эту функцию вниз т.к. если он будет стоять первым то остальные обработчики не будут работать.
        bot.reply_to(message, f'ID: {message.from_user.id}') #будет ОТВЕЧАТЬ на последнее сообщение и писать ID.

bot.polling(non_stop=True) #чтоб бот работал постоянно