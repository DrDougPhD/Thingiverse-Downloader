#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import functools
import logging
import time

logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def classify(obj):
    return converter.get(type(obj), lambda v: v)(obj)


def objectify(obj):
    return DictionaryToObjectMapper(obj=obj)


def listify(obj):
    return [
        converter[type(value)](value)
        for value in obj
    ]


converter = {
    dict: objectify,
    list: listify,
}


class DictionaryToObjectMapper(object):
    def __init__(self, obj):
        self.value = None
        if type(obj) is dict:
            for key, value in obj.items():
                setattr(self, key, DictionaryToObjectMapper(obj=value))
        elif type(obj) is list:
            self.value = []
            for value in obj:
                self.value.append(DictionaryToObjectMapper(obj=value))
        else:
            self.value = obj

    def __str__(self):
        return str(self.value)


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton


def slowdown(to):
    minimum_wait_time = datetime.timedelta(seconds=to)

    def slowdown_decorator(function):
        def wrapper(*args, **kwargs):
            current_time = datetime.datetime.now()
            previous_time = slowdown_decorator.last_called_on
            time_since_last_call = current_time - previous_time
            if time_since_last_call > minimum_wait_time:
                logger.info(f'Waiting {time_since_last_call} until next API call...')
                time.sleep(time_since_last_call.seconds)

            response = function(*args, **kwargs)

            slowdown_decorator.last_called_on = datetime.datetime.now()
            return response

        return wrapper

    slowdown_decorator.last_called_on = datetime.datetime.fromtimestamp(0)
    return slowdown_decorator
