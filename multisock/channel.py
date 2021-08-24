#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Filename: channel.py
Implements a very small and easy to use channel for connecting UDP multicast channels with
simple operations for sending and receiving data.

How easy is it...?

#### THE CONSUMER ####
import multisock
# Create a connection to multicast group 224.1.1.1:1234
udpchan = multisock.Channel('224.1.1.1', 1234)
udpchan.send('Hello World')

#### THE PRODUCER ####
import multisock
# Create a connection to multicast group 224.1.1.1:1234
udpchan = multisock.Channel('224.1.1.1', 1234)
(data,sender)=udpchan.recv()
print "Received from %s: %s" % (sender, data)
"""

import socket
import struct
import logging
from multisock.crypter import Crypter

class Channel:
    """
    Creates a new udp multicast channel bound to a multicast group
    (e.g. 224.1.1.1) and a port.

    All components connected to this group will be able to exchange
    messages through the following primitives:
    - send/recv: by using buffers of data (bytes or more simply strings)

    The channels can be closed (disconnected) with channel.close() method.

    Additionally to ip/port parameters, it is possible to specify the max
    size of read/send buffers (by default 4k) and a custom logger that can
    be instantiated with the logfactory util.

    The optional parameter iface_ip allows to bind socket to a specific interface given
    its ip (e.g. localhost/0.0.0.0....)

    Note: the instantiation of a channel implicitly connects to the multicast group.
    """

    def __init__(self, mcast_ip, mcast_port, bufsize=4096, iface_ip=None, crypto=None):
        self.mcast_ip = mcast_ip
        self.mcast_port = mcast_port
        self.bufsize = bufsize
        self.writer = None
        self.reader = None
        if crypto is not None and not isinstance(crypto, Crypter):
            raise ValueError('Invalid crypto parameter. DataCrypto instance expected')
        self.crypto = crypto
        if iface_ip is not None and len(iface_ip.strip()) > 0:
            self.iface_ip = iface_ip.strip()
        else:
            self.iface_ip = '0.0.0.0'

        self.logger = logging.getLogger()
        self.__init_protocol__()

        self.logger.info('Creating UDP Channel on {ip} {port}', ip=self.mcast_ip, port=self.mcast_port)

    def __init_protocol__(self):
        # UDP socket writer
        self.writer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.writer.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.writer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _mreq = struct.pack("4sI", socket.inet_aton(self.mcast_ip), socket.INADDR_ANY)
        self.writer.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, _mreq)
        self.writer.bind((self.iface_ip, self.mcast_port))

        # UDP socket reader
        self.reader = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.reader.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _mreq = struct.pack("4sI", socket.inet_aton(self.mcast_ip), socket.INADDR_ANY)
        self.reader.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, _mreq)
        # setblocking(0) is equiv to settimeout(0.0) which means we poll the socket.
        # But this will raise an error if recv() or send() can't immediately find or send data.
        self.reader.setblocking(1)
        self.reader.bind((self.iface_ip, self.mcast_port))

    def __repr__(self):
        return 'MulticastCh<%s:%d>' % (self.mcast_ip, self.mcast_port)

    def set_read_blocking(self, blocking=True):
        """
        By default a channel is considered blocking in read, that means that
        a component which tries to read from a channel will wait until new
        data is available.
        This behaviour can be changed by setting the read non blocking thus
        allowing the developer to implement manual polling on channels.
        """
        if blocking:
            self.reader.setblocking(1)
        else:
            self.reader.setblocking(0)

    def close(self):
        """
        Closes the connection to the multicast group.
        """
        raised_exception = None
        try:
            self.reader.close()
        finally:
            self.writer.close()

    def send(self, data):
        """
        Sends data on the channel. What else?
        """
        if self.crypto is not None:
            data = self.crypto.encrypt(data)
        self.writer.sendto(data, (self.mcast_ip, self.mcast_port))

    def recv(self):
        """
        Receives data from the channel and returns a couple
            (data,addr)
        where addr is the sender address.
        """
        data, addr = self.reader.recvfrom(self.bufsize)
        if (data is None or len(data) == 0):
            return None
        if self.crypto is not None:
            data = self.crypto.decrypt(data)
        return data, addr
