# -*- coding: utf-8 -*-

import socket, asyncio as aio, time
from aioconsole import ainput
from typing import Dict

class KServer():
    def __init__(self, port: int, Log: callable = lambda msg: print("{} : {}".format(time.strftime("[%H:%M:%S]"), msg))):
        self.__server: aio.Server = None
        self.loop: aio.BaseEventLoop = aio.get_event_loop()
        self.port: int = port
        self.Log: callable = Log
        self.clts: Dict[aio.Transport, object] = {}
    async def __async_init(self):
        self.__server = await self.loop.create_server(lambda : KProtocol(self), host = '', port = self.port, family = socket.AF_INET)
        await self.__server.start_serving()
    async def SendInput(self):
        while True:
            if len(self.clts) > 0:
                msg = (await ainput(">>>"))
                for clt in list(self.clts.keys()):
                    clt.write(msg.encode("utf8"))
            await aio.sleep(0)
    # def Log(msg: str):
    #     print("{} : {}".format(time.strftime("[%H:%M:%S]"), msg))
    def RunServer(self):
        self.loop.create_task(self.__async_init())
        #self.loop.create_task(self.SendInput())
        self.loop.run_forever()
    # -------------------- Protocol callbacks --------------------
    def ConnectionMade(self, transport: aio.Transport):
        self.clts[transport] = transport.get_extra_info("peername")
        self.Log("Connexion made : {}".format(self.clts[transport]))
    def ConnectionLost(self, exc: Exception, transport: aio.Transport):
        self.Log("Connexion lost : {}".format(self.clts[transport]))
        self.clts.pop(transport)
    def DataReceived(self, data: bytes, transport: aio.Transport):
        self.Log(f"Received from {self.clts[transport]} : {data}")
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