#! /usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
import time
from concurrent import futures
from service_pb2 import *
from service_pb2_grpc import *

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(GreeterServicer):

    def SayHello(self, request, context):
        return HelloReply(message='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('localhost:5000')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()