# -*- coding: utf-8 -*-

from kserver import KServer, KServerInterface

def HelloWorld(interface, target):
    target.write(b"Hello world !")

def main():
    iface = KServerInterface(KServer(55555))
    iface.commands["helloworld"] = HelloWorld
    iface.Run()

main()
