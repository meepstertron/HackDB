from rq import Worker, Queue
from redis import Redis

listen = ['default']
redis_url = "redis://hackdb-redis:6379/0"
conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    worker = Worker([Queue(name, connection=conn) for name in listen])
    worker.work()