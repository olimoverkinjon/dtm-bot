# DTM Bot - PHP Docker Image
FROM php:8.2-apache

# Install required extensions
RUN docker-php-ext-install curl

# Enable Apache modules
RUN a2enmod rewrite headers

# Set working directory
WORKDIR /var/www/html

# Copy files
COPY . /var/www/html/

# Set permissions
RUN chmod 644 *.php && chmod 666 leads.json sessions.json 2>/dev/null || true

# Configure Apache
RUN echo '<Directory /var/www/html>' > /etc/apache2/sites-available/000-default-new.conf && \
    echo '    Options Indexes FollowSymLinks' >> /etc/apache2/sites-available/000-default-new.conf && \
    echo '    AllowOverride All' >> /etc/apache2/sites-available/000-default-new.conf && \
    echo '    Require all granted' >> /etc/apache2/sites-available/000-default-new.conf && \
    echo '</Directory>' >> /etc/apache2/sites-available/000-default-new.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD php -r "file_get_contents('http://localhost/status.php');"

EXPOSE 80

CMD ["apache2-foreground"]
