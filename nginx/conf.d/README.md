# FastAPI Contact App with SSL Setup

This directory contains a backup of your FastAPI contact application with complete SSL/HTTPS configuration.

## Directory Structure

```
my-projects/
├── fastapi_mvc_app/           # Your FastAPI application
│   ├── docker-compose.yaml   # Updated with SSL certificate mounts
│   ├── Dockerfile            # Application Docker configuration
│   ├── app/                  # Your application code
│   └── ...                   # Other project files
├── nginx/                    # Nginx configuration files
│   └── conf.d/
│       └── default.conf      # SSL-enabled nginx config with redirects
├── ssl-config/               # SSL related scripts
│   └── certbot-renew.sh      # Automatic certificate renewal script
└── README.md                 # This file
```

## SSL Configuration Features

### 🔐 Security Features
- **SSL/TLS**: TLS 1.2 and 1.3 support
- **HSTS**: HTTP Strict Transport Security enabled
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- **Auto-Renewal**: Automatic certificate renewal every 60-90 days

### 🔄 Redirect Configuration
- **HTTP → HTTPS**: All HTTP traffic redirects to HTTPS
- **Root → Contacts**: Root domain (`/`) redirects to `/contacts/`

## How to Use This Backup

### 1. Deploy to New Server
```bash
# Copy this folder to your new server
scp -r my-projects/ user@newserver:/home/user/

# Navigate to project directory
cd /home/user/my-projects/fastapi_mvc_app

# Update docker-compose.yaml paths if needed
# Start the application
docker-compose up -d
```

### 2. SSL Certificate Setup on New Server
```bash
# Install certbot
sudo apt update && sudo apt install certbot

# Stop nginx container temporarily
docker stop confd-nginx-proxy-1

# Get SSL certificate (replace with your domain)
sudo certbot certonly --standalone -d yourdomain.com

# Copy renewal script
sudo cp ssl-config/certbot-renew.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/certbot-renew.sh

# Add to cron for automatic renewal
echo "0 2,14 * * * /usr/local/bin/certbot-renew.sh" | sudo tee -a /var/spool/cron/crontabs/root
sudo service cron reload

# Start containers
docker start confd-nginx-proxy-1
```

### 3. Nginx Configuration
The nginx configuration includes:
- SSL termination
- HTTP to HTTPS redirect
- Root path redirect to `/contacts/`
- Security headers
- Reverse proxy to FastAPI app on port 8000

## Current Domain Setup
- **Domain**: abdulhannan.duckdns.org
- **SSL Certificate**: Let's Encrypt (Auto-renewing)
- **Application**: FastAPI Contact Manager
- **Database**: MongoDB

## Important Files
- `nginx/conf.d/default.conf`: Main nginx configuration
- `ssl-config/certbot-renew.sh`: SSL renewal script
- `fastapi_mvc_app/docker-compose.yaml`: Updated with SSL mounts

Created: August 13, 2025
