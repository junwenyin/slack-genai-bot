# uvicorn slack_rag_bot.main:api --reload --port 3000 
# poetry run python -m slack_rag_bot.worker
# poetry run python -m slack_rag_bot.main
# ngrok http http://localhost:3000

git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:junwenyin/slack-genai-bot.git
git push -u origin main