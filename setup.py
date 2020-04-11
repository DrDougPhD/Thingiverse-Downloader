# -*- coding: utf-8 -*-
from setuptools import setup
import pathlib


dependencies = list(
    filter(lambda l: not l.startswith('#'),
           map(lambda l: l.strip(),
               pathlib.Path('requirements.txt').read_text().split('\n')))
)
description = pathlib.Path('README.md').read_text()

setup(
    name='thingiverse_dl',
    version='0.0.0dev1',
    author="Doug McGeehan",
    author_email="djmvfb@mst.edu",
    description=description,
    license="GNU GPLv3",
    keywords="thingiverse",
    url="https://github.com/DrDougPhD/Thingiverse-Downloader",
    packages=['thingiverse',
              'thingiverse.commandline',
              'thingiverse.commandline.scripts'],
    classifiers=[
        "Topic :: Utilities",
    ],
    entry_points={
        'console_scripts': [
            'thingiverse_dl = thingiverse.cli:main',
         ],
    },
    install_requires=dependencies,
)
