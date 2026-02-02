#!/usr/bin/env python3
"""
Chat interactif avec Mistral en local via mistral_inference.

Télécharge le modèle depuis Hugging Face (via Artifactory si configuré)
puis lance une boucle de chat interactive.

Usage:
  docker compose run --rm llm python chat.py
"""

import os
from pathlib import Path

from huggingface_hub import snapshot_download
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
MODEL_DIR = Path("./models/Mistral-7B-Instruct-v0.3")


def download_model():
    """Télécharge le modèle si pas déjà présent."""
    if MODEL_DIR.exists() and any(MODEL_DIR.iterdir()):
        print(f"Modèle déjà présent dans {MODEL_DIR}")
        return

    token = os.environ.get("HF_TOKEN")
    endpoint = os.environ.get("HF_ENDPOINT")

    print(f"Téléchargement du modèle {MODEL_ID}...")
    if endpoint:
        print(f"  Endpoint: {endpoint}")

    snapshot_download(
        repo_id=MODEL_ID,
        local_dir=str(MODEL_DIR),
        token=token,
        endpoint=endpoint,
    )
    print("Téléchargement terminé.")


def main():
    download_model()

    print("Chargement du tokenizer...")
    tokenizer = MistralTokenizer.from_file(str(MODEL_DIR / "tokenizer.model.v3"))

    print("Chargement du modèle...")
    model = Transformer.from_folder(str(MODEL_DIR))

    print("Modèle chargé. Tape 'quit' pour quitter.\n")

    while True:
        try:
            user_input = input("Toi: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        if not user_input:
            continue

        request = ChatCompletionRequest(
            messages=[UserMessage(content=user_input)]
        )
        tokens = tokenizer.encode_chat_completion(request).tokens

        out_tokens, _ = generate(
            [tokens],
            model,
            max_tokens=256,
            temperature=0.7,
            eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id,
        )

        response = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
        print(f"Bot: {response}\n")


if __name__ == "__main__":
    main()
