import logging
from langchain_openai import ChatOpenAI
from slack_sdk import WebClient
from slack_rag_bot.config import Config

class ResponseGenerator:
    """
    A class to handle response generation using ChatOpenAI and sending messages to Slack.
    """

    def __init__(self):
        self.slack_client = WebClient(Config.token)
        self.llm = ChatOpenAI(model="gpt-4o-mini")  # Initialize the OpenAI model

    def generate_response(self, event):
        """
        Generate a response using OpenAI and send it to Slack.
        """
        try:
            logging.info(f"Received event: {event}")
            
            # Extract relevant data
            channel_id = event["channel"]
            thread_ts = event["ts"]
            user_message = event["text"]

            # Prepare the message for the LLM
            messages = [
                ("system", "You are a helpful assistant."),
                ("human", user_message),
            ]
            
            # Get AI-generated message
            ai_response = self.llm.invoke(messages)

            # Send the generated message back to Slack
            self.slack_client.chat_postMessage(
                channel=channel_id,
                text=ai_response.content,
                thread_ts=thread_ts
            )
            logging.info("Message successfully sent to Slack.")
        except Exception as e:
            logging.error(f"Error in generate_response: {e}")
