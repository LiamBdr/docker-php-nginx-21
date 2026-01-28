FROM php:8.4-fpm-alpine

# Installation des dépendances système, Apache et extensions PHP
RUN apk add --no-cache \
        apache2 \
        apache2-ssl \
        apache2-proxy \
        openssl \
        icu-dev \
        libzip-dev \
        linux-headers \
        oniguruma-dev \
        curl \
        git \
        unzip \
    && docker-php-ext-configure intl \
    && docker-php-ext-install -j$(nproc) \
        intl \
        opcache \
        pdo \
        pdo_mysql \
        zip \
        mbstring \
    && rm -rf /var/cache/apk/* /tmp/*

# Installation de Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Configuration PHP pour le développement
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

# Création d'un utilisateur non-root
RUN addgroup -g 1000 symfony \
    && adduser -u 1000 -G symfony -s /bin/sh -D symfony

# Répertoire de travail
WORKDIR /var/www/html

# Permissions sur le cache et les logs Symfony
RUN mkdir -p var/cache var/log \
    && chown -R symfony:symfony var

# Répertoire pour les certificats SSL
RUN mkdir -p /etc/apache2/ssl

# Copier la configuration Apache et l'entrypoint
COPY docker/apache/symfony.conf /etc/apache2/conf.d/symfony.conf
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Désactiver le virtualhost par défaut d'Alpine Apache
RUN sed -i 's|^Include /etc/apache2/conf.d/|#Include /etc/apache2/conf.d/|' /etc/apache2/httpd.conf \
    && echo "Include /etc/apache2/conf.d/symfony.conf" >> /etc/apache2/httpd.conf

# Charger les modules nécessaires
RUN sed -i \
    -e 's/^#LoadModule rewrite_module/LoadModule rewrite_module/' \
    -e 's/^#LoadModule ssl_module/LoadModule ssl_module/' \
    -e 's/^#LoadModule socache_shmcb_module/LoadModule socache_shmcb_module/' \
    /etc/apache2/httpd.conf

EXPOSE 80 443

ENTRYPOINT ["entrypoint.sh"]
