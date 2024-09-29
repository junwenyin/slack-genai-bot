import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    token = os.environ["SLACK_BOT_TOKEN"]