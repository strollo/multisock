import unittest
from unittest.mock import MagicMock, patch
from multisock.channel import Channel
from multisock.crypter import Crypter


class Test_Channel(unittest.TestCase):
    def setUp(self):
        self.mock_socket = patch('multisock.channel.socket').start()
        self.mock_struct = patch('multisock.channel.struct').start()

    def tearDown(self):
        # ensure all patches (if any are stopped once done)
        patch.stopall()

    def test_channel_ctor(self):
        reader_writer_mock = MagicMock()
        aton_mock = MagicMock(return_value=bytes())
        inaddr_any_mock = MagicMock(return_value=123)
        mreq_mock = MagicMock()
        proto_ip_mock = MagicMock()
        ip_membership_mock = MagicMock()
        SOL_SOCKET_mock = MagicMock()
        SO_REUSEADDR_mock = MagicMock()

        self.mock_socket.socket.return_value = reader_writer_mock
        self.mock_socket.inet_aton.return_value = aton_mock
        self.mock_socket.INADDR_ANY = inaddr_any_mock
        self.mock_struct.pack = MagicMock(return_value=mreq_mock)
        self.mock_socket.IPPROTO_IP = proto_ip_mock
        self.mock_socket.IP_ADD_MEMBERSHIP = ip_membership_mock
        self.mock_socket.SOL_SOCKET = SOL_SOCKET_mock
        self.mock_socket.SO_REUSEADDR = SO_REUSEADDR_mock

        crypto = Crypter('pwd', 'passphrase')

        #################
        # WHEN - CTOR
        #################
        chan = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', crypto)

        # THEN
        self.assertTrue(chan.mcast_ip == '224.1.1.1')
        self.assertTrue(chan.mcast_port == 1234)
        self.assertTrue(chan.bufsize == 2048)
        self.assertTrue(chan.iface_ip == '0.0.0.0')
        self.assertTrue(chan.crypto == crypto)

        chan.reader.setsockopt.assert_called()
        chan.reader.bind.assert_called_with((chan.iface_ip, chan.mcast_port))
        chan.reader.setsockopt.assert_called_with(proto_ip_mock, ip_membership_mock, mreq_mock)
        chan.reader.setblocking.assert_called_with(1)

        chan.writer.setsockopt.assert_called()
        chan.writer.bind.assert_called_with((chan.iface_ip, chan.mcast_port))
        chan.writer.setsockopt.assert_called_with(proto_ip_mock, ip_membership_mock, mreq_mock)

        self.mock_struct.pack.assert_called_with("4sI", aton_mock, inaddr_any_mock)

        #################
        # WHEN - SEND
        #################
        chan.send('Hello')

        # THEN
        chan.writer.sendto.assert_called_with(crypto.encrypt('Hello'), (chan.mcast_ip, chan.mcast_port))

        #################
        # WHEN - RECV
        #################
        chan.reader.recvfrom = MagicMock(return_value=(crypto.encrypt('Response Data'), 'sender_addr'))
        (data, sender) = chan.recv()

        self.assertTrue(data == 'Response Data')
        self.assertTrue(sender == 'sender_addr')

        #################
        # WHEN - CLOSE
        #################
        chan.close()

        # THEN
        chan.writer.close.assert_called()
        chan.reader.close.assert_called()

    def test_channel_ctor_invalid_crypter_type(self):
        with self.assertRaises(ValueError):
            Channel('224.1.1.1', 1234, 2048, '0.0.0.0', MagicMock())

    def test_channel_ctor_missing_ifaceip(self):
        crypto = Crypter('pwd', 'passphrase')
        chan = Channel('224.1.1.1', 1234, 2048, None, crypto)

        self.assertTrue(chan.iface_ip == '0.0.0.0')

        chan.close()

    def test_channel_set_read_blocking(self):
        reader_writer_mock = MagicMock()
        aton_mock = MagicMock(return_value=bytes())
        inaddr_any_mock = MagicMock(return_value=123)
        mreq_mock = MagicMock()
        proto_ip_mock = MagicMock()
        ip_membership_mock = MagicMock()
        SOL_SOCKET_mock = MagicMock()
        SO_REUSEADDR_mock = MagicMock()

        self.mock_socket.socket.return_value = reader_writer_mock
        self.mock_socket.inet_aton.return_value = aton_mock
        self.mock_socket.INADDR_ANY = inaddr_any_mock
        self.mock_struct.pack = MagicMock(return_value=mreq_mock)
        self.mock_socket.IPPROTO_IP = proto_ip_mock
        self.mock_socket.IP_ADD_MEMBERSHIP = ip_membership_mock
        self.mock_socket.SOL_SOCKET = SOL_SOCKET_mock
        self.mock_socket.SO_REUSEADDR = SO_REUSEADDR_mock

        crypto = Crypter('pwd', 'passphrase')

        chan = Channel('224.1.1.1', 1234, 2048, '0.0.0.0', crypto)

        # WHEN
        chan.set_read_blocking(False)
        # THEN
        chan.reader.setblocking.assert_called_with(0)

        # WHEN
        chan.set_read_blocking(True)
        # THEN
        chan.reader.setblocking.assert_called_with(1)

        chan.close()

    def test_channel_repr(self):
        crypto = Crypter('pwd', 'passphrase')
        chan = Channel('224.1.1.1', 1234, 2048, None, crypto)

        s = str(chan)

        self.assertTrue(s == 'MulticastCh<224.1.1.1:1234>')

        chan.close()

    def test_channel_read_empty_data(self):
        crypto = Crypter('pwd', 'passphrase')
        chan = Channel('224.1.1.1', 1234, 2048, None, crypto)

        # HAVING
        chan.reader.recvfrom = MagicMock(return_value=(None, 'sender_addr'))
        # WHEN
        retval = chan.recv()
        # THEN
        self.assertIsNone(retval)

        chan.close()

    def test_channel_reader_close_exception(self):
        crypto = Crypter('pwd', 'passphrase')
        chan = Channel('224.1.1.1', 1234, 2048, None, crypto)

        # HAVING
        chan.reader.close = MagicMock(side_effect=Exception())
        # OBSERVE EXCEPTION
        with self.assertRaises(Exception):
            chan.close()
