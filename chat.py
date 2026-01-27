#!/usr/bin/env python3
"""
Chat simple avec un LLM en local.

Usage:
  python chat.py ./models/mon-modele       # Utilise un modèle local
"""

import sys
from transformers import pipeline, Conversation

def main():
    # Modèle par défaut ou chemin passé en argument
    model_path = sys.argv[1] if len(sys.argv) > 1 else "facebook/blenderbot-400M-distill"
    
    print(f"Chargement du modèle: {model_path}")
    
    chatbot = pipeline(
        "conversational",
        model=model_path
    )
    
    print("✅ Modèle chargé ! Tape 'quit' pour quitter.\n")
    
    conversation = Conversation()
    
    while True:
        user_input = input("Toi: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Bye!")
            break
        
        if not user_input:
            continue
        
        conversation.add_user_input(user_input)
        conversation = chatbot(conversation)
        
        print(f"Bot: {conversation.generated_responses[-1]}\n")

if __name__ == "__main__":
    main()
