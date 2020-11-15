import time
from reusepatterns.singltones import SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        with open(f'{self.name}_logs.txt', 'a') as f:
            f.write(f'{text}\n')


# декоратор
def debug(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('DEBUG-------->', func.__name__, end - start)
        return result

    return inner
