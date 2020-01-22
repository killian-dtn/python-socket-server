# -*- coding: utf-8 -*-

import tkinter as tk
import asyncio as aio
from typing import List
from kserverprotocol import KServer

class KServerInterface(tk.Tk):
    def __init__(self, server: KServer):
        super().__init__()
        self.CommandEntry: tk.Entry = tk.Entry(self)
        self.ClientsListbox: tk.Listbox = tk.Listbox()
        self.server: KServer = server
        self.loop: aio.BaseEventLoop = self.server.loop
        self.tasks: List[aio.Task] = []
        self.tasks.append(self.loop.create_task(self.__MainloopAsync()))
        self.protocol("WM_DELETE_WINDOW", self.Close)
    async def __MainloopAsync(self):
        while True:
            self.update()
            await aio.sleep(0)
    def Run(self):
        self.server.RunServer()
    def Close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

KServerInterface(KServer(55555)).Run()
