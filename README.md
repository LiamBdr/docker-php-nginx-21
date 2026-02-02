```bash
cp .env.example .env  # renseigner HF_TOKEN
docker compose build
docker compose run --rm llm python chat.py
```
