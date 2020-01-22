# -*- coding: utf-8 -*-

import KServer, asyncio as aio

class KProtocol(aio.Protocol):
    def __init__(self, server: KServer):
        self.__server = server
        self.__sock_transport: aio.Transport = None
    def connection_made(self, transport: aio.Transport):
        self.__sock_transport = transport
        self.__server.ConnectionMade(self.__sock_transport)
    def connection_lost(self, exc: Exception):
        self.__server.ConnectionLost(exc, self.__sock_transport)
    def data_received(self, data: bytes):
        self.__server.DataReceived(data, self.__sock_transport)
