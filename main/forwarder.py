import re
import socket
import logging
import sys
import threading

REMOTE_FLAG = {}
POOL_SIZE = 10

# 缓冲区大小
BUFFER_SIZE = 1024 * 1024

# logger设置
logger = logging.getLogger("Forwarder Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
                              '%Y %b %d %a %H:%M:%S', )
# 例: Forwarder Logging 2022 Aug 08 Mon 17:20:27 DEBUG    31   Connection closed.
stream_handler = logging.StreamHandler(sys.stderr)  # 错误输出到logger
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


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
            REMOTE_FLAG[remote_conn] = True
        except:
            logger.error('Unable to connect to the remote server on ' + remote_ip + ':' + str(remote_port))
            return

    def get_pool(self, remote_ip, remote_port):
        for remote_conn in self.remote_pool:
            if remote_conn.getpeername() == (remote_ip, remote_port):
                return remote_conn
        self.append_pool(remote_ip, remote_port)
        return self.get_pool(remote_ip, remote_port)

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
            return
        local_conn.sendall(res)


def forward_manager(local_conn: socket.socket):
    """将单个用户的请求转发个多个服务器"""
    remote_pool = RemotePool()
    buffer = b''
    req = b''
    while True:
        while True:
            buffer += local_conn.recv(BUFFER_SIZE)
            if buffer == b'':
                break
            header_end = buffer.find(b'\r\n\r\n')
            if header_end == -1:  # 没有找到头部结束位置
                continue
            header_end += 4  # 加上\r\n\r\n的长度
            header = buffer[:header_end]
            if header.find(b'Transfer-Encoding: chunked') != -1:  # transfer-encoding为chunked
                chunked_end = buffer.find(b'\r\n0\r\n\r\n')
                if chunked_end == -1:  # 没有找到 chunked 结束位置
                    continue
                req = buffer[:chunked_end + 7]  # 加上\r\n0\r\n\r\n的长度
                break
            match = re.search(r'Content-Length: (\d+)', header.decode())
            if match:
                content_length = int(match.group(1))
                if len(buffer) - header_end < content_length:  # 没接收完整
                    continue
                req = buffer[:header_end + content_length]
                break
            else:  # 没有Content-Length字段，则请求报文仅有请求头
                req = buffer[:header_end]
                break
        buffer = buffer.replace(req, b'')
        if req == b'':
            break
        logger.debug(req)
        # TODO 从 uri 中获得 remote_ip 和 remote_port
        # uri = req.decode().split(' ')[1]
        remote_ip = '34.227.213.82'
        remote_port = 80
        remote_conn = remote_pool.get_pool(remote_ip, remote_port)
        logger.info("Forward: %s -> %s" % (local_conn.getpeername(), remote_conn.getpeername()))
        remote_conn.sendall(req)
        for each in threading.enumerate():
            if remote_conn.getpeername()[0] + ':' + str(remote_conn.getpeername()[1]) == each.getName():
                break
        else:
            thread = threading.Thread(target=forward_res, args=(local_conn, remote_conn))
            thread.setName(remote_conn.getpeername()[0] + ':' + str(remote_conn.getpeername()[1]))
            thread.start()


def run(host: str = "", port: int = 8888):
    local_server = socket.socket()
    local_server.bind((host, port))
    local_server.listen(1)
    while 1:
        local_conn, local_addr = local_server.accept()
        threading.Thread(target=forward_manager, args=(local_conn,)).start()


if __name__ == '__main__':
    run()
