import telebot
from rapidfuzz import fuzz

BOT_TOKEN = "7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE"
bot = telebot.TeleBot(BOT_TOKEN)

FAQ = {
    "delivery": {
        "keywords": ["доставка", "заказ", "когда придет", "привезут", "курьер", "отправка"],
        "ru": "К сожалению, у нас нет собственных курьеров, доставкой занимается Kaspi Логистика. По срокам уточняйте по номеру 9999.",
        "kz": "Өкінішке орай, өз курьеріміз жоқ, жеткізумен Kaspi Логистика айналысады. Жеткізу уақытын 9999 нөміріне хабарласып біле аласыз."
    },
    "shop": {
        "keywords": ["магазин", "офлайн", "адрес магазина", "где вы находитесь", "точка продаж"],
        "ru": "К сожалению, у нас нет офлайн-точки. Продажи идут только через маркетплейс Kaspi.",
        "kz": "Өкінішке орай, офлайн дүкен жоқ. Сату тек Kaspi маркетплейсі арқылы жүреді."
    },
    "model": {
        "keywords": ["модель", "характеристики", "параметры", "описание телефона"],
        "ru": "Подробную информацию о модели телефона смотрите в приложении Kaspi в разделе «Характеристики».",
        "kz": "Телефон моделінің толық ақпаратын Kaspi қосымшасындағы «Сипаттамалары» бөлімінен көре аласыз."
    },
    "complect": {
        "keywords": ["комплектация", "в комплекте", "что входит", "состав коробки"],
        "ru": "Комплектация указана в разделе «Особенности и дополнительная информация».",
        "kz": "Құрамы «Ерекшеліктер және қосымша ақпарат» бөлімінде көрсетілген."
    },
    "guarantee": {
        "keywords": ["гарантия", "гарантии", "ремонт", "сервисный случай"],
        "ru": "Гарантия — 1 год в электронном виде. Данные телефона зарегистрированы в базе OPPO.",
        "kz": "Кепілдік — 1 жыл электрондық түрде. Телефон деректері OPPO базасында тіркелген."
    },
    "version": {
        "keywords": ["версия", "глобальная", "китайская сборка", "imei"],
        "ru": "Версия — глобальная (Европа), сборка — китайская. IMEI верифицирован на территории РК.",
        "kz": "Нұсқа — жаһандық (Еуропа), жинағы — Қытай. IMEI Қазақстан аумағында тексерілген."
    },
    "gift": {
        "keywords": ["подарок", "подарки", "акция", "бонус"],
        "ru": "Все подарки, указанные в карточке товара, идут в комплекте. Подробнее в разделе «Особенности и дополнительная информация».",
        "kz": "Өнім картасында көрсетілген барлық сыйлықтар құрамда бар. Толығырақ «Ерекшеліктер және қосымша ақпарат» бөлімінде."
    },
    "arrival": {
        "keywords": ["поступление", "когда будет", "когда появится", "наличие"],
        "ru": "К сожалению, дата поступления в продажу неизвестна.",
        "kz": "Өкінішке орай, сатуға шығу күні белгісіз."
    },
    "service": {
        "keywords": ["сервис", "сервисный центр", "где ремонт", "куда обратиться"],
        "ru": "Адреса сервисных центров можно узнать на сайте: https://support.oppo.com/ru/service-center/",
        "kz": "Сервистік орталықтардың мекен-жайын мына сайттан білуге болады: https://support.oppo.com/ru/service-center/"
    },
    "return": {
        "keywords": ["возврат", "обмен", "вернуть", "брак"],
        "ru": "Возврат возможен только в случае заводского брака. Обратитесь в ближайший сервисный центр.",
        "kz": "Қайтару тек зауыт ақауы болған жағдайда мүмкін. Ең жақын сервис орталығына хабарласыңыз."
    },
    "warehouse": {
        "keywords": ["склад", "самовывоз", "забрать самому", "адрес склада"],
        "ru": "Адрес склада можно узнать при оформлении покупки с самовывозом.",
        "kz": "Қойма мекенжайын тапсырыс беріп, өзіңіз алып кету кезінде біле аласыз."
    },
    "technical": {
        "keywords": [
            "лагает", "глючит", "тормозит", "зависает", "не работает",
            "қатады", "істемейді", "жұмыс істемейді", "қатып қалады"
        ],
        "ru": (
            "Если телефон работает некорректно, рекомендуем выполнить перезагрузку устройства. "
            "Если проблема сохраняется — обратитесь в сервисный центр OPPO: "
            "https://support.oppo.com/ru/service-center/"
        ),
        "kz": (
            "Телефон дұрыс жұмыс істемесе, құрылғыны қайта іске қосып көріңіз. "
            "Мәселе шешілмесе, OPPO сервис орталығына жүгініңіз: "
            "https://support.oppo.com/ru/service-center/"
        )
    }
}


user_lang = {}

def find_best_match(user_text):
    best_score = 0
    best_answer = None

    for item in FAQ.values():
        for keyword in item["keywords"]:
            score = fuzz.partial_ratio(keyword, user_text)
            if score > best_score:
                best_score = score
                best_answer = item

    if best_score > 70:
        return best_answer
    return None


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_ru = telebot.types.InlineKeyboardButton("Русский 🇷🇺", callback_data="ru")
    btn_kz = telebot.types.InlineKeyboardButton("Қазақша 🇰🇿", callback_data="kz")
    markup.add(btn_ru, btn_kz)
    bot.send_message(message.chat.id, "Выберите язык / Тілді таңдаңыз", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def set_language(call):
    user_lang[call.message.chat.id] = call.data

    if call.data == "ru":
        bot.send_message(call.message.chat.id, "Вы выбрали русский язык 🇷🇺")
        bot.send_message(
            call.message.chat.id,
            "Здравствуйте! 👋\n"
            "Я бот поддержки OPPO.\n"
            "Вы можете задать вопрос про доставку, гарантию, склад, сервис и т.д.\n"
            "Если вопрос нестандартный — я передам его менеджеру."
        )
    else:
        bot.send_message(call.message.chat.id, "Сіз қазақ тілін таңдадыңыз 🇰🇿")
        bot.send_message(
            call.message.chat.id,
            "Сәлем! 👋\n"
            "Мен OPPO қолдау ботымын.\n"
            "Сіз жеткізу, кепілдік, қойма, сервис туралы сұрай аласыз.\n"
            "Егер сұрақ стандартты болмаса — менеджерге жіберемін."
        )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    lang = user_lang.get(message.chat.id, "ru")
    user_text = message.text.lower()

    # благодарность
    if any(word in user_text for word in ["спасибо", "рахмет", "благодарю"]):
        bot.send_message(message.chat.id,
                         "Рады помочь! 😊" if lang=="ru"
                         else "Көмегіміз тигеніне қуаныштымыз! 😊")
        return

    result = find_best_match(user_text)

    if result:
        bot.send_message(message.chat.id, result[lang])
    else:
        bot.send_message(message.chat.id,
                         "Ваш вопрос передан менеджеру." if lang=="ru"
                         else "Сұрағыңыз менеджерге жіберілді.")

bot.polling(non_stop=True)