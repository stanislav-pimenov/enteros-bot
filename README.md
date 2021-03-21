### Enteros Bot
#### Install Telegram API

[Telegram Bot API](https://github.com/eternnoir/pyTelegramBotAPI)
```commandline
pip install pyTelegramBotAPI
```
#### Install NLTK
```commandline
pip install nltk
```

### Heroku
```commandline
heroku run python enteros-bot.py
heroku scale worker=1
```

#### Stop
```commandline
heroku ps
heroku ps:stop run.9670
```