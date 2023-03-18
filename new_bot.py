"""""""""""" """"""""""""
""" --- Ядро бота --- """ # Отвечает за запуск бота и его поддержание
"""                   """
"""""""""""" """"""""""""

# Скрипт с ключиками к апишкам
# Набор команд для бота
from scripts import api, cmds

# Накидываем немного функционала, чтобы лаконичнее обрабатывать ботом сообщения и перекидывать на подпрограммы:

#   Application отвечает за запуск бота и его работу в целом
#   CommandHanlder ловит конкретную команду ботом (строка после '/')
#   MessageHanlder распознаёт некомандные сообщения, различая их типы через..
#   ..filters
#   ContextTypes распознаёт контекст (например, команду)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    )

#   Update содержит в себе инфу о сообщении, в т.ч. и сам его текст (update.message.text)
#   InlineKeyboardButton
#   InlineKeyboardMarkup
    

def main():

    # api.tg -- вызов скрипта api.py и его подпрограммы tg, возвращающей ключ тг-апи
    bot = Application.builder().token(api.tg()).build()
    print('Бот завёлся')

    # При вводе "/start" запускает функцию 'intro', ниже по той же логике
    bot.add_handler(CommandHandler("start", cmds.intro))
    bot.add_handler(CommandHandler("help", cmds.help))
    bot.add_handler(CommandHandler("h", cmds.help))
    bot.add_handler(CommandHandler("weather", cmds.weather))
    bot.add_handler(CommandHandler("butt", cmds.butt))
    bot.add_handler(MessageHandler(filters.ALL, cmds.text))

    # Поддерживает работу бота вплоть до его закрытия через Ctrl-C/Z в терминале
    # (надо бы добавить выключатель (а лучше перезагружатель) через сам бот)
    bot.run_polling()

main()