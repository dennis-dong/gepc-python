# -*- coding: utf-8 -*-

import random
from src.utils import grpcconn


def run():
    serverList = grpcconn.getServerList()
    index=random.randrange(0, serverList)
    server = serverList[index]

