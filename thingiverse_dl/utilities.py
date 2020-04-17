#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import functools
import logging
import time

logger = logging.getLogger(__name__)


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
                logger.info(f'Waiting {time_since_last_call} until next call...')
                time.sleep(time_since_last_call.seconds)

            response = function(*args, **kwargs)

            slowdown_decorator.last_called_on = datetime.datetime.now()
            return response

        return wrapper

    slowdown_decorator.last_called_on = datetime.datetime.fromtimestamp(0)
    return slowdown_decorator