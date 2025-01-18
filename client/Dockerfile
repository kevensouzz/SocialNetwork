FROM php:8.2.12-apache

RUN apt-get update && apt-get install -y \
    zip \
    unzip \
    && docker-php-ext-install pdo_mysql

COPY ./ /var/www/html

RUN chown -R www-data:www-data /var/www/html

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www/html

RUN composer install

RUN sed -i 's|/var/www/html|/var/www/html/src/pages|g' /etc/apache2/sites-available/000-default.conf

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

RUN a2enmod rewrite