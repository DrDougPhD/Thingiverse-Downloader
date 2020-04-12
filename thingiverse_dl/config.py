#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pathlib
import sys
import yaml
import logging

logger = logging.getLogger(__name__)


class defaults(object):
    '''Default configuration for application
    '''
    subcommand = 'user'


class secrets(object):
    yml_file = pathlib.Path(__file__).parent.parent.resolve() / 'secrets.yml'
    # yml_dict = yaml.load(yml_file.read_text(),
    #                      Loader=yaml.BaseLoader)
    expected_config_keys = {'client_id', 'client_secret', 'app_token'}


# load secrets.yml file and assign values to the secrets config object
try:
    yaml_dict = yaml.load(secrets.yml_file.read_text(),
                          Loader=yaml.BaseLoader)
    missing_config_keys = secrets.expected_config_keys.difference(yaml_dict.keys())
    if len(missing_config_keys) > 0:
        raise KeyError()
except FileNotFoundError as e:
    # User did not create the `secrets.yml` file
    logger.critical(f'Thingiverse secrets file not found at {secrets.yml_file}.\n'
                    f'Please register your usage of this app with Thingiverse, '
                    f'populate the "{secrets.yml_file.name}.template" file, '
                    f'and rename it to "{secrets.yml_file.name}"')
    sys.exit(1)
except KeyError as e:
    # User did not properly format the `secrets.yml` file
    logger.critical(f'{secrets.yml_file} is incomplete.\n'
                    f'\tExpected keys: {", ".join(secrets.expected_config_keys)}\n'
                    f'\tMissing keys:  {", ".join(missing_config_keys)}')
    sys.exit(1)
else:
    for key in secrets.expected_config_keys:
        setattr(secrets, key, yaml_dict[key])
