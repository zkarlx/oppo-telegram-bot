import telebot
import os
import webbrowser

# Получаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
if TOKEN is None:
    raise ValueError("❌ Переменная окружения TELEGRAM_TOKEN не установлена!")

# Создаём объект бота
bot = telebot.TeleBot(TOKEN)

user_lang = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_ru = telebot.types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru")
    btn_kz = telebot.types.InlineKeyboardButton("Қазақша 🇰🇿", callback_data="lang_kz")
    markup.add(btn_ru, btn_kz)

    bot.send_message(
        message.chat.id,
        "Здравствуйте! 👋\nСәлеметсіз бе! 👋\n\n"
        "Это бот OPPO 📱 / Бұл OPPO бот 📱\n\n"
        "Выберите язык / Тілді таңдаңыз",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_lang(call):

    if call.data == "lang_ru":
        user_lang[call.message.chat.id] = "ru"

        bot.send_message(
            call.message.chat.id,
            f"Здравствуйте {call.from_user.first_name}! 👋\n\n"
            "Чтобы получить список вопросов, введите команду /help."
        )

    elif call.data == "lang_kz":
        user_lang[call.message.chat.id] = "kz"

        bot.send_message(
            call.message.chat.id,
            f"Сәлеметсіз бе {call.from_user.first_name}! 👋\n\n"
            "/help командасын енгізіп, сұрақтар тізімін көре аласыз."
        )


@bot.message_handler(commands=['help'])
def help_command(message):

    lang = user_lang.get(message.chat.id, "ru")

    if lang == "ru":
        bot.send_message(
            message.chat.id,
            "📌 Часто задаваемые вопросы:\n\n"

            "1️⃣ Можете доставить заказ до 17:00? Когда будет доставка? Хотел узнать про доставку.\n\n"
            "2️⃣ Есть ли у вас магазин? Могу ли я потрогать или осмотреть телефон?\n\n"
            "3️⃣ Хотел узнать про эту модель.\n\n"
            "4️⃣ Хочу узнать про комплектацию телефона.\n\n"
            "5️⃣ Есть ли гарантия?\n\n"
            "6️⃣ Какая версия? Какая сборка? Верифицированный?\n\n"
            "7️⃣ Есть ли подарок?\n\n"
            "8️⃣ Когда поступит в продажу?\n\n"
            "9️⃣ Адрес сервисного центра?\n\n"
            "🔟 Хотел сделать возврат.\n\n"
            "1️⃣1️⃣ Можно ли купить телефон без подарков?\n\n"
            "1️⃣2️⃣ Дайте адрес склада.\n\n"

            "✏️ Отправьте номер вопроса."
        )

    else:
        bot.send_message(
            message.chat.id,
            "📌 Жиі қойылатын сұрақтар:\n\n"

            "1️⃣ Тапсырысты сағат 17:00-ге дейін жеткізе аласыздар ма? Жеткізу қашан болады? Жеткізу туралы білгім келеді.\n\n"
            "2️⃣ Сіздерде дүкен бар ма? Телефонды ұстап көруге немесе қарап шығуға бола ма?\n\n"
            "3️⃣ Осы модель туралы білгім келеді.\n\n"
            "4️⃣ Телефонның жиынтығы туралы білгім келеді.\n\n"
            "5️⃣ Кепілдік бар ма?\n\n"
            "6️⃣ Қандай нұсқа? Қандай жинақ? IMEI тексерілген бе?\n\n"
            "7️⃣ Сыйлық бар ма?\n\n"
            "8️⃣ Қашан сатылымға түседі?\n\n"
            "9️⃣ Сервистік орталықтың мекенжайы қандай?\n\n"
            "🔟 Қайтару жасағым келеді.\n\n"
            "1️⃣1️⃣ Телефонды сыйлықсыз сатып алуға бола ма?\n\n"
            "1️⃣2️⃣ Қойманың мекенжайын беріңіз.\n\n"

            "✏️ Сұрақ нөмірін жіберіңіз."
        )


@bot.message_handler(func=lambda message: message.text.isdigit())
def faq_answers(message):

    lang = user_lang.get(message.chat.id, "ru")

    if lang == "ru":
        if message.text == "1":
            bot.send_message(message.chat.id,
                "К сожалению, у нас нет собственных курьеров, доставкой занимается Kaspi Логистика. "
                "По срокам доставки вы можете уточнить, позвонив в Kaspi по номеру 9999."
            )
        elif message.text == "2":
            bot.send_message(message.chat.id,
                "К сожалению, у нас нет офлайн-точки. Продажи идут только через маркетплейс Kaspi, "
                "но вы можете оформить заказ самовывозом и забрать товар прямо со склада."
            )
        elif message.text == "3":
            bot.send_message(message.chat.id,
                "Подробную информацию о модели телефона вы можете посмотреть в приложении Kaspi "
                "в разделе «Характеристики»."
            )
        elif message.text == "4":
            bot.send_message(message.chat.id,
                "Комплектация телефона указана в разделе «Особенности и дополнительная информация»."
            )
        elif message.text == "5":
            bot.send_message(message.chat.id,
                "Гарантия — 1 год в электронном виде. Данные телефона зарегистрированы в базе OPPO."
            )
        elif message.text == "6":
            bot.send_message(message.chat.id,
                "Версия — глобальная (Европа), сборка — китайская. IMEI верифицирован на территории РК."
            )
        elif message.text == "7":
            bot.send_message(message.chat.id,
                "Все подарки, указанные в карточке товара, идут в комплекте. "
                "Подробнее можно посмотреть в разделе «Особенности и дополнительная информация»."
            )
        elif message.text == "8":
            bot.send_message(message.chat.id,
                "К сожалению, дата поступления в продажу неизвестна."
            )
        elif message.text == "9":
            bot.send_message(message.chat.id,
                "Адреса сервисных центров можно узнать на сайте:\n"
                "https://support.oppo.com/ru/service-center/"
            )
        elif message.text == "10":
            bot.send_message(message.chat.id,
                "Возврат возможен только в случае заводского брака. "
                "Для этого необходимо обратиться в ближайший сервисный центр и получить акт о браке."
            )
        elif message.text == "11":
            bot.send_message(message.chat.id,
                "Вы можете поискать в нашем магазине товар без подарков. "
                "Если такая позиция есть — да, можно купить."
            )
        elif message.text == "12":
            bot.send_message(message.chat.id,
                "Адрес склада можно узнать при оформлении покупки с самовывозом."
            )
        else:
            bot.send_message(message.chat.id,
                "Если ваш вопрос другой, пожалуйста, обратитесь в колл-центр по номеру +7 707 688 10 10"
            )

    else:
        if message.text == "1":
            bot.send_message(message.chat.id,
                "Өкінішке орай, біздің өз курьерлеріміз жоқ, жеткізумен Kaspi Логистика айналысады. "
                "Жеткізу мерзімін Kaspi-дің 9999 нөміріне қоңырау шалып нақтылай аласыз."
            )
        elif message.text == "2":
            bot.send_message(message.chat.id,
                "Өкінішке орай, бізде офлайн дүкен жоқ. Сату тек Kaspi маркетплейсі арқылы жүзеге асады, "
                "бірақ сіз самовывоз рәсімдеп, тауарды қоймадан өзіңіз алып кете аласыз."
            )
        elif message.text == "3":
            bot.send_message(message.chat.id,
                "Телефон моделі туралы толық ақпаратты Kaspi қосымшасындағы "
                "«Сипаттамалары» бөлімінен көре аласыз."
            )
        elif message.text == "4":
            bot.send_message(message.chat.id,
                "Телефонның жиынтығы «Ерекшеліктер және қосымша ақпарат» бөлімінде көрсетілген."
            )
        elif message.text == "5":
            bot.send_message(message.chat.id,
                "Кепілдік — 1 жыл электрондық түрде. Телефон деректері OPPO базасында тіркелген."
            )
        elif message.text == "6":
            bot.send_message(message.chat.id,
                "Нұсқа — жаһандық (Еуропа), жинағы — қытайлық. "
                "IMEI Қазақстан аумағында тексерілген."
            )
        elif message.text == "7":
            bot.send_message(message.chat.id,
                "Өнім картасында көрсетілген барлық сыйлықтар жиынтықта бар. "
                "Толығырақ «Ерекшеліктер және қосымша ақпарат» бөлімінен көре аласыз."
            )
        elif message.text == "8":
            bot.send_message(message.chat.id,
                "Өкінішке орай, сатылымға шығу күні белгісіз."
            )
        elif message.text == "9":
            bot.send_message(message.chat.id,
                "Сервистік орталықтардың мекенжайын мына сайттан білуге болады:\n"
                "https://support.oppo.com/ru/service-center/"
            )
        elif message.text == "10":
            bot.send_message(message.chat.id,
                "Қайтару тек зауыттық ақау болған жағдайда ғана мүмкін. "
                "Ол үшін ең жақын сервистік орталыққа барып, ақау туралы акт алу қажет."
            )
        elif message.text == "11":
            bot.send_message(message.chat.id,
                "Дүкенімізден сыйлықсыз тауар бар-жоғын қарап көре аласыз. "
                "Егер ондай позиция бар болса — иә, сатып алуға болады."
            )
        elif message.text == "12":
            bot.send_message(message.chat.id,
                "Қойманың мекенжайын тапсырыс беріп, самовывоз рәсімдеу кезінде біле аласыз."
            )
        else:
            bot.send_message(message.chat.id,
                "Егер сұрағыңыз басқа болса, колл-орталыққа +7 707 688 10 10 нөміріне хабарласыңыз."
            )


@bot.message_handler(func=lambda message: not message.text.isdigit() and not message.text.startswith('/'))
def unknown_message(message):
    lang = user_lang.get(message.chat.id, "ru")
    if lang == "ru":
        bot.send_message(message.chat.id,
            "Если ваш вопрос другой, пожалуйста, обратитесь в колл-центр по номеру +7 707 688 10 10"
        )
    else:
        bot.send_message(message.chat.id,
            "Егер сұрағыңыз басқа болса, колл-орталыққа +7 707 688 10 10 нөміріне хабарласыңыз."
        )

bot.polling(non_stop=True)
