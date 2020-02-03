# -*- coding: utf-8 -*-

from kserver import KServer, KServerInterface

def Send(interface, target, *args):
    target.write((" ".join(args)).encode("utf8"))

def main():
    iface = KServerInterface(KServer(55555))
    iface.commands["helloworld"] = lambda interface, target, *args: Send(interface, target, "Hello World!")
    iface.commands["send"] = Send
    iface.Run()

main()
