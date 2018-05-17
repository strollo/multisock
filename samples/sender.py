#!/usr/bin/env python

from context import *
import multisock
import time
import random
import sys

if __name__ == '__main__':
    udpchan = multisock.Channel('224.1.1.1', 1234, 2048, '0.0.0.0')

    senderName='anonymous'
    if len(sys.argv) > 1:
        senderName=sys.argv[1]

    time.sleep(5)
    for i in range(1000):
        print 'Sending to %s' % udpchan
        udpchan.send('Hello world!')
        time.sleep(random.randint(0,1))
