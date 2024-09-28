import logging
from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from fastapi import FastAPI, Request
from redis import Redis
from rq import Queue
from langchain_openai import ChatOpenAI
import uvicorn
import os

from slack_rag_bot.config import Config
from slack_rag_bot.response_generator import ResponseGenerator

# Load environment variables and configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Slack app and RQ (Redis Queue) setup
app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)
response_generator = ResponseGenerator(app)

redis_conn = Redis.from_url(Config.redis_url)  # Create Redis connection from URL
queue = Queue(connection=redis_conn)

# FastAPI app
api = FastAPI()

async def generate_response(body):
    await response_generator.generate_response(body)

# Event handler for Slack app mentions
@app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    try:
        logging.info("Enqueuing task to process app_mention event.")
        queue.enqueue(generate_response, body)  # Enqueue background task
    except Exception as e:
        logging.error(f"Error in handle_app_mentions: {e}")

# Event handler for general Slack messages
@app.event("message")
async def handle_message(body):
    logging.info("handle_message event triggered, but no action taken.")

# FastAPI route to handle Slack events
@api.post("/slack/events")
async def slack_events_endpoint(req: Request):
    return await app_handler.handle(req)

# Main entry point for running the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run("slack_rag_bot.main:api", host="0.0.0.0", port=3000, reload=True)
