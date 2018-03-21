#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import warnings
from multisock import package_info

setup(
    name='multisock',
    version=package_info.__version__,
    author=package_info.__author__,
    author_email=package_info.__email__,
    url='http://github.com/strollo/multisock',
    packages=find_packages(exclude=['tests','samples']),
    description='Lightweight multicast communication overlay library',
    keywords=["IoT", "UDP", "Multicasting"],
    platforms=['Windows', 'Linux', 'OSX'],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL 3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: IoT :: SmallComponents',
        'Topic :: IoT :: Cheap HW',
        'Topic :: IoT :: Communication',
    ],
    include_package_data=True,
    license=package_info.__license__,
    zip_safe=False,
)
