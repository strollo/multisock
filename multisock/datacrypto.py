#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Allows SHA256 encryption of exchanged data.
"""

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys

class DataCrypto:
    def __init__(self, key=None, passphrase=None):
        """
        Creates an encrypter instance with a given key.
        :param key: if None no encryption at all
        """
        self._key=None
        self.pad_delimiter='' # hope you'll never try to use this in plain strings :D
        if key is not None and passphrase is not None:
            key.strip()
            self._key=SHA256.new(key.strip()).digest()
            self._passphrase=SHA256.new(passphrase.strip()).digest()[:16]
    def _adjustpadding(self, data):
        '''
        Internally used for 16bits padding of data to crypt.
        '''
        if data is None:
            return None
        l=len(data)%16
        return data + (self.pad_delimiter * (16-l))
    def encrypt(self, data):
        if self._key is None:
            return data
        _encryptor = AES.new(self._key, AES.MODE_CBC, self._passphrase)
        return _encryptor.encrypt(self._adjustpadding(data))
    def decrypt(self, data):
        if self._key is None or data is None:
            return data
        _encryptor = AES.new(self._key, AES.MODE_CBC, self._passphrase)
        res=_encryptor.decrypt(data)
        return res[:res.find(self.pad_delimiter)]
