import unittest
import random
import string
import multiprocessing
from multiprocessing import Process
from multisock.channel import Channel
from multisock.crypter import Crypter


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def do_send(sender, msg):
    sender.send(msg)


def do_recv(receiver, result_buffer):
    (msg, sender) = receiver.recv()
    result_buffer.put(msg)
    return result_buffer

def do_send_object(sender, obj):
    print('object sent')
    sender.send_object(obj)

def do_recv_object(receiver, result_buffer):
    (msg, sender) = receiver.recv_object()
    print('object received')
    result_buffer.put(msg)
    return result_buffer

class Test_Channel_E2E(unittest.TestCase):

    def test_message_exchange(self):
        crypto = Crypter('pwd', 'passphrase')
        sender = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', crypto)
        receiver = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', crypto)

        msg_to_send = get_random_string(1024)

        sender_th = Process(target=do_send, args=(sender, msg_to_send,))
        # creating multiprocessing Queue
        results = multiprocessing.Queue()
        receiver_th = Process(target=do_recv, args=(receiver, results))

        # Init threads
        sender_th.start()
        receiver_th.start()
        # Start threads
        sender_th.join()
        receiver_th.join()

        # Close Channels
        sender.close()
        receiver.close()

        self.assertTrue(results.qsize() == 1)
        received_msg = results.get()
        self.assertTrue(received_msg == msg_to_send)

    def test_object_exchange(self):
        crypto = Crypter('pwd', 'passphrase')
        sender = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', crypto)
        receiver = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', crypto)

        msg_to_send = {'number': get_random_string(1024), 'str': 'Hello world', 'bool': True}

        sender_th = Process(target=do_send_object, args=(sender, msg_to_send,))
        # creating multiprocessing Queue
        results = multiprocessing.Queue()
        receiver_th = Process(target=do_recv_object, args=(receiver, results))

        # Init threads
        sender_th.start()
        receiver_th.start()
        # Start threads
        sender_th.join()
        receiver_th.join()

        # Close Channels
        sender.close()
        receiver.close()

        self.assertTrue(results.qsize() >= 1)
        received_msg = results.get()
        self.assertTrue(received_msg == msg_to_send)

    def test_object_exchange_unencrypted(self):
        sender = Channel('224.1.1.1', 1234, 2048, '0.0.0.0')
        receiver = Channel('224.1.1.1', 1234, 2048, '0.0.0.0')

        msg_to_send = {'number': get_random_string(1024), 'str': 'Hello world', 'bool': True}

        sender_th = Process(target=do_send_object, args=(sender, msg_to_send,))
        # creating multiprocessing Queue
        results = multiprocessing.Queue()
        receiver_th = Process(target=do_recv_object, args=(receiver, results))

        # Init threads
        sender_th.start()
        receiver_th.start()
        # Start threads
        sender_th.join()
        receiver_th.join()

        # Close Channels
        sender.close()
        receiver.close()

        self.assertTrue(results.qsize() >= 1)
        received_msg = results.get()
        self.assertTrue(received_msg == msg_to_send)
