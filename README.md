## Enteros Bot
### Python Libs Used
#### Telegram API

[Telegram Bot API](https://github.com/eternnoir/pyTelegramBotAPI)
```commandline
pip install pyTelegramBotAPI
```
#### NLTK

```commandline
pip install nltk
```

#### pymorphy2

For russian language lemminization: [pymorphy2](https://pymorphy2.readthedocs.io/en/stable/_modules/pymorphy2/analyzer.html)

```commandline
pip install pymorphy2
```

### Heroku 

*not relevant anymore. Github actions are used*

#### Run
```commandline
heroku run python enteros-bot.py
heroku scale worker=1
```

#### Stop
```commandline
heroku ps
heroku ps:stop run.9670
```
