#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download all stuff uploaded by a user"""

import logging

from thingiverse_dl import config
from thingiverse_dl.api import users

logger = logging.getLogger(__name__)


def cli(subcommand):
    '''Add command-line arguments to this subcommand
    '''
    subcommand.add_argument(
        'username',
        help='username from whom to download',
    )
    subcommand.set_defaults(func=main)


def main(args):
    # read from file system to learn about albums that have been ripped
    user = users.get(username=args.username)
