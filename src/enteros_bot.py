import os

import nltk
import pymorphy2
import requests
import telebot
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from telebot import types
import re

from quotas import quota_exceeded

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
# nltk
nltk.download('punkt')
nltk.download('stopwords')
stemmer = SnowballStemmer("russian")
stop_words = stopwords.words("russian")
# pymorphy2
morph = pymorphy2.MorphAnalyzer()
MORNING_DICT = ['утро', 'утренний', 'утром']


# @bot.message_handler(commands=['void'])
# def handle_boobs_choice(message):
#     markup = types.ReplyKeyboardMarkup()
#     itembtna = types.KeyboardButton('/boobs')
#     itembtnv = types.KeyboardButton('/pussy')
#     itembtnc = types.KeyboardButton('/ass')
#     itembtnd = types.KeyboardButton('/missionary')
#     itembtne = types.KeyboardButton('/cowgirl')
#     itembtnf = types.KeyboardButton('/doggystyle')
#     itembtng = types.KeyboardButton('/blowjob')
#     itembtnh = types.KeyboardButton('/cumshots')
#
#     markup.row(itembtna, itembtnv, itembtnc)
#     markup.row(itembtnd, itembtnf)
#     markup.row(itembtne, itembtng, itembtnh)
#     bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
#     bot.register_next_step_handler(message, handle_send_boobs)


@bot.message_handler(commands=['boobs'])
def handle_send_boobs(message):
    msg_text = quota_exceeded(message.from_user.id)
    if (msg_text):
        bot.send_message(message.chat.id, msg_text)
    else:
        r = requests.get('https://love-you.xyz/api/v2' + message.text,
                         headers={'Accept': 'application/json'})
        url = r.json()['url']
        bot.send_message(message.chat.id, url)


@bot.message_handler(commands=['rzhu'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
        Выбери контент и возможно тебе будет смешно блев:
1 - Анекдот
2 - Рассказы
3 - Стишки
4 - Афоризмы
5 - Цитаты
6 - Тосты
8 - Статусы
11 - Анекдот (+18)
12 - Рассказы (+18)
13 - Стишки (+18)
14 - Афоризмы (+18)
15 - Цитаты (+18)
16 - Тосты (+18)
18 - Статусы (+18)
""")
    bot.register_next_step_handler(msg, process_rzhu)


def process_rzhu(message):
    try:
        id = message.text
        param = {'CType': id, }
        r = requests.get(
            'http://rzhunemogu.ru/RandJSON.aspx', params=param, allow_redirects=False)
        rzhu = r.text.replace("{\"content\":\"", "").replace("\"}", "")
        bot.send_message(message.chat.id, rzhu)
    except Exception as e:
        bot.reply_to(message, 'блев')


@bot.message_handler(commands=['ivan'])
def be_like_ivan(message):
    try:
        chat_id = message.chat.id
        r = requests.get('http://api.icndb.com/jokes/random',
                         allow_redirects=False)

        joke = r.json()["value"]["joke"].replace('&quot;', '\"')
        entriesToReplace = ['Chuck Norris', 'Norris', 'Chuck']
        for i in entriesToReplace:
            src_str = re.compile(i, re.IGNORECASE)
            joke = src_str.sub('Ivan', joke)

        bot.send_message(message.chat.id, joke)
    except Exception as e:
        bot.reply_to(message, 'блев')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/help':
        bot.send_message(
            message.chat.id, 'Пожелай доброго утра блев или выполни /boobs, /rzhu, /ivan')
    else:
        parsed = lemminized_morning(message.text.lower())
        if parsed:
            bot.send_message(message.chat.id, prepare_response(
                parsed), reply_to_message_id=message.message_id)


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
