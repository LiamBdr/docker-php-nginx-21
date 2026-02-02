FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu \
    mistral_inference \
    mistral_common \
    huggingface_hub

CMD ["bash"]
