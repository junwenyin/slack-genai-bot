# worker.py
import os
import redis
from rq import Worker, Queue, Connection
from slack_rag_bot.config import Config

# Create Redis connection
conn = redis.from_url(Config.redis_url)

# Set up a queue
listen = ['default']

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
