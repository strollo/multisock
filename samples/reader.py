#!/usr/bin/env python

from context import *
import multisock
from multisock import LogFactory
from multisock import DataCrypto

if __name__ == '__main__':
    udpchan = multisock.Channel('224.1.1.1', 1234, 2048, '0.0.0.0', None, DataCrypto('pwd', 'passphrase'))

    mylogger = LogFactory('readr', 'traces')
    mylogger.info('Reading from %s' % udpchan)
    while True:
        (data,sender) = udpchan.recv()
        mylogger.info ('received %s' % data)