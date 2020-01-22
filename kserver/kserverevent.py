# -*- coding: utf-8 -*-

class KServerEvent():
    def __init__(self):
        self.__tasks = set()
    def __iadd__(self, handler):
        self.__tasks.add(handler)
        return self
    def __isub__(self, handler):
        try:
            self.__tasks.remove(handler)
        except:
            raise ValueError("No handler.")
        return self
    def __len__(self):
        return len(self.__tasks)
    def __call__(self, sender: object, msg: str):
        for task in self.__tasks:
            task(sender, msg)
