import telebot

bot = telebot.TeleBot('5761545857:AAFqY-qTVm9b4QjOyq8HWYIv5wBWvZfJG20')

def text(id, msg):
    bot.send_message(id, msg)
    print('Отправили \"' + msg + '\"')
    return 0