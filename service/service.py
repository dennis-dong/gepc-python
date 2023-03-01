# -*- coding: utf-8 -*-
# Author: areful
#
# pip install grpcio
# pip install protobuf
# pip install grpcio-tools
# ...

# Copyright 2015, Google Inc.
# All rights reserved.
"""The Python implementation of the GRPC helloworld.Greeter server."""

import logging
import os
import time
from concurrent import futures

from service_pb2 import *
from service_pb2_grpc import *

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(GreeterServicer):

    def SayHello(self, request, context):
        return HelloReply(message='Hello, %s!' % request.name)


logging.basicConfig(
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
logger: logging.Logger = logging.getLogger()


def serve(host: str = 'localhost', port: int = 7000, enableSSL: bool = True):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GreeterServicer_to_server(Greeter(), server)

    if enableSSL:
        # 如果是启用了ssl,则读取文件，然后建立一个安全的连接
        # read in key and certificate
        with open(os.path.join(os.path.split(__file__)[0], "cert/server.pem")) as f:
            private_key = f.read().encode()
        with open(os.path.join(os.path.split(__file__)[0], "cert/cert.pem")) as f:
            certificate_chain = f.read().encode()
        # create server credentials
        server_creds = grpc.ssl_server_credentials(((
            private_key,
            certificate_chain,
        ), ))
        server.add_secure_port(f"{host}:{port}", server_creds)
    else:
        # 否则建立一个普通的连接
        server.add_insecure_port(f"{host}:{port}")

    # 启动服务
    server.start()
    try:
        # 打印我们挂载了多少个子服务(也就是上面注册的服务)
        for generic_handler in server._state.generic_handlers:
            logger.info(f"add service name:{generic_handler.service_name()} cnt:{len(generic_handler._method_handlers)}")
        logger.info(f"server run in {host}:{port}")
        # 一直运行，直到被关闭
        server.wait_for_termination()
    except KeyboardInterrupt:
        # 收到退出的信号，关闭服务
        server.stop(0)


if __name__ == '__main__':
    serve()