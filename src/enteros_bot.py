import os
import random
import re

import nltk
import pymorphy2
import requests
import wikipedia
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, ContextTypes, MessageHandler, filters

from quotas import quota_exceeded
from setup_logging import *

bot_token = os.getenv('BOT_TOKEN')

# nltk
nltk.download('punkt')
nltk.download('stopwords')
stemmer = SnowballStemmer("russian")
stop_words = stopwords.words("russian")
# pymorphy2
morph = pymorphy2.MorphAnalyzer()
MORNING_DICT = ['утро', 'утренний', 'утром']
# conversation states
QUERY = range(1)


def print_user_info(update, context):
    botl.info('chat: %s', update.message.chat)
    botl.info('from_user %s:', update.message.from_user)


async def handle_send_boobs(update, context):
    print_user_info(update, context)
    msg_text = quota_exceeded(update.message.from_user.id)
    if (msg_text):
        await context.bot.send_message(chat_id=update.message.chat_id, text=msg_text)
    else:
        boobsNr = random.randint(1, 403)
        url = 'http://www.porngif.top/gif/prsa/' + str(boobsNr).zfill(4) + '.gif'
        await context.bot.send_message(chat_id=update.message.chat_id, text=url)


menu_dict = {
    "Анекдот": 1,
    "Рассказы": 2,
    "Стишки": 3,
    "Афоризмы": 4,
    "Цитаты": 5,
    "Тосты": 6,
    "Статусы": 8,
    "Анекдот (+18)": 11,
    "Рассказы (+18)": 12,
    "Стишки (+18)": 13,
    "Афоризмы (+18)": 14,
    "Цитаты (+18)": 15,
    "Тосты (+18)": 16,
    "Статусы (+18)": 18
}
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about content type."""
    reply_keyboard =  [
        list(menu_dict.keys())[0:3],
        list(menu_dict.keys())[3:6],
        list(menu_dict.keys())[6:9],
        list(menu_dict.keys())[9:12],
        list(menu_dict.keys())[12:14]
    ]
    await update.message.reply_text(
        "Выбери контент и возможно тебе будет смешно блев:\nИли /cancel для отмены",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Контент"
        ),
    )
    return QUERY

async def process_rzhu(update, context) -> int:
    try:
        text = update.message.text
        id = list(menu_dict.values())[list(menu_dict.keys()).index(text)]
        param = {'CType': id, }
        r = requests.get(
            'http://rzhunemogu.ru/RandJSON.aspx', params=param, allow_redirects=False)
        rzhu = r.text.replace("{\"content\":\"", "").replace("}", "")
        await context.bot.send_message(chat_id=update.message.chat_id, text=rzhu, reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        botl.exception("Something wrong when process_rzhu")
        await context.bot.send_message(chat_id=update.message.chat_id, text='блев', reply_markup=ReplyKeyboardRemove())
    finally:
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    botl.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "В пизду!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def be_like_ivan(update, context):
    try:
        chat_id = update.message.chat_id
        r = requests.get('http://api.icndb.com/jokes/random', allow_redirects=False)
        joke = r.json()["value"]["joke"].replace('&quot;', '\"')
        entriesToReplace = ['Chuck Norris', 'Norris', 'Chuck']
        for i in entriesToReplace:
            src_str = re.compile(i, re.IGNORECASE)
            joke = src_str.sub('Ivan', joke)

        await context.bot.send_message(chat_id=chat_id, text=joke)
    except Exception as e:
        botl.exception('something went wrong')
        await context.bot.send_message(chat_id=chat_id, text='блев')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        update.message.chat_id,
        'Пожелай доброго утра блев или выполни /boobs, /rzhu, /ivan или /wiki, если ты кот учёный')


async def get_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stemmed_word = stemmer.stem("пизда")
    if re.search(stemmed_word, update.message.text.lower()):
        await context.bot.send_message(chat_id=update.message.chat_id,
                                       text="Винтовка это праздник, всё летит в пизду!!!",
                                       reply_to_message_id=update.message.message_id)

    parsed = lemminized_morning(update.message.text.lower())
    if parsed:
        await context.bot.send_message(chat_id=update.message.chat_id, text=prepare_response(
            parsed), reply_to_message_id=update.message.message_id)

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


async def wiki_search(update, context) -> None:
    query = " ".join(context.args)
    botl.info('query: %s', query)
    try:
        page = wikipedia.page(query)
        await update.message.reply_text(page.summary + os.linesep + page.url, disable_web_page_preview=True)
    except wikipedia.exceptions.DisambiguationError as e:
        await update.message.reply_text("Sorry, I couldn't find any results for that query. Please be more specific.")
    except wikipedia.exceptions.PageError:
        await update.message.reply_text("Sorry, I couldn't find any results for that query.")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler('boobs', handle_send_boobs))
    # application.add_handler(CommandHandler('rzhu', send_welcome))
    application.add_handler(CommandHandler('wiki', wiki_search))
    application.add_handler(CommandHandler('ivan', be_like_ivan))
    application.add_handler(CommandHandler("help", help_command))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("rzhu", send_welcome)],
        states={
            QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_rzhu)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_text_messages))

    # init logging
    init_logger()
    wikipedia.set_lang('ru')
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
