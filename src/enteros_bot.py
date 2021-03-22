import telebot
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
import nltk

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/help':
        bot.send_message(message.chat.id, 'Напиши Доброе утро')
    elif is_good_morning_nltk(message.text.lower()):
        bot.send_message(message.chat.id, 'Хуютра!', reply_to_message_id=message.message_id)


def is_good_morning(message):
    return 'утра' in message or 'утро' in message

def is_good_morning_nltk(message):
    nltk.download('punkt')
    stemmer = SnowballStemmer("russian")
    for sentence in sent_tokenize(message, language="russian"):
        for word in word_tokenize(sentence, language="russian"):
            stem = stemmer.stem(word)
            if stem == 'утр':
                return True
    return False

bot.polling(none_stop=True, interval=0)
