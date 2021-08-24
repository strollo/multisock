#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
logfactory.py
Don't want to waste time to see logging api? OK.
Try this:

from multisock import LogFactory
# This will create a logger associated to a component named <mycomponent> and will log output into a file
# <trace>_$date.log. Notice that the second parameter is optional (the filename) and if None or not passed
# the logger will simply trace info on STDOUT.
mylogger=LogFactory('mycomponent', 'traces')
mylogger.info('Hello world!')
mylogger.warn('Too lazy to check logging APIs. Maybe later!')
mylogger.critical('This should never happen')
mylogger.fatal('Farewell cruel world')
"""

import logging
import datetime
import os

class LogFactory:
    '''
    A general purpose logger builder.
    Usage:
        # Creates a log file logs/samplelog_${DATE}.log
        # The log dir will be created if does not exist
        logger = LogFactory('compname', 'logs/samplelog')
        logger.info('Hello world')
    '''

    def __init__(self, compname, fname=None):
        """
        :param compname: to distinguish components that are sharing same log file
        :param fname: the log file name prefixed with log dir (file extension not needed)
        """
        self.__init_logger__(compname, fname)

    def __check_log_dir(self, logfile):
        '''
        checks if the log dir exists otherwise tries to create it.
        '''
        _dir = os.path.dirname(logfile)
        if _dir is None or len(_dir.strip()) == 0:
            return
        # directory does not exists
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    def __init_logger__(self, compname, fname):
        if compname is not None:
            compname = compname[:5]
        else:
            compname = 'undef'

        #################
        # STDOUT
        #################
        self.logger = logging.getLogger(compname)
        self.logger.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.NOTSET)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)-15s|%(name)-5s|%(levelname).3s|%(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        #################
        # Trace to file
        #################
        if fname:
            self.__check_log_dir(fname)
            _date = datetime.date.strftime(datetime.date.today(), '%Y%m%d')
            _fname = '%s_%s.log' % (fname, _date)
            fh = logging.FileHandler(_fname)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def __getattr__(self, item):
        '''
        Allows direct access to encapsulated logger instance.
        '''
        return getattr(self.logger, item)
