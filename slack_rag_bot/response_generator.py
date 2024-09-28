import logging
from langchain_openai import ChatOpenAI

class ResponseGenerator:
    """
    A class to handle response generation using ChatOpenAI and sending messages to Slack.
    """

    def __init__(self, app):
        self.app = app
        self.llm = ChatOpenAI(model="gpt-4o-mini")  # Initialize the OpenAI model

    async def generate_response(self, body):
        """
        Generate a response using OpenAI and send it to Slack.
        """
        try:
            logging.info(f"Received body: {body}")
            
            # Extract relevant data
            channel_id = body["event"]["channel"]
            thread_ts = body["event"]["event_ts"]
            user_message = body["event"]["text"]

            # Prepare the message for the LLM
            messages = [
                ("system", "You are a helpful assistant."),
                ("human", user_message),
            ]
            
            # Get AI-generated message
            ai_response = self.llm.invoke(messages)

            # Send the generated message back to Slack
            await self.app.client.chat_postMessage(
                channel=channel_id,
                text=ai_response.content,
                thread_ts=thread_ts
            )
            logging.info("Message successfully sent to Slack.")
        except Exception as e:
            logging.error(f"Error in generate_response: {e}")
