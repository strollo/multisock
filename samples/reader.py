#!/usr/bin/env python

from context import *
import multisock
from multisock import LogFactory

if __name__ == '__main__':
    udpchan = multisock.Channel('232.232.117.122', 15033, 2048, '0.0.0.0')

    mylogger = LogFactory('readr', 'traces')
    mylogger.info('Reading from %s' % udpchan)
    while True:
        (data,sender) = udpchan.recv()
        mylogger.info ('received %s' % data)