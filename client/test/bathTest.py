import os
import time


def run():
    for i in range(200):
        os.system('start cmd /k ; cd C:\\讯首WorkSpace\\MyCode\\GrpcClient\\Publish ^& GrpcClient.exe')
        # os.system('start "grpcClient" /d "C:\\讯首WorkSpace\\MyCode\\GrpcClient\\Publish" /wait "GrpcClient.exe"')
        # time.sleep(1)

    print('success')


if __name__ == "__main__":
    run()
