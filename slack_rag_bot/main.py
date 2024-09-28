import logging
from dotenv import load_dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk import WebClient
from fastapi import FastAPI, Request, BackgroundTasks
from redis import Redis
from rq import Queue

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)

async def generate_response(body):
    logging.info(body)
    logging.info("task run")
    channel_id = body["event"]["channel"]
    await app.client.chat_postMessage(
        channel=channel_id,
        text="Hello world!",
        thread_ts= body["event"]["event_ts"]
        # You could also use a blocks[] array to send richer content
    )


@app.event("app_mention")
async def handle_app_mentions(body, say, logger):
    logging.info("add_task")
    queue.enqueue(generate_response, body)
    # thread_ts= body["event"]["event_ts"]
    # await say("What's up?", thread_ts=thread_ts)


@app.event("message")
async def handle_message(body):
    logging.info("handle_message")
    pass

api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("slack_rag_bot.main:api", host="0.0.0.0", port=3000, reload=True)