```bash
docker compose build
docker compose run --rm llm python chat.py
```

## Utiliser un modèle local (déjà téléchargé)

1. Place ton modèle dans le dossier `./models/` :
   ```
   models/
   └── mon-modele/
       ├── config.json
       ├── tokenizer.json
       ├── model.safetensors (ou pytorch_model.bin)
       └── ...
   ```

2. Lance avec le chemin local :
   ```bash
   docker compose run --rm llm python chat.py ./models/mon-modele
   ```
