import config
import redis
import time

# 等待 redis 容器初始化完成
time.sleep(5)

redis_conn_pool = redis.ConnectionPool(host=config.config["services"]["redis"]["host"], port=config.config["services"]["redis"]["port"], decode_responses=True)
redis_conn = redis.Redis(connection_pool=redis_conn_pool)

def get_redis_conn():
    return redis.Redis(connection_pool=redis_conn_pool)

if __name__ == '__main__':
    redis_conn = redis.Redis(connection_pool=redis_conn_pool)
    redis_conn.set("test_key", "test_value")
    print(redis_conn.get("test_key"))
