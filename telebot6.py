import telebot
import requests #для отправки HTTP-запросов к API
from telebot import types #для кнопок

bot = telebot.TeleBot("7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE")

# храним данные пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму!')
    bot.register_next_step_handler(message, summa)


def summa(message):
    try:
        amount = float(message.text.strip())
    except ValueError: #ValueError - если введено не число
        bot.send_message(message.chat.id, 'Некорректный формат, введите число')
        bot.register_next_step_handler(message, summa)
        return

    if amount <= 0: #при введении числа меньше 0, срабатывает это
        bot.send_message(message.chat.id, 'Сумма должна быть больше 0')
        bot.register_next_step_handler(message, summa)
        return

    # сохраняем сумму пользователя
    user_data[message.chat.id] = amount

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
    btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
    btn3 = types.InlineKeyboardButton('USD/KZT', callback_data='USD/KZT')
    btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True) #эта функция срабатывает каждый раз, когда пользователь нажимает inline-кнопку.
def callback(call): #call — это объект, который содержит: call.data — данные кнопки (например USD/KZT), call.message — сообщение, к которому относится кнопка, call.id — id нажатия
    bot.answer_callback_query(call.id) #подтверждение нажатия

    chat_id = call.message.chat.id #это ID пользователя (или чата), чтобы понимать, кому отвечать.

    if chat_id not in user_data: #user_data = {chat.id - 12345678: сумма которую ввел пользователь - 100.0} Если в словаре нет такого chat_id То есть если пользователь ещё не вводил сумму.
        bot.send_message(chat_id, "Сначала введите сумму")
        return

    if call.data != 'else': #если пользователь нажал на кнопку USD/EUR или другие 2 кнопки то:
        base, target = call.data.split('/') #разделяем строку по / и base = USD, target = EUR.

        convert_currency(chat_id, base, target) #дальше вызывается эта команда, то есть сразу идём считать курс.

    else:
        bot.send_message(chat_id, 'Введите пару валют через / например USD/KZT') #если пользователь нажимает "Другое значение" то выполняется это и:
        bot.register_next_step_handler(call.message, my_currency) #срабатывает функция my_currency


def my_currency(message):
    chat_id = message.chat.id #это ID пользователя (или чата), чтобы понимать, кому отвечать.

    try:
        base, target = message.text.upper().split('/')
        convert_currency(chat_id, base.strip(), target.strip())
    except:
        bot.send_message(chat_id, 'Неверный формат. Пример: USD/KZT')
        bot.register_next_step_handler(message, my_currency)


def convert_currency(chat_id, base, target):
    amount = user_data.get(chat_id) #берём сохранённую сумму

    try:
        url = f"https://open.er-api.com/v6/latest/{base}" #делаем запрос к API, если base = USD, запрос будет: https://open.er-api.com/v6/latest/USD
        response = requests.get(url)
        data = response.json()

        if data['result'] != 'success': #проверяем, успешно ли API ответил
            raise Exception("Ошибка API") #если что-то не так — вызываем ошибку.

        rate = data['rates'].get(target) #получаем курс нужной валюты, например USD → KZT = 470

        if rate is None: #если такой валюты нет
            raise Exception("Валюта не найдена")

        result = amount * rate #считаем результат

        bot.send_message(chat_id,f'{amount} {base} = {round(result, 2)} {target}\n\nВведите новую сумму')

        # очищаем данные пользователя
        user_data.pop(chat_id, None)

        bot.register_next_step_handler_by_chat_id(chat_id, summa)

    except Exception as e:  #Если что-то пошло не так: API не работает валюта не существует интернет отключён Сработает:
        print(e)
        bot.send_message(chat_id, 'Ошибка конвертации или такой валюты нет')
        bot.register_next_step_handler_by_chat_id(chat_id, summa)


bot.polling(non_stop=True)


