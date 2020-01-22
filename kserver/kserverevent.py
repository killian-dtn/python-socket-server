# -*- coding: utf-8 -*-

from typing import List

class KServerEvent():
    def __init__(self):
        self.__tasks: List[callable] = []
    def __call__(self):
        for task in self.tasks:
            task()
    def InsertTask(self, task: callable):
        self.__tasks.append(task)
