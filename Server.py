# -*- coding: utf-8 -*-

import socket, asyncio, time
from aioconsole import ainput
from typing import Dict

class KServer():
    def __init__(self):
        self.__loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
        self.__server: asyncio.Server = None
        self.clts: Dict[asyncio.Transport, object] = {}
    async def __async_init(self):
        self.__server = await self.__loop.create_server(lambda : KProtocol(self), host = '', port = 55555, family = socket.AF_INET)
        await self.__server.start_serving()
    async def SendInput(self):
        while True:
            if len(self.clts) > 0:
                msg = (await ainput(">>>"))
                for clt in list(self.clts.keys()):
                    clt.write(msg.encode("utf8"))
            await asyncio.sleep(0)
    def Log(msg: str):
        print("{} : {}".format(time.strftime("[%H:%M:%S]"), msg))
    def RunServer(self):
        self.__loop.create_task(self.__async_init())
        self.__loop.create_task(self.SendInput())
        self.__loop.run_forever()
    # -------------------- Protocol callbacks --------------------
    def ConnectionMade(self, transport: asyncio.Transport):
        self.clts[transport] = transport.get_extra_info("peername")
        KServer.Log("Connexion made : {}".format(self.clts[transport]))
    def ConnectionLost(self, exc: Exception, transport: asyncio.Transport):
        KServer.Log("Connexion lost : {}".format(self.clts[transport]))
        self.clts.pop(transport)
    def DataReceived(self, data: bytes, transport: asyncio.Transport):
        KServer.Log(f"Received from {self.clts[transport]} : {data}")
    # ------------------------------------------------------------

class KProtocol(asyncio.Protocol):
    def __init__(self, server: KServer):
        self.__server = server
        self.__sock_transport: asyncio.Transport = None
    def connection_made(self, transport: asyncio.Transport):
        self.__sock_transport = transport
        self.__server.ConnectionMade(self.__sock_transport)
    def connection_lost(self, exc: Exception):
        self.__server.ConnectionLost(exc, self.__sock_transport)
    def data_received(self, data: bytes):
        self.__server.DataReceived(data, self.__sock_transport)

KServer().RunServer()