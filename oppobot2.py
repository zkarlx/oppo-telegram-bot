import telebot
import ollama

BOT_TOKEN = "7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE"

bot = telebot.TeleBot(BOT_TOKEN)

FAQ = {
    "доставка": (
        "К сожалению, у нас нет собственных курьеров, доставкой занимается Kaspi Логистика. По срокам уточняйте по номеру 9999.",
        "Өкінішке орай, өз курьеріміз жоқ, жеткізумен Kaspi Логистика айналысады. Жеткізу уақытын 9999 нөміріне хабарласып біле аласыз."
    ),
    "магазин": (
        "К сожалению, у нас нет офлайн-точки. Продажи идут только через маркетплейс Kaspi.",
        "Өкінішке орай, офлайн дүкен жоқ. Сату тек Kaspi маркетплейсі арқылы жүреді."
    ),
    "модель": (
        "Подробную информацию о модели телефона смотрите в приложении Kaspi в разделе «Характеристики».",
        "Телефон моделінің толық ақпаратын Kaspi қосымшасындағы «Сипаттамалары» бөлімінен көре аласыз."
    ),
    "комплектация": (
        "Комплектация указана в разделе «Особенности и дополнительная информация».",
        "Құрамы «Ерекшеліктер және қосымша ақпарат» бөлімінде көрсетілген."
    ),
    "гарантия": (
        "Гарантия — 1 год в электронном виде. Данные телефона зарегистрированы в базе OPPO.",
        "Кепілдік — 1 жыл электрондық түрде. Телефон деректері OPPO базасында тіркелген."
    ),
    "версия": (
        "Версия — глобальная (Европа), сборка — китайская. IMEI верифицирован на территории РК.",
        "Нұсқа — жаһандық (Еуропа), жинағы — Қытай. IMEI Қазақстан аумағында тексерілген."
    ),
    "подарок": (
        "Все подарки, указанные в карточке товара, идут в комплекте. Подробнее в разделе «Особенности и дополнительная информация».",
        "Өнім картасында көрсетілген барлық сыйлықтар құрамда бар. Толығырақ «Ерекшеліктер және қосымша ақпарат» бөлімінде."
    ),
    "поступление": (
        "К сожалению, дата поступления в продажу неизвестна.",
        "Өкінішке орай, сатуға шығу күні белгісіз."
    ),
    "сервис": (
        "Адреса сервисных центров можно узнать на сайте: https://support.oppo.com/ru/service-center/",
        "Сервистік орталықтардың мекен-жайын мына сайттан білуге болады: https://support.oppo.com/ru/service-center/"
    ),
    "возврат": (
        "Возврат возможен только в случае заводского брака. Обратитесь в ближайший сервисный центр.",
        "Қайтару тек зауыт ақауы болған жағдайда мүмкін. Ең жақын сервис орталығына хабарласыңыз."
    ),
    "склад": (
        "Адрес склада можно узнать при оформлении покупки с самовывозом.",
        "Қойма мекенжайын тапсырыс беріп, өзіңіз алып кету кезінде біле аласыз."
    )
}

user_lang = {}


def ask_ai(user_text, lang="ru"):
    # Передаем FAQ как контекст
    context = "\n".join([f"{k}: {v[0] if lang == 'ru' else v[1]}" for k, v in FAQ.items()])

    # Очень строгая инструкция (System Prompt)
    system_instruction = (
        f"Ты помощник поддержки OPPO. Отвечай ТОЛЬКО на языке: {lang}. "
        f"Используй эти факты: {context}. "
        "Ответ должен быть коротким (не более 20 слов). Если ответа в фактах нет, скажи позвать менеджера."
    )

    try:
        # Используем быструю модель llama3.2:1b
        response = ollama.chat(model='llama3.2:1b', messages=[
            {'role': 'system', 'content': system_instruction},
            {'role': 'user', 'content': user_text},
        ])
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Ошибка: {e}")
        return "Извините, произошла ошибка. Менеджер скоро ответит."


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_ru = telebot.types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru")
    btn_kz = telebot.types.InlineKeyboardButton("Қазақша 🇰🇿", callback_data="lang_kz")
    markup.add(btn_ru, btn_kz)
    bot.send_message(message.chat.id, "Выберите язык / Тілді таңдаңыз", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_lang(call):
    if call.data == "lang_ru":
        user_lang[call.message.chat.id] = "ru"
        bot.send_message(call.message.chat.id,
                         "Вы выбрали русский язык 🇷🇺\n\nПривет! 👋\nЯ бот поддержки OPPO. Задайте свой вопрос про доставку, гарантию или товар.")
    elif call.data == "lang_kz":
        user_lang[call.message.chat.id] = "kz"
        bot.send_message(call.message.chat.id,
                         "Сіз қазақ тілін таңдадыңыз 🇰🇿\n\nСәлем! 👋\nМен OPPO қолдау ботымын. Жеткізу, кепілдік немесе тауар туралы сұрағыңызды қойыңыз.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    lang = user_lang.get(message.chat.id, "ru")
    user_text = message.text.lower()

    # 1. Сначала ищем точное совпадение слова (работает мгновенно)
    for key, (text_ru, text_kz) in FAQ.items():
        if key in user_text:
            bot.send_message(message.chat.id, text_ru if lang == "ru" else text_kz)
            return

    # 2. Если точного слова нет — включаем ИИ
    bot.send_chat_action(message.chat.id, 'typing')
    ai_answer = ask_ai(message.text, lang)
    bot.send_message(message.chat.id, ai_answer)


print("Бот запущен на модели Llama 3.2 1B...")
bot.polling(non_stop=True)