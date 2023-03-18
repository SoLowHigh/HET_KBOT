""""""""""" """""""""""
""" --- Команды --- """ # Зачем async? Зачем await? Да хрен его знает, иначе не работает тупо
"""                 """
""""""""""" """""""""""

from telegram.ext import (
    ContextTypes # определяет контект (например, "команда")
)

from telebot.types import (
    Update # содержит всякую инфу о сообщении (например, ИД и имя юзера и текст)
)

# Буфер памяти для запоминания аргумента команды
# По идее, лучше держать не в одной переменной,
#   а в словаре с чётким соответсвием id <-> argue
argue = ''


# start
async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print('Обрабатываем start')
    print(update.message.text)
    await update.message.reply_text('Можешь глянуть что-нибудь \
                                    <a href="http://solowhigh.github.io">ещё</a>',\
                                          parse_mode='HTML')


# h or help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('docs/help', 'r') as f_cmd:
        help_text = f_cmd.read()

    print('Обрабатываем help от', update.message.chat.username)
    await update.message.reply_text(help_text)


# weather
from . import temperature
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print('Обрабатываем weather')
    global argue
    argue = update.message.text.replace('/weather ', '')
    print('\'',argue,'\'')

    # Если команда подана с аргументом
    if argue == '/weather':
        await update.message.reply_text(temperature.main(argue))

    # Если команда подана без аргумента
    else:
        await update.message.reply_text('В каком городе нужно узнать температуру?')


# h (if testing)
async def testFunc(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(str(update))


# Возможно, кнопка (пока не вызывается)
async def butt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print('Обрабатываем butt')
    keyboard = [[
        InlineKeyboardButton("Option 1", callback_data="1"),
        InlineKeyboardButton("Option 2", callback_data="2"),
        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


# Обрботка некомандного текста
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '\\':
        await update.message.reply_text(str(update))
        return

    print('Обрабатываем текст')
    global argue
    print('\'',argue,'\'')
    if argue != '':
        await update.message.reply_text(temperature.main(argue))
        argue = ''
    else:
        await update.message.reply_text(update.message.text[::-1])