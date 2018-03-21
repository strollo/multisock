#!/usr/bin/env python

from context import *
import json
import unittest

class TestStringMethods(unittest.TestCase):
    def test_MessageToJson(self):
        m = SerializableData()
        m.info = SerializableData()
        m.info.name = 'Daniele'
        m.info.surname = 'Strollo'

        # Object to string
        jsonStr=m.toJSON()
        self.assertIsNotNone(jsonStr)
        self.assertTrue(len(jsonStr) > 0)

        # json string to dictionary
        fromJson = json.loads(jsonStr)
        self.assertIsNotNone(jsonStr)

        self.assertTrue(fromJson.has_key('info'))
        info=fromJson['info']
        self.assertTrue(info.has_key('name'))
        self.assertTrue(info['name'] == 'Daniele')
        self.assertTrue(info.has_key('surname'))
        self.assertTrue(info['surname'] == 'Strollo')

    def test_JsonToMessage(self):
        _json='''
        {
            "info": {
                "name": "Daniele",
                "surname": "Strollo"
            },
            "sender": "tester",
            "token": "#1"
        }
        '''
        msg=SerializableData.fromJSON(_json)
        self.assertTrue(msg.sender == 'tester')
        self.assertTrue(msg.token == '#1')
        self.assertTrue(msg.info.name == 'Daniele')
        self.assertTrue(msg.info.surname == 'Strollo')


if __name__ == '__main__':
    unittest.main()