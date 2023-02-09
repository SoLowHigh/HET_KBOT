import telebot
# from telegram.ext import Updater, CommandHandler
from telebot import types

bot = telebot.TeleBot('5761545857:AAFqY-qTVm9b4QjOyq8HWYIv5wBWvZfJG20')

# lat1 = 1
# lat2 = 2
# long1 = -1
# long2 = -2

# coords = [[lat1, long1], [lat2, long2]]
coords = [['-0.127696', '51.507351'], ['-81.250048', '42.983001'], ['27.867743', '-33.000161'], ['0.10504', '51.61575'], ['-0.060385', '51.310052'], ['-84.083487', '37.128502'], ['-83.448522', '39.886703'], ['-72.220488', '41.299168'], ['-61.514897', '10.652368'], ['-81.149015', '43.028577']]

coords.sort(key=lambda x: float(x[0]), reverse=True)
print(coords)

i = 0
while i < len(coords) - 1:
    if abs(float(coords[i][0]) - float(coords[i+1][0])) < 3 or abs(float(coords[i][1]) - float(coords[i+1][1])) < 3:
        del coords[i]
    else: 
        i += 1 
print(coords)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()

    for i in range(len(coords)):  # Для каждой пары переменных из coords создаем кнопку с текстом "Пара {i}" 
        button_coord = types.InlineKeyboardButton(text=f"Пара {i}", callback_data=f"{coords[i][0]},{coords[i][1]}")

        keyboard.add(button_coord)

    bot.send_message(message.chat.id, 'Выберите пару:', reply_markup=keyboard)

    
@bot.callback_query_handler(func=lambda call: True) 
# Обработчик callback-query (нажатия на кнопку) сохраняет lat, long из call.data (вид "lat,long")  
def temp(call):  
    lat, long = call.data.split(',')  
bot.polling()

# message: {'content_type': 'text', 'id': 1295, 'message_id': 1295, 'from_user': {'id': 364623079,
#           'is_bot': False, 'first_name': 'SoLowHigh', 'username': 'SoLowHigh', 'last_name': None, 
#           'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None, 
#           'supports_inline_queries': None, 'is_premium': None, 'added_to_attachment_menu': None}, 
#           'date': 1674657682, 'chat': {'id': 364623079, 'type': 'private', 'title': None, 
#           'username': 'SoLowHigh', 'first_name': 'SoLowHigh', 'last_name': None, 'is_forum': None,
#           'photo': None, 'bio': None, 'join_to_send_messages': None, 'join_by_request': None,
#           'has_private_forwards': None, 'has_restricted_voice_and_video_messages': None, 
#           'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 
#           'slow_mode_delay': None, 'message_auto_delete_time': None, 'has_protected_content': None, 
#           'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None, 
#           'active_usernames': None, 'emoji_status_custom_emoji_id': None, 'has_hidden_members': None, 
#           'has_aggressive_anti_spam_enabled': None}, 'sender_chat': None, 'forward_from': None, 
#           'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 
#           'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 
#           'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'has_protected_content': None, 
#           'media_group_id': None, 'author_signature': None, 'text': '/weather omsk', 
#           'entities': [<telebot.types.MessageEntity object at 0x7fb3d61187c0>], 'caption_entities': None, 
#           'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 
#           'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 
#           'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 
#           'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 
#           'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 
#           'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 
#           'connected_website': None, 'reply_markup': None, 'message_thread_id': None, 'is_topic_message': None, 
#           'forum_topic_created': None, 'forum_topic_closed': None, 'forum_topic_reopened': None, 
#           'has_media_spoiler': None, 'forum_topic_edited': None, 'general_forum_topic_hidden': None, 
#           'general_forum_topic_unhidden': None, 'write_access_allowed': None, 
#           'json': {'message_id': 1295, 'from': {'id': 364623079, 'is_bot': False, 'first_name': 'SoLowHigh', 
#           'username': 'SoLowHigh', 'language_code': 'ru'}, 'chat': {'id': 364623079, 'first_name': 'SoLowHigh', 
#           'username': 'SoLowHigh', 'type': 'private'}, 'date': 1674657682, 'text': '/weather omsk', 
#           'entities': [{'offset': 0, 'length': 8, 'type': 'bot_command'}]}}