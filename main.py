# -*- coding: utf-8 -*-

from kserver import KServer, KServerInterface

def main():
    KServerInterface(KServer(55555)).Run()

main()