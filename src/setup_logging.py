import logging.handlers
import sys

LOG_FILENAME = 'botl.log'
botl = logging.getLogger('BotLogger')

class LoggerWriter:
    def __init__(self, level):
        self.level = level

    def write(self, message):
        if message != '\n':
            self.level(message)

    def flush(self):
        self.level(sys.stderr)

def init_logger():
    # Set up a specific logger with our desired output level
    botl.setLevel(logging.INFO)

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, encoding='utf-8', maxBytes=10485760, backupCount=5)

    formatter = logging.Formatter(u'%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    botl.addHandler(handler)

    sys.stdout = LoggerWriter(botl.info)
    sys.stderr = LoggerWriter(botl.error)

    print('Init logger: Done')
    botl.info('Olala')


if __name__ == '__main__':
    init_logger()