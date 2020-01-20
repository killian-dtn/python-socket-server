# -*- coding: utf-8 -*-

import asyncio
import async_timeout as asyncto
import socket
import time
from typing import Dict, Tuple
#from aioconsole import ainput

class Server():
    def __init__(self, port: int, listen_clt_max: int = 5, req_timeout: float = None):
        self.port: int = port
        self.listen_clt_max: int = listen_clt_max
        self.req_timeout = req_timeout
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clts: Dict[socket.socket, Tuple[object, object]] = {}
        self.need_stop: bool = False
        self.loop = asyncio.get_event_loop()
        self.sock.setblocking(False)
        self.sock.bind(('', self.port))
        self.sock.listen(self.listen_clt_max)
        asyncio.set_event_loop(self.loop)
    async def __SockAccept(self, use_timeout: bool = True):
        try:
            if use_timeout:
                async with asyncto.timeout(self.req_timeout):
                    return await self.loop.sock_accept(self.sock)
            else: return await self.loop.sock_accept(self.sock)
        except (asyncio.TimeoutError, ConnectionResetError, ConnectionAbortedError) as err:
            raise err
    async def __SockSendAll(self, client: socket.socket, msg: bytes, use_timeout: bool = True):
        try:
            if use_timeout:
                async with asyncto.timeout(self.req_timeout):
                    return await self.loop.sock_sendall(client, msg)
            else: return await self.loop.sock_sendall(client, msg)
        except (asyncio.TimeoutError, ConnectionResetError, ConnectionAbortedError) as err:
            raise err
    async def __SockRecv(self, client: socket.socket, msg_size: int, use_timeout: bool = True):
        try:
            if use_timeout:
                async with asyncto.timeout(self.req_timeout):
                    return await self.loop.sock_recv(client, msg_size)
            else: return await self.loop.sock_recv(client, msg_size)
        except (asyncio.TimeoutError, ConnectionResetError, ConnectionAbortedError) as err:
            raise err
    async def __AcceptLoopAsync(self):
        """
        Boucle qui accepte des clients en permanence.
        """
        while not self.need_stop:
            Server.__Log("Waiting for new clients ...")
            try:
                clt, clt_inf = await self.__SockAccept(False)
                self.clts[clt] = clt_inf
            except asyncio.TimeoutError:
                continue
            finally:
                await asyncio.sleep(1)
            Server.__Log(f"Accepted : {clt_inf}")
    async def __PingLoopAsync(self):
        """
        Ping en boucle sur tous les clients.
        """
        while not self.need_stop:
            if len(self.clts) > 0:
                Server.__Log("Start pinging all clients : {}".format(list(self.clts.values())))
                for clt, clt_inf in self.clts.copy().items():
                    Server.__Log(f"Sending Ping to {clt_inf} ...")
                    try:
                        await self.__SockSendAll(clt, b"Ping")
                        Server.__Log("Response from {} : {}.".format(clt_inf, await self.__SockRecv(clt, 255)))
                    except (asyncio.TimeoutError, ConnectionResetError, ConnectionAbortedError) as err:
                        Server.__Log(f"Ping not received : {err}")
                        self.clts.pop(clt)
                Server.__Log("All clients pinged.")
            else:
                Server.__Log("No client ...")
            await asyncio.sleep(1)
    def __Log(msg: str):
        """
        Affiche un message précédé de l'heure actuelle.
        """
        print("{} : {}".format(time.strftime("[%H:%M:%S]"), msg))
    async def __UselessLoop(self, msg: str, x: float):
        """
        Tests
        """
        while not self.need_stop:
            print(msg)
            await asyncio.sleep(x)
    def StartSrv(self):
        """
        Start accept and ping loops.
        """
        self.loop.create_task(self.__AcceptLoopAsync())
        self.loop.create_task(self.__PingLoopAsync())
        self.loop.run_forever()

print("Start : {}".format(time.strftime("[%H:%M:%S]")))
Server(55555, req_timeout = 1).StartSrv()

"""
#CLIENT POUR TEST

import socket
from time import strftime

def Log(msg: str):
    print("{} : {}".format(strftime("[%H:%M:%S]"), msg))

def f():
    while True:
        s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected: bool = False
        Log("Connecting ...")
        while not connected:
            try:
                s.connect(("localhost", 55555))
            except:
                continue
            connected = True
        try:
            while True:
                Log("Wait server message ...")
                msg = s.recv(255)
                Log(f"{msg} received, sending response.")
                if msg == b"Stop":
                    break
                s.send(b"Pong")
            s.close()
        except (ConnectionResetError, ConnectionAbortedError):
            Log("Connection lost ...")
        finally:
            s.close()

f()
"""