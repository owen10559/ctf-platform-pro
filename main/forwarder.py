import os
import re
import socket
import logging
import sys
import threading
import containers

REMOTE_FLAG = {}
POOL_SIZE = 10

# 缓冲区大小
BUFFER_SIZE = 1024 * 1024

# logger设置
logger = logging.getLogger("Forwarder Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
                              '%Y %b %d %a %H:%M:%S', )
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
if 'LOG_LEVEL' in os.environ:
    logger.setLevel(os.environ['LOG_LEVEL'])
else:
    logger.setLevel('DEBUG')


class RemotePool:
    def __init__(self):
        self.remote_pool = []

    def append_pool(self, remote_ip, remote_port):
        if len(self.remote_pool) >= POOL_SIZE:
            self.close_error_conn()
        remote_conn = socket.socket()
        try:
            remote_conn.connect((remote_ip, remote_port))
            self.remote_pool.append(remote_conn)
        except:
            logger.error('Unable to connect to the remote server on ' + remote_ip + ':' + str(remote_port))
            return

    def get_pool(self, remote_ip, remote_port):
        # 重试10次
        for i in range(10):
            for remote_conn in self.remote_pool:
                if remote_conn.getpeername() == (remote_ip, remote_port):
                    return remote_conn
            self.append_pool(remote_ip, remote_port)

    def close_error_conn(self):
        for remote_conn in self.remote_pool:
            if not REMOTE_FLAG[remote_conn]:
                remote_conn.close()
                self.remote_pool.remove(remote_conn)
                logger.debug(
                    'Close the error connection to the remote server on ' + remote_conn.getpeername()[0] + ':' + str(
                        remote_conn.getpeername()[1]))

    def close_pool(self):
        for remote_conn in self.remote_pool:
            remote_conn.close()


def forward_res(local_conn, remote_conn):
    while True:
        res = remote_conn.recv(BUFFER_SIZE)
        if res == b'':
            REMOTE_FLAG[remote_conn] = False
            logger.debug(f'Thread {threading.current_thread().name} closed')
            return
        local_conn.sendall(res)


def forward_manager(local_conn: socket.socket):
    """将单个用户的请求转发个多个服务器"""
    is_close = False
    remote_pool = RemotePool()
    remote_conn = None
    buffer = b''
    req = b''

    while True:
        # 接收请求头
        while True:
            data = local_conn.recv(BUFFER_SIZE)
            if data == b'':
                is_close = True
                break
            buffer += data
            header_end = buffer.find(b'\r\n\r\n')
            if header_end != -1:
                # 请求头接受完成
                break
        if is_close:
            break
        header_end += 4  # 加上\r\n\r\n的长度
        header = buffer[:header_end]
        if header.find(b'Transfer-Encoding: chunked') != -1:
            # transfer-encoding为chunked
            while True:
                data = local_conn.recv(BUFFER_SIZE)
                if data == b'':
                    is_close = True
                    break
                buffer += data
                chunked_end = buffer.find(b'\r\n0\r\n\r\n')
                if chunked_end != -1:
                    # 数据接受完成
                    req = buffer[:chunked_end + 7]  # 加上\r\n0\r\n\r\n的长度
                    buffer = buffer[chunked_end + 7:]
                    break
        else:
            match = re.search(r'Content-Length: (\d+)', header.decode())
            if match:
                content_length = int(match.group(1))
                while True:
                    if len(buffer) - header_end < content_length:
                        data = local_conn.recv(BUFFER_SIZE)
                        if data == b'':
                            is_close = True
                            break
                        buffer += data
                    else:
                        # 请求体接收完整
                        req = buffer[:header_end + content_length]
                        buffer = buffer[header_end + content_length:]
                        break
            else:
                # 没有Content-Length字段，则请求报文仅有请求头
                req = buffer[:header_end]
                buffer = buffer[header_end:]
        if is_close:
            break

        logger.debug(req)
        # TODO 从 req 的中获取training_id
        # training_id 在 req 的 uri 中，uri 的格式为 /entrances/<training_id>/...
        # 取出后把 uri 的前缀 /entrances/<training_id> 去掉，只保留 /... 的内容
        # 例如某个 uri 为 /entrances/abc123/index?q=1，则 training_id 为abc123，去掉前缀后的 uri 为 /index?q=1
        req_split = req.decode().split(' ')
        uri = req_split[1]
        if not uri.startswith('/entrances/'):
            break
        container_id = uri.split('/')[2]
        req_split[1] = '/' + ''.join(uri.split('/')[3:])
        req = ' '.join(req_split).encode()
        remote_ip = socket.gethostbyname('dind')
        remote_port = containers.get_export_port(containers.get_container(container_id=container_id))
        remote_conn = remote_pool.get_pool(remote_ip, int(remote_port))
        remote_conn.sendall(req)
        logger.info(f"Forward: {local_conn.getpeername()} -> {remote_conn.getpeername()} len: {len(req)}")

        for each in threading.enumerate():
            if remote_conn.getpeername()[0] + ':' + str(remote_conn.getpeername()[1]) == each.getName():
                break
        else:
            threading.Thread(target=forward_res, args=(local_conn, remote_conn),
                             name=remote_conn.getpeername()[0] + ':' + str(remote_conn.getpeername()[1])).start()

    logger.info(f"Close: {local_conn.getpeername()}")
    for each in threading.enumerate():
        if remote_conn and remote_conn.getpeername()[0] + ':' + str(remote_conn.getpeername()[1]) == each.getName():
            each.join()
            break
    remote_pool.close_pool()
    local_conn.close()


def run(host: str = "", port: int = 8888):
    local_server = socket.socket()
    local_server.bind((host, port))
    local_server.listen(1)
    while 1:
        local_conn, local_addr = local_server.accept()
        threading.Thread(target=forward_manager, args=(local_conn,)).start()


if __name__ == '__main__':
    run()
