#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pathlib
import yaml


class defaults(object):
    '''Default configuration for application
    '''
    subcommand = 'user'


class secrets(object):
    file = pathlib.Path(__file__).parent.parent.resolve() / 'secrets.yml'

# load secrets.yml file and assign values to the secrets config object
for key, value in yaml.load(
        secrets.file.read_text(), Loader=yaml.BaseLoader
).items():
    setattr(secrets, key, value)
