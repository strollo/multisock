#!/usr/bin/env python

# Include parent folder in module resolution
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from multisock.channel import Channel
from multisock.crypter import Crypter

if __name__ == '__main__':
    udpchan = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', Crypter('pwd', 'passphrase'))

    print(f'Reading from {udpchan}')
    while True:
        (data, sender) = udpchan.recv()
        print(f'received from {sender}: [{data}] ')
