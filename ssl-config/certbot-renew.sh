#!/bin/bash

# SSL Certificate Renewal Script for Docker Nginx
# This script will renew Let's Encrypt certificates and reload nginx

LOG_FILE="/var/log/certbot-renew.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Starting certificate renewal check..." >> $LOG_FILE

# Stop nginx container to allow certbot standalone mode
docker stop confd-nginx-proxy-1 >> $LOG_FILE 2>&1

# Renew certificates
certbot renew --standalone --quiet >> $LOG_FILE 2>&1
RENEWAL_EXIT_CODE=$?

# Start nginx container back up
docker start confd-nginx-proxy-1 >> $LOG_FILE 2>&1

if [ $RENEWAL_EXIT_CODE -eq 0 ]; then
    echo "[$DATE] Certificate renewal completed successfully" >> $LOG_FILE
else
    echo "[$DATE] Certificate renewal failed with exit code $RENEWAL_EXIT_CODE" >> $LOG_FILE
fi

echo "[$DATE] Renewal process finished" >> $LOG_FILE
