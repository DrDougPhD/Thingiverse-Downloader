#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download all stuff uploaded by a user"""

import logging
import pathlib

import progressbar

from thingiverse_dl.api import users, things

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
    logger.info(user)
    download_directory = pathlib.Path('dl')/args.username
    for user_thing in progressbar.progressbar(user.things):
        thing = things.get(id=user_thing.id)
        thing_download_directory = download_directory/str(user_thing.id)
        logger.info(f'\t{thing}')
        for f in thing.files:
            logger.info(f'\t\t{f}')
            f.download(within=thing_download_directory)
        logger.info('-'*120)
