#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import functools
import json
import logging
import pathlib
import time

import requests
import yarl
from retry import retry

from thingiverse_dl import config

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


class DelayedNetworkRequest(requests.Session):
    LAST_CALLED_ON = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @retry((requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout),
           tries=3, delay=5,
           logger=logger)
    def request(self, *args, **kwargs):
        if DelayedNetworkRequest.LAST_CALLED_ON is not None:
            self.wait()

        response = super().request(timeout=config.defaults.timeout, *args, **kwargs)
        DelayedNetworkRequest.LAST_CALLED_ON = datetime.datetime.now()

        return response

    def wait(self):
        current_time = datetime.datetime.now()
        previous_time = DelayedNetworkRequest.LAST_CALLED_ON
        time_since_last_call = current_time - previous_time
        time_to_wait = config.defaults.delay - time_since_last_call
        if time_to_wait > datetime.timedelta(seconds=0):
            logger.info(f'Waiting {time_to_wait} until next API call...')
            time.sleep(time_to_wait.seconds + 1)


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


def safe_filename(value):
    keepcharacters = {' ', '.', '_', '-'}
    return ''.join([
        c
        for c in str(value)
        if c.isalnum()
           or c in keepcharacters
    ]).rstrip()


class CachedDecorator(object):
    def __init__(self, key):
        self.key = key

    def get_caching_value(self, obj, *args, **kwargs):
        return kwargs[self.key] if obj is None else getattr(obj, self.key)

    def get_object_instance(self, *args):
        return None if len(args) == 0 else args[0]


class cached_json(CachedDecorator):
    def __call__(self, function):
        def wrapper(*args, **kwargs):
            obj = self.get_object_instance(*args)
            caching_attr_value = self.get_caching_value(
                obj=obj,
                *(args[1:] if len(args) > 1 else tuple()),
                **kwargs
            )

            logger.info(f'Looking up cache for {self.key}={caching_attr_value}...')

            safe_filename_value = safe_filename(value=caching_attr_value)
            cache_file_name = '{}.json'.format(safe_filename_value) \
                .replace('/', '-')

            cache_directory \
                = config.defaults.cache / obj.__class__.__name__ / function.__name__

            cache_directory.mkdir(parents=True, exist_ok=True)
            cache_path = cache_directory / cache_file_name

            try:
                cache = json.loads(cache_path.read_text())
                logger.debug('JSON cache loaded for {key} from {path}'.format(
                    key=caching_attr_value,
                    path=cache_path
                ))
            except IOError:
                # cache doesn't exist
                logger.debug('No JSON cache for {}'.format(caching_attr_value))
                cache = function(*args, **kwargs)

                try:
                    file = cache_path.open('w')
                except OSError:
                    import hashlib
                    checksum = hashlib.sha1()
                    checksum.update(caching_attr_value.encode('utf-8'))
                    cache_file_name = '{}.json'.format(checksum.hexdigest())
                    cache_path = cache_directory / cache_file_name
                    file = cache_path.open('w')
                json.dump(cache, file, indent=4, sort_keys=True)
                file.close()
            return cache
        return wrapper


class cached_file(CachedDecorator):
    def __call__(self, function):
        def wrapper(*args, **kwargs):
            obj = self.get_object_instance(*args)
            cached_file_path = self.get_caching_value(
                obj=obj,
                *(args[1:] if len(args) > 1 else tuple()),
                **kwargs
            )

            logger.info(f'Looking up pre-downloaded file for'
                        f' {self.key}={cached_file_path}...')

            if cached_file_path.exists():
                logger.info(f'File already exists at {cached_file_path}')
                return

            logger.debug('No cached file for {}'.format(cached_file_path))
            cache = function(*args, **kwargs)
            return cache
        return wrapper


@cached_file(key='to')
def download(url: yarl.URL, to: pathlib.Path):
    logger.info(f'Starting download of {url} to {to}')
    with DelayedNetworkRequest() as session:
        with session.get(url, stream=True) as response:
            response.raise_for_status()
            with to.open('wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
                        # f.flush()
    logger.info(f'Finished download of {url} to {to}')