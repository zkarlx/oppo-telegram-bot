from aiogram import Bot, Dispatcher, executor, types


bot = Bot("7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE")
dp = Dispatcher(bot)




executor.start.polling(dp)

#bot = telebot.TeleBot("7788684334:AAGrLwioLd2_4Ph8Rq7Acu1WQrxu8mTXVvE")
#bot.polling(non_stop=True)