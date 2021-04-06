import telebot
import os
import requests
import schedule
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import nltk
import pymorphy2


bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
# nltk
nltk.download('punkt')
nltk.download('stopwords')
stemmer = SnowballStemmer("russian")
stop_words = stopwords.words("russian")
# pymorphy2
morph = pymorphy2.MorphAnalyzer()
MORNING_DICT = ['утро', 'утренний', 'утром']

@bot.message_handler(commands=['boobs'])
def handle_send_boobs(message):
    r = requests.get('http://lboobs.herokuapp.com/boobs.jpg', allow_redirects=False)
    location = r.headers['Location']
    bot.send_message(message.chat.id, location)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/help':
        bot.send_message(message.chat.id, 'Напиши что-нибудь про утро или /boobs')
    else :
        parsed = lemminized_morning(message.text.lower())
        if parsed is not None :
            bot.send_message(message.chat.id, prepare_response(parsed), reply_to_message_id=message.message_id)

def is_good_morning_nltk(message):
    for sentence in sent_tokenize(message, language="russian"):
        for word in word_tokenize(sentence, language="russian"):
            stem = stemmer.stem(word)
            if stem == 'утр':
                return True
    return False

def prepare_response(obj: pymorphy2.analyzer.Parse):
    word = obj.word
    return 'хую' + word[1:] + '!'

def lemminized_morning(message):
    for sentence in sent_tokenize(message, language="russian"):
        for word in word_tokenize(sentence, language="russian"):
            if word in stop_words:
                continue
            parsed = morph.parse(word)
            for parse in parsed:
                if parse.normal_form in MORNING_DICT:
                    return parse
    return None

bot.polling(none_stop=True, interval=0)