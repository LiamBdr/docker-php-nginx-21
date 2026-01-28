#!/bin/sh
set -e

CERT_DIR="/etc/apache2/ssl"
CERT_FILE="$CERT_DIR/server.crt"
KEY_FILE="$CERT_DIR/server.key"

# Générer un certificat auto-signé si absent
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "Generating self-signed SSL certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$KEY_FILE" \
        -out "$CERT_FILE" \
        -subj "/CN=localhost" \
        -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
fi

# Lancer php-fpm en arrière-plan
php-fpm -D

# Lancer Apache en avant-plan
exec httpd -D FOREGROUND
