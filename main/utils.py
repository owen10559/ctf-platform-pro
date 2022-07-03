import docker
import time
import json

with open("config.json", "r") as f:
    config = json.load(f)

client = docker.from_env()

# class Container(docker.models.containers.Container):

#     def __init__(self, container):
#         self = container

#     def get_name(self):
#         print(self.attrs["Name"])

#     # def is_running(client:docker.DockerClient):

def command_parse(s:str):
    '''
    命令解析器，只能解析单个选项单个参数的命令，格式参考Unix风格（如果参数不够用，也可以加入GNU风格的参数）
    >>> s = "cmd p1 -o p2"
    >>> command_parse(s)
    ("cmd", {"cmd":"p1", "-o":"p2"})
    '''

    result = s.split(" ")
    command = result[0]

    parser = {}
    option = ""
    argument = ""

    for arg in result[1:]:
        if arg[0] == "-":
            if option == "":
                option = arg
            else:
                if argument == "":
                    parser.update({option:None})
                else:
                    parser.update({option:argument})
                option = arg
                argument = ""
        else:
            argument = arg

        if argument == "":
            parser.update({option:None})
        elif option == "":
            parser.update({command:argument})
        else:
            parser.update({option:argument})
    return command, parser

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

def set_training_status(training_name:str, status_code:int):
    with open("trainings/%s/status" % training_name, "w") as f:
        f.write(str(status_code))

def is_ready(training_name:str):
    """
    判断指定training的status文件的内容是否为“1”
    """
    with open("trainings/%s/status" % training_name, "r") as f:
        if f.read() == "1":
            return True
        else:
            return False

def is_verified(training_name:str):
    """
    判断指定training是否已完成
    """
    with open("trainings/info.json","r") as f:
        info=json.load(f)
    if info[training_name] == True :
        return True
    else:
        return False

def wait_training_init(training_name:str):
    """
    等待training初始化成功

    返回结果（初始化成功或超时）
    """
    for i in range(config["max_init_time"]):
        print("\rInitializing...time consumed:", i, end="")
        if is_ready(training_name):
            print()
            return True
        else:
            time.sleep(1)
    print()
    return False