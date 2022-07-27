import docker
import time
import json

with open("config.json", "r") as f:
    config = json.load(f)

client = docker.from_env()


def set_client(new_client:docker.DockerClient):
    global client
    client = new_client

def get_container(container_name:str):
    '''
    只能获取正在运行的容器（因此也可以用来判定容器是否在运行）
    '''
    for container in client.containers.list():
        if container.name == container_name:
            return container

def get_export_port(container):
    '''
    只能获取一个开放的端口
    '''
    return list(container.attrs["NetworkSettings"]["Ports"].values())[0][0]["HostPort"]

# def set_training_status(training_name:str, status_code:int):
#     with open("trainings/%s/status" % training_name, "w") as f:
#         f.write(str(status_code))

def is_ready(training_name:str, training_id:str):
    """
    判断指定training是否初始化完成
    """
    with open("trainings/%s/status" % training_name, "r") as f:
        if training_id+":1\n" in f.readlines():
            return True
        else:
            return False

# def is_verified(training_name:str):
#     """
#     判断指定training是否已完成
#     """
#     with open("trainings/info.json","r") as f:
#         info=json.load(f)
#     if info[training_name] == True :
#         return True
#     else:
#         return False

# def wait_training_init(training_name:str):
#     """
#     等待training初始化成功

#     返回结果（初始化成功或超时）
#     """
#     for i in range(config["max_init_time"]):
#         print("\rInitializing...time consumed:", i, end="")
#         if is_ready(training_name):
#             print()
#             return True
#         else:
#             time.sleep(1)
#     print()
#     return False