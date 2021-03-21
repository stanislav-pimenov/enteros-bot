import telebot
import os

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    message_lower = message.text.lower() 
    if "утра" in message_lower or "утро" in message_lower:
        bot.send_message(message.chat.id, "Хуютра!", reply_to_message_id=message.message_id)
    elif message.text == "/help":
        bot.send_message(message.chat.id, "Напиши Доброе утро")

bot.polling(none_stop=True, interval=0)