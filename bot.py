# Импортируем скрипт с набором команд для бота
from scripts import cmds
# Импортируем бота
import telebot
# Импортируем кнопки для бота
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

bot = telebot.TeleBot('5761545857:AAFqY-qTVm9b4QjOyq8HWYIv5wBWvZfJG20')

@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id, 'О, привет! А я тебя.. не, не знаю')

    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Update.message.reply_text('Please choose:', reply_markup=reply_markup)
    
@bot.message_handler(content_types=['text'])

#   Определяет тип сообщения
#   (аргумент; команда; другое)
def msg_type(message):
    print('     from: '+message.from_user.username)
    print('  message: '+message.text)
    global flag 
    print('     type:', end=' ')

    # Определяет наличие аргумента у команды
    if flag['cmd_arg'] != '~' and message.text[:1] != '/':
        print('argument for ' + '\'' + flag['cmd_arg'] + '\'')
#       Приписывает команду к аргументу
        message.text = flag['cmd_arg'] + ' ' + message.text
        commands(message)
        return

    if message.text[0] == '/':
        print('command')
        commands(message)
    else: 
        print('other')
        other(message)


#   Определяет команду сообщения
#   (weather, h, /, exit)
def commands(message):
    print('  command:', end=' ')
    cmd = message.text[1:]

#   weather
    if cmd >= 'weather':
        print('weather', end=' ')

#       с аргументом
        if cmd > 'weather':
            print('with argument')
            city_name = cmd.replace('weather ','')
            temp = cmds.weather(city_name)
            print('  command: {}'.format(cmd))
            print('     city: {}'.format(city_name))
            print('   output: {}'.format(temp))
            bot.send_message(message.chat.id, 'Идём в ' + city_name)
            bot.send_message(message.chat.id, temp)
            flag['cmd_arg'] = '~'


#       без аргумента
        else: 
            print('without argument')
            bot.send_message(message.chat.id, 'Город допиши, будь добр')
            flag['cmd_arg'] = '/weather'


#   h
    elif cmd == 'h':
        print('help')
        bot.send_message(message.chat.id, cmds.help(message))


#   exit
    elif cmd == 'exit': 
        print('exit')
        bot.send_message(message.chat.id, 'Не-а')
        exit # который никак не хочет делать exit


#   restart
    elif cmd == 'restart': 
        print('restart')
        bot.send_message(message.chat.id, 'Я хз, как можно через бот зарестартить \
                                    этого же бота. Напиши @SoLowHigh в лс, если знаешь')

#   alias
    elif cmd > 'alias ':
        print('alias for \'{}\''.format(message.text[7:]))
        alias.append(cmd.replace('alias ', ''))
        print('all binds:', end=' ')
        for i in alias:
            print(i, end=', ')
        print('')
        flag['alias'] += 1
        bot.send_message(message.chat.id, 'Запомним')
        # реализовано наполовину

#   /
    elif cmd == '':
        print('slash')
        bot.send_message(message.chat.id, 'It\'s a slash!')

    tick()



#   Реакция на не-команду
def other(message):
    msg = message.text
    # with open('docs/NoU', 'r') as f_NoU:
    #         NoU = f_NoU.read()
    # if message.text >= NoU:
    #     bot.send_message(message.chat.id, 'Нет, ты')
    #     return
    if msg == msg[::-1] and len(msg) > 3:
        bot.send_message(message.chat.id, 'Ладно, подловил')
        tick()
        return
    if msg == 'admin' or msg == 'root':
        bot.send_message(message.chat.id, 'Хорошая попытка, но нет')
        tick()
        return
    bot.send_message(message.chat.id, msg[::-1])
    # output(msg[::-1])
    tick()

def tick():
    print('     tick\n')

# Попытка сделать вывод сообщения в чат единой функцией, но message не ловится :(
def output(msg):
    global message
    bot.send_message(message.chat.id, msg)
    tick()
    return

# cmd_arg -- если != ~, то бот будет ждать вместо новой команды дописывания аргумента к старой
# level -- по идее, это вкусное оформление логов в виде табуляции, но непонятно, как реализовать
flag = {'cmd_arg': '~', 'level': 0, 'alias': 0}

alias = []

#   Постоянное чтение сообщений ботом, которое я вообще не понимаю, как работает
bot.polling()


# принцип работы бота

# действие:
#     лог в консоль
#     *действие*
#     под-действие:
#         лог в консоль
#         *под-действие*
#     тик


# закрывашка любой команды на время доработки

# print('|censored|')
# bot.send_message(message.chat.id, 'У меня лапки, доступ закрыт')
# tick()
# return