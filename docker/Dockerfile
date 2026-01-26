# <url>/php:8.3-fpm-alpine
FROM php:8.3-fpm-alpine

# Installation des dépendances système et extensions PHP
RUN apk add --no-cache \
        icu-dev \
        libzip-dev \
        linux-headers \
        oniguruma-dev \
        curl \
        fcgi \
        git \
        unzip \
    # Installation des extensions PHP
    && docker-php-ext-configure intl \
    && docker-php-ext-install -j$(nproc) \
        intl \
        opcache \
        pdo \
        pdo_mysql \
        zip \
        mbstring \
    # Nettoyage pour réduire la taille de l'image
    && rm -rf /var/cache/apk/* /tmp/*

# Installation de Composer
# COPY --from=<url>/composer:2
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Script de healthcheck pour PHP-FPM
RUN set -xe \
    && curl -o /usr/local/bin/php-fpm-healthcheck \
       https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck \
    && chmod +x /usr/local/bin/php-fpm-healthcheck

# Configuration PHP-FPM : activer le status pour le healthcheck
RUN set -xe \
    && echo "pm.status_path = /status" >> /usr/local/etc/php-fpm.d/zz-docker.conf \
    && echo "ping.path = /ping" >> /usr/local/etc/php-fpm.d/zz-docker.conf \
    && echo "ping.response = pong" >> /usr/local/etc/php-fpm.d/zz-docker.conf

# Configuration PHP pour le développement
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

# Création d'un utilisateur non-root pour plus de sécurité
RUN addgroup -g 1000 symfony \
    && adduser -u 1000 -G symfony -s /bin/sh -D symfony

# Répertoire de travail
WORKDIR /var/www/html

# Permissions sur le cache et les logs Symfony
RUN mkdir -p var/cache var/log \
    && chown -R symfony:symfony var

# Port exposé par PHP-FPM
EXPOSE 9000

CMD ["php-fpm"]
