import re
import time
import threading
import docker

import apis
import config
import containers

def training_monitor():
    """
    通过多线程循环执行，循环周期由配置文件决定
    遍历所有容器（包括已经停止的），进行以下操作：
    1. 根据容器名（以<username>_<training_name>的格式作为开头）, 获取training_id
    获取方法：名为 <username>_<training_name>_main_1 的容器的id即为对应的training_id
    2. 根据training_id查询其对应的training在redis中的记录。
    3. 若redis中不存在该training对应的记录，则将该容器移除
    4. 若redis中存在该training对应的记录，但该容器已停止，则重启（先remove再start）整个training
    重启training可以尝试执行以下代码：
    apis.remove_training(username, training_name)
    apis.create_training(username, training_name)
    """

    monitorTime = config.config['trainings']['detection_period']
    client = containers.client
    while 1:
        # 遍历所有容器
        containersList = client.containers.list(all=1)
        for Container in containersList:
            container = client.containers.get(Container.id)
            containerName = container.attrs['Name']
            if 'main_1' not in containerName:
                continue
            containerNameList = re.split(r'_', containerName)
            if len(containerNameList) < 2:
                continue
            if '/' in containerNameList[0]:
                containerNameList[0] = containerNameList[0].lstrip('/')
            if r.exists(containerNameList[0]) == 0:
                apis.remove_training(containerNameList[0], containerNameList[1])
        containersList = client.containers.list()
        for Container in containersList:
            container = client.containers.get(Container.id)
            containerName = container.attrs['Name']
            if 'main_1' not in containerName:
                continue
            containerNameList = re.split(r'_', containerName)
            if len(containerNameList) < 2:
                continue
            if '/' in containerNameList[0]:
                containerNameList[0] = containerNameList[0].lstrip('/')
            if r.exists(containerNameList[0]) == 0:
                apis.remove_training(containerNameList[0], containerNameList[1])
                apis.create_training(containerNameList[0], containerNameList[1])
        time.sleep(monitorTime)

if __name__ == "__main__":
    # 通过多线程执行training_monitor
    t1 = threading.Thread(target=training_monitor)
    t1.start()
    apis.app.run("0.0.0.0")

