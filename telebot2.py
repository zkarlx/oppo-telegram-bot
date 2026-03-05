import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot("7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE") #токен тг-бота

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup() #кнопки ReplyKeyboard - снизу автоматом будут стоять кнопки
    btn1 = (types.KeyboardButton('Перейти на сайт'))
    markup.row(btn1)
    btn2 = (types.KeyboardButton('Удалить фото'))
    btn3 = (types.KeyboardButton('Изменить текст'))
    markup.row(btn2, btn3)
    photo_file = open('./logo.jpg', 'rb')
    bot.send_photo(message.chat.id, photo_file, reply_markup=markup)
    #bot.send_audio(message.chat.id, photo_file, reply_markup=markup)
    #bot.send_video(message.chat.id, photo_file, reply_markup=markup)
    #bot.send_message(message.chat.id, 'Привет', reply_markup=markup) #при отправке /start бот будет отвечать 'Привет' и снизу появятся кнопки из за - reply_markup=markup
    bot.register_next_step_handler(message, on_click) #следующее сообщение пользователя обработай функцией on_click

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Сайт открыт')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Фото удалено')


@bot.message_handler(content_types= ['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup() #это контейнер для кнопок, в него мы добавляем кнопки, которые будут отображаться прямо под сообщением
    btn1 = (types.InlineKeyboardButton('Перейти на сайт', url='https://youtube.com')) #создали переменную btn1 чтобы хранить в нем код первой кнопки
    markup.row(btn1)
    btn2 = (types.InlineKeyboardButton('Удалить фото', callback_data='delete'))
    btn3 = (types.InlineKeyboardButton('Изменить текст', callback_data='edit'))
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True) #ловит события кнопок и 'func=...' - говорит что любая кнопка с callback_data попадёт сюда.
def callback_message(callback): #callback - это объект в которм есть - callback.data(callback_data), callback.message и т.д. то есть это как объект 'message' только для кнопок
    if callback.data == 'delete': #если кнопка 'Удалить фото'
        bot.delete_message(callback.message.chat.id, callback.message.message_id -1) #то делается это, ID чата --> ID сообщения с кнопкой --> -1 удаляется пред сообщение
    elif callback.data == 'edit': #если кнопка 'Изменить текст'
        bot.edit_message_text('Изменить текст', callback.message.chat.id, callback.message.message_id) #мы изменяем текст сообщения, к которому прикреплена кнопка.


bot.polling(non_stop=True) #чтоб бот работал постоянно