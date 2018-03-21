#!/usr/bin/env python

import multisock
import time
import random

if __name__ == '__main__':
    udpchan = multisock.Channel('224.1.1.1', 1234, 1024)

    for i in range(10):
        m=multisock.SerializableData()
        m.sender='Test Sender'
        m.seqno=i
        print 'Sending to %s' % udpchan
        udpchan.sendData(m)
        time.sleep(random.randint(0,2))
