#!/usr/bin/env python
# -*- coding: utf-8 -*-

from channel import Channel
from logfactory import LogFactory
from serializabledata import SerializableData
from package_info import *

######################################################
# Package information are imported from package_info
# DATA IMPORTED FROM package_info.py file
######################################################
__author__      = package_info.__author__
__copyright__   = package_info.__copyright__
# __credits__   = []
__license__     = package_info.__license__
__version__     = package_info.__version__
__maintainer__  = package_info.__maintainer__
__email__       = package_info.__email__
__status__      = package_info.__status__
######################################################

# The list of components implicitly imported by library
__all__ = ['Channel', 'LogFactory', 'SerializableData']
