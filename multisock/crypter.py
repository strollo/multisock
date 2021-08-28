#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Allows encryption of exchanged data.
"""

import base64
import random
import string
from Crypto.Cipher import AES
from multisock.exceptions import InvalidParameterException, InvalidKeyLenghtException, EncryptionInvalidParameterException

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

MAX_KEY_LENGTH = 32
ENCODING = 'utf-8'
BS = 16

def is_empty_string(s):
    if s is None or not isinstance(s, str) or len(s.strip()) == 0:
        return True
    return False

class Crypter:
    def __init__(self, key, iv):
        if is_empty_string(key):
            raise InvalidParameterException('Invalid or empty parameter [key]')
        if len(key) > MAX_KEY_LENGTH:
            raise InvalidKeyLenghtException(f'Not supported key having length greater than {MAX_KEY_LENGTH} bytes')
        if is_empty_string(iv):
            raise InvalidParameterException('Invalid or empty parameter [iv]')
        self.key = self.pad_key(key)
        self.iv = self.pad(iv)

    def unpad(self, s):
        return s[0:-ord(s[-1:])]

    def pad_key(self, s):
        if len(s) % MAX_KEY_LENGTH == 0:
            return bytes(s, ENCODING)
        return bytes(s + (MAX_KEY_LENGTH - len(s) % MAX_KEY_LENGTH) * chr(MAX_KEY_LENGTH - len(s) % MAX_KEY_LENGTH), ENCODING)

    def pad(self, s):
        if isinstance(s, str):
            return bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), ENCODING)
        if isinstance(s, bytearray):
            return bytes(get_random_string(BS), ENCODING) + bytes(s) + bytes((BS - len(s) % BS) * chr(BS - len(s) % BS), ENCODING)
        if isinstance(s, bytes):
            return s + bytes((BS - len(s) % BS) * chr(BS - len(s) % BS), ENCODING)
        raise EncryptionInvalidParameterException(f'Cannot manage objects of type: {type(s)}')

    def encrypt(self, raw):
        if raw is None:
            raise InvalidParameterException('Invalid or empty parameter')
        raw = self.pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.encodebytes(cipher.encrypt(raw))

    def decrypt(self, enc):
        if enc is None:
            raise InvalidParameterException('Invalid or empty parameter')
        enc = base64.decodebytes(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        try:
            return self.unpad(cipher.decrypt(enc)).decode(ENCODING)
        except:
            return self.unpad(cipher.decrypt(enc)[16:])
