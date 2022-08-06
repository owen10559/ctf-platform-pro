import config
import redis

redis_conn_pool = redis.ConnectionPool(host=config.config["services"]["redis"]["host"], port=config.config["services"]["redis"]["port"], decode_responses=True)

if __name__ == '__main__':
    redis_conn = redis.Redis(connection_pool=redis_conn_pool)
    redis_conn.set("test_key", "test_value")
    print(redis_conn.get("test_key"))
