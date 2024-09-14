from logging import (basicConfig,
                     INFO, DEBUG, WARNING, ERROR, CRITICAL,
                     Formatter,
                     StreamHandler,
                     getLogger)
from concurrent_log_handler import ConcurrentRotatingFileHandler
from sys import (stdout,
                 platform)
from os import (system,
                path,
                mkdir)
from typing import (Literal,
                    List)

class CustomFormatter(Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = '%(asctime)s,%(msecs)d %(levelname)-4s [%(filename)s:%(lineno)d -> %(name)s - %(funcName)s] ___ %(message)s'

    FORMATS = {
        DEBUG: grey + format + reset,
        INFO: grey + format + reset,
        WARNING: yellow + format + reset,
        ERROR: red + format + reset,
        CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_fmt)
        return formatter.format(record)

def configure_logger(log_name : str = "runtime_log.log",
                     maxBytes: int = 20*1024*1024,
                     backupCount: int = 2,
                     log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = DEBUG,
                     propagate_logger: bool = True):

    if platform == 'win32':
        # enable colored console text on windows
        system('color')

    if propagate_logger:
        # some libs will interfere with the logger and overwrite the log level
        # the logic below will make sure that the same log level is used for other "problematic" libs as well
        for lib in ['requests', 'urllib']:
            getLogger(lib).setLevel(log_level)

    ch = StreamHandler(stream=stdout)
    ch.setLevel(DEBUG)
    ch.setFormatter(CustomFormatter())
    # first check if the log_name specified is actually within a folder and try to create it
    if (path.dirname(log_name) and
            not path.isdir(path.dirname(log_name))):
        try:
            mkdir(path.dirname(log_name))
        except:
            raise Exception(f'Your log name is invalid: {log_name}')

    # and after that pass the argument along to ConcurrentRotatingFileHandler
    fh = ConcurrentRotatingFileHandler(log_name,
                                       mode='a',
                                       maxBytes=maxBytes,
                                       backupCount=backupCount)
    fh.setLevel(DEBUG)
    fh.setFormatter(Formatter('%(asctime)s,%(msecs)d %(levelname)-4s [%(filename)s:%(lineno)d -> %(name)s - %(funcName)s] ___ %(message)s'))

    basicConfig(datefmt='%Y-%m-%d:%H:%M:%S',
                level=log_level,
                handlers=[fh,ch])

def configure_loggers(log_names : List[str] = ("main_logger.log"),
                      maxBytes: int = 20*1024*1024,
                      backupCount: int = 2,
                      log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = DEBUG,
                      propagate_logger: bool = True):

    if platform == 'win32':
        # enable colored console text on windows
        system('color')

    if propagate_logger:
        # some libs will interfere with the logger and overwrite the log level
        # the logic below will make sure that the same log level is used for other "problematic" libs as well
        for lib in ['requests', 'urllib']:
            getLogger(lib).setLevel(log_level)

    ch = StreamHandler(stream=stdout)
    ch.setLevel(DEBUG)
    ch.setFormatter(CustomFormatter())

    # configure each logger in the same manner, but with different file handlers
    for log_name in log_names:

        # first check if the log_name specified is actually within a folder and try to create it
        if (path.dirname(log_name) and
                not path.isdir(path.dirname(log_name))):
            try:
                mkdir(path.dirname(log_name))
            except:
                raise Exception(f'Your log name is invalid: {log_name}')

        # and after that pass the argument along to ConcurrentRotatingFileHandler
        fh = ConcurrentRotatingFileHandler(log_name,
                                           mode='a',
                                           maxBytes=maxBytes,
                                           backupCount=backupCount)
        fh.setLevel(DEBUG)
        fh.setFormatter(Formatter('%(asctime)s,%(msecs)d %(levelname)-4s [%(filename)s:%(lineno)d -> %(name)s - %(funcName)s] ___ %(message)s'))

        basicConfig(datefmt='%Y-%m-%d:%H:%M:%S',
                    level=log_level)

        log = getLogger(path.basename(log_name))
        for _ in log.handlers:
            log.removeHandler(_)
        log.addHandler(fh)
        log.addHandler(ch)

        # disable logger hierarchy propagation
        log.propagate = False

if __name__ == '__main__':

    # a single root logger
    configure_logger(log_name='log\\my_log.log',
                     log_level='INFO')
    log = getLogger()

    log.debug('I am a DEBUG message')
    log.info('I am an INFO message')
    log.warning('I am a WARNING message')
    log.error('I am an ERROR message')
    log.critical('I am a CRITICAL message')

    # multiple loggers
    configure_loggers(log_names=['log\\some_log.log', 'log\\another_log.log'])
    log = getLogger('some_log.log')
    log.debug('some_log I am a DEBUG message')
    log.info('some_log I am an INFO message')
    log.warning('some_log I am a WARNING message')
    log.error('some_log I am an ERROR message')
    log.critical('some_log I am a CRITICAL message')

    log = getLogger('another_log.log')
    log.debug('another_log I am a DEBUG message')
    log.info('another_log I am an INFO message')
    log.warning('another_log I am a WARNING message')
    log.error('another_log I am an ERROR message')
    log.critical('another_log I am a CRITICAL message')

    print('MANUAL assessment required !')