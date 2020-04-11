#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYNOPSIS

	python thingiverse.py [-h,--help] [-v,--verbose]


DESCRIPTION

	Download stuff uploaded to Thingiverse


ARGUMENTS

	-h, --help          show this help message and exit
	-v, --verbose       verbose output


AUTHOR

	Doug McGeehan


LICENSE

	Copyright 2020 Doug McGeehan - GNU GPLv3

"""
import logging
import progressbar

from thingiverse import cli


__appname__ = "thingiverse_dl"
__author__ = "Doug McGeehan"
__license__ = "GNU GPLv3"
__indevelopment__ = True        # change this to false when releases are ready


progressbar.streams.wrap_stderr()
logger = logging.getLogger(__appname__)


def main(args):
    '''ADD DESCRIPTION HERE'''
    args.func(args=args)


if __name__ == '__main__':
    with cli.prepare(app=__appname__,
                     description=main.__doc__,
                     verbosity=__indevelopment__) as commandline:
        main(args=commandline.arguments)
