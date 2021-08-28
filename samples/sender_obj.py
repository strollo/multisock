#!/usr/bin/env python

# Include parent folder in module resolution
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import random
from multisock.crypter import Crypter
from multisock.channel import Channel
from serializabledata import SerializableObject

import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


if __name__ == '__main__':
    udpchan = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', Crypter('pwd', 'passphrase'))

    senderName = sys.argv[1] if len(sys.argv) > 1 else 'anonymous'

    for i in range(1000):
        obj = SerializableObject(token='/patter/tester', payload={'key1': 'value1', 'key2': i})

        print(f'Sending to {udpchan}')
        udpchan.send_object(obj)
        time.sleep(random.randint(0, 1))
