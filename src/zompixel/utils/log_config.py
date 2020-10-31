import sys
import logging


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerManager(object):
    """
    this.cls + singleton: make sure we have the same logger everywhere
    A metaclass is a class whose instances are classes.
    Like an "ordinary" class defines the behavior of the instances of the class,
    a metaclass defines the behavior of classes and their instances.
    https://www.python-course.eu/python3_metaclasses.php
    """

    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def getLogger(name=None):
        """
        Create logger
        If called with the same name "root" each time,
        it'll return the same logger
        """
        if name not in LoggerManager._loggers.keys():
            # Create logger with right params
            LoggerManager._loggers[name] = logging.getLogger(str(name))

            # Set logs level
            LoggerManager._loggers[name].setLevel(logging.WARNING)

            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            LoggerManager._loggers[name].addHandler(handler)

        return LoggerManager._loggers[name]
