#!/usr/bin/env python

# Include parent folder in module resolution
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SerializableObject():
    """
    Class used for serializing object to be trasmitted in samples.
    """
    def __init__(self, token, payload={}):
        if token is None or not isinstance(token, str):
            raise ValueError('Invalid token parameter')
        self.token = token.strip()
        self.payload = payload
