# worker.py
import os
import redis
from rq import Worker, Queue, Connection
from dotenv import load_dotenv
load_dotenv()


# Create Redis connection
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

# Set up a queue
listen = ['default']

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
