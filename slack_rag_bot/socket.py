import logging
import os
from typing import Optional
from redis import Redis
from rq import Queue
import asyncio

from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_rag_bot.config import Config
from slack_rag_bot.tasks import generate_response

logging.basicConfig(level=logging.DEBUG)

#
# Socket Mode Bolt app
#

# Install the Slack app and get xoxb- token in advance
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])
global socket_mode_client
socket_mode_client: Optional[SocketModeClient] = None

redis_conn = Redis.from_url(Config.redis_url)  # Create Redis connection from URL
queue = Queue(connection=redis_conn)


@app.event("app_mention")
async def handle_app_mentions(event, say):
    try:
        logging.info(f"handle_app_mentions: {event}")
        logging.info("Enqueuing task to process app_mention event.")
        #await generate_response(event)
        #await say("hello")
        queue.enqueue(generate_response, event)  # Enqueue background task
    except Exception as e:
        logging.error(f"Error in handle_app_mentions: {e}")


#
# Web app for hosting the healthcheck endpoint for k8s etc.
#

from aiohttp import web


async def healthcheck(_req: web.Request):
    if socket_mode_client is not None and socket_mode_client.is_connected():
        return web.Response(status=200, text="OK")
    return web.Response(status=503, text="The Socket Mode client is inactive")


web_app = app.web_app()
web_app.add_routes([web.get("/health", healthcheck)])


#
# Start the app
#

async def start_socket_mode(_web_app: web.Application):
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.connect_async()
    socket_mode_client = handler.client

async def shutdown_socket_mode(_web_app: web.Application):
    await socket_mode_client.close()

def run():
    web_app.on_startup.append(start_socket_mode)
    web_app.on_shutdown.append(shutdown_socket_mode)
    web.run_app(app=web_app, port=8080)
    
if __name__ == "__main__":
    run()