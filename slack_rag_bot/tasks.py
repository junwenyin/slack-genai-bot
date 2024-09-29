import logging
from slack_rag_bot.response_generator import ResponseGenerator

response_generator = ResponseGenerator()

def generate_response(event):
    logging.info(f"generate_response: {event}")
    response_generator.generate_response(event)