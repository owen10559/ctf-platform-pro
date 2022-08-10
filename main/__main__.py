import json
import re
import time
import threading
import docker

import apis


def training_monitor():
    """
    通过多线程循环执行，循环周期由配置文件决定
    1.遍历所有的容器（包括已经停止的），根据容器名（以<username>_<training>的格式作为开头）查询其对应的training在redis中的记录。
    若redis中不存在该training对应的记录，则将该容器移除
    2.遍历所有正在运行的training，若其对应的某个容器已经停止，则重启（先remove再start）该training
    """
    # 获取配置文件中的循环周期,单位：秒

    with open("config.json","r") as  f:
        res = json.load(f)
    MonitorTime = res['monitor_thread']['monitor_time']
    client = docker.from_env()
    while 1:
        # 遍历所有容器
        ContainersList = client.containers.list(all=1)
        for Container in ContainersList:
            container = client.containers.get(Container.id)
            ContainerName = container.attrs['Name']
            ContainerNameList = re.split(r'-',ContainerName)
            print(ContainerNameList)
        # print(type(ContainersList))
        # print(ContainersList)
        time.sleep(MonitorTime)

if __name__ == "__main__":
    # 通过多线程执行training_monitor
    t1 = threading.Thread(target=training_monitor)
    t1.start()
    apis.app.run("0.0.0.0")

