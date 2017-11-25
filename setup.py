# -*- coding: utf-8 -

import os
import sys

from setuptools import setup, find_packages

CLASSIFIERS = []

# read long description
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()


setup(
    name='gnansomer',
    version="0.1.0",
    description='Software for mapping pollution to geographic position',
    long_description=long_description,
    author='Dejan Noveski',
    author_email='dr.mote@gmail.com',
    classifiers=CLASSIFIERS,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyserial",
    ],
    entry_points="""
    [console_scripts]
    gnasnomer=gnasnomer:run
    """
)
