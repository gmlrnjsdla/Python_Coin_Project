import telegram
from telegram.ext import Updater, MessageHandler, Filters

telegram_bot = telegram.Bot(token='5580478919:AAFEtLVmb7ZH1dKzMkCp4aMCI9G_Aif4pQY')
chat_id = 5400256265

telegram_bot.sendMessage(chat_id=chat_id, text="안녕하세요")
