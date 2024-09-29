# uvicorn slack_rag_bot.main:api --reload --port 3000 
# poetry run python -m slack_rag_bot.worker

# SOCKET MODE
# poetry run python -m slack_rag_bot.socket

# API MODE
# poetry run python -m slack_rag_bot.main
# ngrok http http://localhost:3000

docker run --name redis-server -d -p 6379:6379 redis
