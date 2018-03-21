#!/usr/bin/env python

import multisock

if __name__ == '__main__':
    udpchan = multisock.Channel('224.1.1.1', 1234, 1024)
    print 'Reading from %s' % udpchan

    while True:
        data = udpchan.recvData()
        print 'received %s' % data