"""
.. module:: decorator
   :synopsis: Module containing current and any future custom decorators used
   by app.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""

from threading import Thread


def async_in_thread(func):
    """Function annotation allowing decoration of calling functions.
    """
    def wrapper(*args, **kwargs):
        """Decoratoring method allowing functions to be executed within a
        thread."""
        thr = Thread(target=func, args=args, kwargs=kwargs)
        # print('about to start following thread: {tid} {args}' .format(
        # tid=thr.name, args=thr._kwargs))
        thr.start()

    return wrapper
