import re
import time
import threading
import docker

import apis
import config
import containers
import db

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
    MonitorTime = config.config['trainings']['detection_period']
    client = containers.client
    r = db.get_redis_conn()
    while 1:
        print("training_monitor start", flush=True)
        for container in client.containers.list(all=1):

            # BUG
            # 得到的 username 开头会多出一个 "/"
            ContainerNameList = re.split(r'_',container.attrs["Name"])
            if len(ContainerNameList) < 2:
                continue
            username = ContainerNameList[0]
            training_name = ContainerNameList[1]

            # print(ContainerNameList, flush=True)

            _, status = apis.get_training_info(username, training_name)
            if status == 404:
                # training 已到期
                print("clear", username, training_name)
                apis.remove_training(username, training_name)
            else:
                # training 未到期
                if container.attrs["State"]["Status"] == "exited":
                    print("restart", username, training_name)
                    apis.remove_training(ContainerNameList[0],ContainerNameList[1])
                    apis.create_training(ContainerNameList[0],ContainerNameList[1])
        time.sleep(MonitorTime)


        # 遍历所有容器
        # ContainersList = client.containers.list(all=1)
        # for Container in ContainersList:
        #     # container = client.containers.get(Container.id)

        #     ContainerName = Container.attrs['Name']
        #     ContainerNameList = re.split(r'_',ContainerName)
        #     if len(ContainerNameList) < 2:
        #         continue
        #     if r.exists(ContainerNameList[0]) == 0:
        #         print("removing your Container")
        #         apis.remove_training(ContainerNameList[0],ContainerNameList[1])

            # print(ContainerNameList)

        # ContainersList = client.containers.list()
        # for Container in ContainersList:
        #     container = client.containers.get(Container.id)
        #     ContainerName = container.attrs['Name']
        #     ContainerNameList = re.split(r'_',ContainerName)
        #     if len(ContainerNameList) < 2:
        #         continue
        #     if r.exists(ContainerNameList[0]) == 0:
        #         print("restarting your Container")
        #         apis.remove_training(ContainerNameList[0],ContainerNameList[1])
        #         apis.create_training(ContainerNameList[0],ContainerNameList[1])

        # print(type(ContainersList))
        # print(ContainersList)

if __name__ == "__main__":
    # 通过多线程执行training_monitor
    # threading.Thread(target=training_monitor).start()
    apis.app.run("0.0.0.0")

