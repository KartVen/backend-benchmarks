FROM php:8.3-fpm

RUN apt-get update -y && apt-get install -y \
    nginx \
    openssl \
    zip \
    unzip \
    git \
    curl \
    libpq-dev \
    libzip-dev && \
    docker-php-ext-install pdo pdo_pgsql zip

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www/html
COPY . .

COPY www.conf /usr/local/etc/php-fpm.d/www.conf

RUN composer install --no-dev --optimize-autoloader

RUN php artisan config:cache && php artisan route:cache

RUN echo "expose_php = Off" >> /usr/local/etc/php/php.ini

COPY default.conf /etc/nginx/conf.d/default.conf

CMD ["sh", "-c", "php-fpm & nginx -g 'daemon off;'"]
