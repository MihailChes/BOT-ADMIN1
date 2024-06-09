import telebot # библиотека telebot
from config import token # импорт токена

bot = telebot.TeleBot(token) 
warn = {}
@bot.message_handler(commands=['start'])
def start(message):
    warn[message.from_user.id] = 0
    bot.reply_to(message, "Привет! Я бот для управления чатом.")
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Чтобы забанить пользователя, надо в ответ написать /ban")
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")
@bot .message_handler(commands=['warning'])
def warning_user(message):
    global warn
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        if user_id not in warn.keys():
            warn[user_id] = 0
        warn[user_id] += 1
        warnings =warn[user_id] 

        bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} имеет {warnings}/4 предупреждении")
        if warnings >= 4:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
       
            warnings = 0
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, который вы хотите предупредить.")
@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'Я принял нового пользователя!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)
bot.infinity_polling(none_stop=True)
