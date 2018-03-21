#!/usr/bin/env python

from context import *
import multisock

if __name__ == '__main__':
    udpchan = multisock.Channel('232.232.117.122', 15033, 2048, '0.0.0.0')
    print 'Reading from %s' % udpchan

    while True:
        (data,sender) = udpchan.recv()
        print 'received %s' % data