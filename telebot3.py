import telebot
import sqlite3

bot = telebot.TeleBot("7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE")

user_data = {} #словарь для хранения имя пользователя во время регистрации

@bot.message_handler(commands=['start'])
def start(message):
    bot.clear_step_handler_by_chat_id(message.chat.id)

    conn = sqlite3.connect('oppo.sql') #для соединении с файлом oppo.sql
    cur = conn.cursor() #объект для выполнения SQL-команд, чтоб он выполнял соединяем его с conn

    cur.execute(''' 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        pass TEXT
    )
    ''') #execute - говорит cur чтоб он выполнил SQL код в скобках
    conn.commit() #сохранить изменения
    cur.close() #закрыть соединение
    conn.close()

    bot.send_message(message.chat.id, 'Введите ваше имя') #отправка сообщения
    bot.register_next_step_handler(message, user_name) #следующее сообщение этого пользователя отправить в функцию user_name


def user_name(message): #сюда попадает сообщение с именем
    user_data[message.chat.id] = message.text.strip() #strip - убирает пробелы, сохраняем в словарь по его chat.id
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message): #пароль попадает сюда
    password = message.text.strip() #убираем пробелы
    name = user_data.get(message.chat.id) #берем сохраненное имя

    conn = sqlite3.connect('oppo.sql') #подключаемся к базе
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, password)) #добавляем имя и пароль в базу, '?' - безопасный способ передачи данных.
    conn.commit() #сохраняем изменения и закрываем базу
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup() #создаём объект клавиатуры.
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users')) #callback_data - будет сработвать при нажатии на кнопку
    markup.add(telebot.types.InlineKeyboardButton('Очистить список', callback_data='clear'))
    bot.send_message(message.chat.id, 'Вы зарегистрированы!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'users') #этот обработчик срабатывает только если: callback_data == 'users'
def callback(call):
    conn = sqlite3.connect('oppo.sql')
    cur = conn.cursor()

    cur.execute('SELECT name FROM users') #берём все имена из базы
    users = cur.fetchall() #fetchall() возвращает список

    info = ''
    for el in users: #el — текущий элемент списка users (каждый пользователь)
        info += f'Имя: {el[0]}\n' #проходимся по всем пользователям и добавляем их имена в строку.
    # берём имя пользователя из кортежа (позиция 0) и добавляем в строку
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


@bot.callback_query_handler(func=lambda call: call.data == 'clear')
def clear_users(call):
    conn = sqlite3.connect('oppo.sql')
    cur = conn.cursor()

    cur.execute("DELETE FROM users")
    conn.commit()

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, "Список пользователей очищен")

bot.polling(non_stop=True) #чтоб бот работал постоянно