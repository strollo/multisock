import unittest
from unittest.mock import patch
import random
import string
from multisock.crypter import Crypter
from multisock.exceptions import InvalidParameterException, InvalidKeyLenghtException, EncryptionInvalidParameterException

class SerializableObject():
    def __init__(self, token, payload={}):
        if token is None or not isinstance(token, str):
            raise ValueError('Invalid token parameter')
        self.token = token.strip()
        self.payload = payload


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class Test_Crypter(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # ensure all patches (if any are stopped once done)
        patch.stopall()

    def test_crypter_ctor_with_invalid_parameters(self):
        with self.assertRaises(InvalidParameterException):
            Crypter(key=None, iv='ValidIV')
        with self.assertRaises(InvalidParameterException):
            Crypter(key='    ', iv='ValidIV')
        with self.assertRaises(InvalidParameterException):
            Crypter(key='ValidKey', iv=None)
        with self.assertRaises(InvalidParameterException):
            Crypter(key='ValidKey', iv='    ')

    def test_crypter_ctor_with_too_long_key(self):
        with self.assertRaises(InvalidKeyLenghtException):
            Crypter(key=get_random_string(33), iv='The IV')

    def test_crypter_encrypt_null_parameter(self):
        with self.assertRaises(InvalidParameterException):
            c = Crypter(key=get_random_string(32), iv='The IV')
            c.encrypt(None)

    def test_crypter_decrypt_null_parameter(self):
        with self.assertRaises(InvalidParameterException):
            c = Crypter(key=get_random_string(32), iv='The IV')
            c.decrypt(None)

    def test_crypter_encrypt_with_invalid_parameter_type(self):
        with self.assertRaises(EncryptionInvalidParameterException):
            c = Crypter(key=get_random_string(32), iv='The IV')
            c.encrypt({'key': 'value'})

    def test_encrypt_and_decrypt(self):
        crypter = Crypter(key=' --- My Key --- ', iv='The IV')
        initial_string = '   Hello World   '
        encrypted = crypter.encrypt(initial_string)
        self.assertTrue(crypter.decrypt(encrypted) == initial_string)

    def test_encrypt_and_decrypt_key_not_16bytes_should_pad_key(self):
        crypter = Crypter(key='SampleKey', iv='The IV')
        initial_string = '   Hello World   '
        encrypted = crypter.encrypt(initial_string)
        self.assertTrue(crypter.decrypt(encrypted) == initial_string)

    def test_encrypt_and_decrypt_wrong_iv(self):
        crypter = Crypter(key=' --- My Key --- ', iv='The IV')
        initial_string = '   Hello World   '
        encrypted = crypter.encrypt(initial_string)

        decrypter = Crypter(key=' --- My Key --- ', iv='Another IV')
        self.assertFalse(decrypter.decrypt(encrypted) == initial_string)

    def test_encrypt_and_decrypt_wrong_key(self):
        crypter = Crypter(key=' --- My Key --- ', iv='The IV')
        initial_string = '   Hello World   '
        encrypted = crypter.encrypt(initial_string)

        decrypter = Crypter(key=' --- No Key --- ', iv='The IV')
        self.assertFalse(decrypter.decrypt(encrypted) == initial_string)

    def test_encrypt_long_message_and_decrypt(self):
        crypter = Crypter(key=' --- My Key --- ', iv='The IV')
        initial_string = get_random_string(6000)
        encrypted = crypter.encrypt(initial_string)
        self.assertTrue(crypter.decrypt(encrypted) == initial_string)

    def test_encrypt_long_key_and_decrypt(self):
        crypter = Crypter(key=get_random_string(32), iv='The IV')
        initial_string = get_random_string(1024)
        encrypted = crypter.encrypt(initial_string)
        self.assertTrue(crypter.decrypt(encrypted) == initial_string)

    def test_encrypt_bytebuffer(self):
        crypter = Crypter(key=get_random_string(32), iv='The IV')
        initial_string = bytearray(random.getrandbits(8) for _ in range(1024))
        encrypted = crypter.encrypt(initial_string)
        decrypted = crypter.decrypt(encrypted)
        self.assertTrue(len(decrypted) == len(initial_string))
        self.assertTrue(decrypted == initial_string)

    def test_encrypt_bytebuffer_notaligned(self):
        crypter = Crypter(key=get_random_string(32), iv='The IV')
        initial_string = bytearray(random.getrandbits(8) for _ in range(723))
        encrypted = crypter.encrypt(initial_string)
        decrypted = crypter.decrypt(encrypted)
        self.assertTrue(len(decrypted) == len(initial_string))
        self.assertTrue(decrypted == initial_string)

    def test_encrypt_bytebuffer_notaligned_with_not_padded_key(self):
        crypter = Crypter(key=get_random_string(24), iv='The IV')
        initial_string = bytearray(random.getrandbits(8) for _ in range(723))
        encrypted = crypter.encrypt(initial_string)
        decrypted = crypter.decrypt(encrypted)
        self.assertTrue(len(decrypted) == len(initial_string))
        self.assertTrue(decrypted == initial_string)

    def test_encrypt_bytestring(self):
        crypter = Crypter(key=get_random_string(24), iv='The IV')
        initial_string = b'Hello'
        encrypted = crypter.encrypt(initial_string)
        decrypted = crypter.decrypt(encrypted)
        self.assertTrue(len(decrypted) == len(initial_string))
        self.assertTrue(bytes(decrypted, 'utf-8') == initial_string)

    def test_serializable_object(self):
        crypter = Crypter(key=get_random_string(24), iv='The IV')
        import pickle
        import base64

        # Encryption
        obj = SerializableObject(token='/patter/tester', payload={'key1': 'value1', 'key2': 123})
        obj_b64 = base64.b64encode(pickle.dumps(obj))
        encrypted_bytes = crypter.encrypt(obj_b64)

        # Decryption
        decrypted_bytes = crypter.decrypt(encrypted_bytes)
        decrypted_b64 = base64.b64decode(decrypted_bytes)
        decrypted_obj = pickle.loads(decrypted_b64)

        # Compare objects after encryption/serialization
        self.assertTrue(pickle.dumps(obj) == pickle.dumps(decrypted_obj))
