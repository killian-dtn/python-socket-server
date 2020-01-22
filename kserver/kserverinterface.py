# -*- coding: utf-8 -*-

import tkinter as tk
import asyncio as aio
from typing import List
from . import KServer

class KServerInterface(tk.Tk):
    def __init__(self, server: KServer):
        super().__init__()
        self.server: KServer = server
        self.loop: aio.BaseEventLoop = self.server.loop
        self.tasks: List[aio.Task] = []
        self.tasks.append(self.loop.create_task(self.__MainloopAsync()))
        # ------------------------------ Widgets ------------------------------
        self.CommandEntry: tk.Entry = tk.Entry(self)
        self.ClientsListbox: tk.Listbox = tk.Listbox(self)
        # ------------------------------ Events -------------------------------
        self.server.ConnectionMadeEvent += self.ConnectionMade
        self.server.ConnectionLostEvent += self.ConnectionLost
        self.server.DataReceivedEvent += self.DataReceived
        # ---------------------------------------------------------------------
        self.protocol("WM_DELETE_WINDOW", self.Close)
    async def __MainloopAsync(self):
        while True:
            self.update()
            await aio.sleep(0)
    # ---------------------------- Event functions ----------------------------
    def ConnectionMade(self, sender, client: aio.Transport):
        self.ClientsListbox.insert(tk.END, client)
    def ConnectionLost(self, sender, reason: Exception, client: aio.Transport):
        self.ClientsListbox.delete(0, tk.END)
        self.ClientsListbox.insert(tk.END, list(self.server.clts.keys()))
    def DataReceived(self, sender, msg: bytes, client: aio.Transport):
        pass
    # -------------------------------------------------------------------------
    def Render(self):
        self.ClientsListbox.pack(fill = tk.BOTH, expand = True)
        self.CommandEntry.pack(fill = tk.X, expand = False)
    def Run(self):
        self.Render()
        self.server.RunServer()
    def Close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()
