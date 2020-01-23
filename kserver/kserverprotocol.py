# -*- coding: utf-8 -*-

import socket, asyncio as aio, time
from typing import Dict
from . import KServerEvent

class KServer():
    def __init__(self, port: int, Log: callable = lambda msg: print("{} : {}".format(time.strftime("[%H:%M:%S]"), msg))):
        self.__server: aio.Server = None
        self.loop: aio.BaseEventLoop = aio.get_event_loop()
        self.port: int = port
        self.Log: callable = Log
        self.clts: Dict[aio.Transport, object] = {}
        # ------------------------ Events ------------------------
        self.ConnectionMadeEvent: KServerEvent = KServerEvent() # args : client
        self.ConnectionLostEvent: KServerEvent = KServerEvent() # args : reason, client
        self.DataReceivedEvent: KServerEvent = KServerEvent()   # args : msg, client
        # --------------------------------------------------------
    async def __async_init(self):
        self.__server = await self.loop.create_server(lambda : KProtocol(self), host = '', port = self.port, family = socket.AF_INET)
        await self.__server.start_serving()
    def RunServer(self):
        self.loop.create_task(self.__async_init())
        self.loop.run_forever()
    def StopServer(self):
        self.__server.close()
    # -------------------- Protocol callbacks --------------------
    def ConnectionMade(self, transport: aio.Transport):
        self.clts[transport] = transport.get_extra_info("peername")
        self.ConnectionMadeEvent(self, client = transport)
        self.Log(msg = f"Connexion made : {self.clts[transport]}")
    def ConnectionLost(self, exc: Exception, transport: aio.Transport):
        self.Log(msg = f"Connexion lost : {self.clts[transport]}")
        self.clts.pop(transport)
        self.ConnectionLostEvent(self, reason = exc, client = transport)
    def DataReceived(self, data: bytes, transport: aio.Transport):
        self.DataReceivedEvent(self, msg = data, client = transport)
        self.Log(msg = f"Received from {self.clts[transport]} : {data}")
    # ------------------------------------------------------------

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
