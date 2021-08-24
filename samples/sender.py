#!/usr/bin/env python

from context import *
import time
import random
import sys
from multisock.crypter import Crypter
from multisock.channel import Channel

if __name__ == '__main__':
    udpchan = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', Crypter('pwd', 'passphrase'))

    senderName=sys.argv[1] if len(sys.argv) > 1 else 'anonymous'

    for i in range(1000):
        print(f'Sending to {udpchan}')
        udpchan.send('Hello world!')
        time.sleep(random.randint(0, 1))
