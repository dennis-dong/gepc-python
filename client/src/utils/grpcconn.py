import json
import requests
from stub.service_pb2 import *
from stub.service_pb2_grpc import *


def getServerList():
    '''
    获取可用服务器列表
    '''
    url = "http://192.168.10.215:8500/v1/agent/services"
    headers = {'X-Consul-Token': 'c10dbaf5-7da5-eb1a-61bc-d2e2c7b3e05c'}

    response = requests.request("GET", url, headers=headers)
    jsonRes = json.loads(response.text)
    serverList = []

    for i in jsonRes:
        # 自动根据id获取
        print(i)
        serverInfo = jsonRes[i]
        address = serverInfo['Address']
        port = serverInfo['Port']
        serverList.append(f'{address}:{port}')

    return serverList

def connection(host: str = 'localhost', port: int = 7000, enableSSL: bool = True):
    '''
    创建grpc服务器连接
    '''
    if enableSSL:
        options = (('grpc.ssl_target_name_override', 'grpc.dennis.com'), )
        kwargs = {
            'target': f"{host}:{port}",
            'options': (
                ("grpc.lb_policy_name", "round_robin"),  # 自动根据dns域名解析服务列表
                *options)
        }
        with open('cert/cert.pem', 'rb') as f:
            root_certificates = f.read()

        creds = grpc.ssl_channel_credentials(root_certificates)
        channel = grpc.secure_channel(**kwargs, credentials=creds)
    else:
        channel = grpc.insecure_channel(f"{host}:{port}")

    return GreeterStub(channel)