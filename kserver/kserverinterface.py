# -*- coding: utf-8 -*-

import tkinter as tk
import asyncio as aio
from typing import List, Dict
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
        self.ClientsListbox: tk.Listbox = tk.Listbox(self, selectmode = tk.MULTIPLE)
        # ------------------------------ Events -------------------------------
        self.server.ConnectionMadeEvent += self.ConnectionMade
        self.server.ConnectionLostEvent += self.ConnectionLost
        self.server.DataReceivedEvent += self.DataReceived
        # ---------------------------------------------------------------------
        self.protocol("WM_DELETE_WINDOW", self.Close)
        self.commands: Dict[str, callable] = {}
        self.clts: Dict[str, aio.Transport] = {}
    async def __MainloopAsync(self):
        while True:
            self.update()
            await aio.sleep(0)
    # ------------------------ Server Events functions ------------------------
    def ConnectionMade(self, sender, client: aio.Transport):
        txt: str = str(client.get_extra_info("peername"))
        self.ClientsListbox.insert(tk.END, txt)
        self.clts[txt] = client
    def ConnectionLost(self, sender, reason: Exception, client: aio.Transport):
        self.ClientsListbox.delete(0, tk.END)
        self.clts.pop(str(client.get_extra_info("peername")))
        if len(self.clts) > 0:
            for clt in list(self.clts.keys()):
                self.ClientsListbox.insert(tk.END, clt)
    def DataReceived(self, sender, msg: bytes, client: aio.Transport):
        pass
    # -------------------------------------------------------------------------
    def ExecCommand(self, command: str):
        selected_items = [self.ClientsListbox.get(i) for i in self.ClientsListbox.curselection()]
        try:
            if command not in self.commands.keys(): raise KeyError
            for item in selected_items:
                self.commands[command](interface = self, target = self.clts[item])
        except KeyError:
            self.server.Log(msg = f"No command \"{command}\".")
        except Exception:
            raise
        finally:
            self.server.Log(msg = f"Command : {command}, on target(s) : {selected_items}")
        self.CommandEntry.delete(0, tk.END)
    def Render(self):
        self.ClientsListbox.pack(fill = tk.BOTH, expand = True)
        self.CommandEntry.pack(fill = tk.X, expand = False)
        self.CommandEntry.bind("<Return>", lambda event: self.ExecCommand(self.CommandEntry.get()))
    def Run(self):
        self.Render()
        self.server.RunServer()
    def Close(self):
        for task in self.tasks:
            task.cancel()
        self.server.StopServer()
        self.loop.stop()
        self.destroy()
