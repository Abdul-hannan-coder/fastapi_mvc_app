# Quick Setup Guide - FastAPI App with SSL

## 🚀 Quick Deploy Steps

### 1. Prerequisites
```bash
# Install Docker and Docker Compose
sudo apt update
sudo apt install docker.io docker-compose-v2 certbot -y
sudo usermod -aG docker $USER
```

### 2. Copy Project
```bash
# Copy the entire project folder to your server
scp -r my-projects/ user@yourserver:/home/user/
```

### 3. Get SSL Certificate
```bash
# Update domain name in nginx config first
sed -i 's/abdulhannan.duckdns.org/YOUR_DOMAIN_HERE/g' nginx/conf.d/default.conf

# Stop any running containers
cd fastapi_mvc_app
docker-compose down

# Get SSL certificate
sudo certbot certonly --standalone -d YOUR_DOMAIN_HERE
```

### 4. Setup Auto-Renewal
```bash
# Copy renewal script
sudo cp ssl-config/certbot-renew.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/certbot-renew.sh

# Update domain in renewal script
sudo sed -i 's/confd-nginx-proxy-1/YOUR_CONTAINER_NAME/g' /usr/local/bin/certbot-renew.sh

# Add to crontab
echo "0 2,14 * * * /usr/local/bin/certbot-renew.sh" | sudo crontab -
```

### 5. Start Application
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### 6. Verify Setup
```bash
# Test HTTP redirect
curl -I http://YOUR_DOMAIN_HERE

# Test HTTPS
curl -I https://YOUR_DOMAIN_HERE

# Should redirect to /contacts/
```

## 📁 Important Files

- **nginx/conf.d/default.conf**: Nginx configuration with SSL and redirects
- **fastapi_mvc_app/docker-compose.yaml**: Updated with SSL certificate mounts
- **ssl-config/certbot-renew.sh**: Automatic SSL renewal script
- **.env**: Environment variables (update as needed)

## 🔧 Customization

### Change Domain
Replace `abdulhannan.duckdns.org` with your domain in:
1. `nginx/conf.d/default.conf`
2. `ssl-config/certbot-renew.sh`
3. Run certbot with your domain

### Change Root Redirect
Edit `nginx/conf.d/default.conf`, find:
```nginx
location = / {
    return 301 https://$server_name/contacts/;
}
```
Change `/contacts/` to your preferred path.

## ✅ Features Included

- ✅ HTTP to HTTPS redirect
- ✅ Root path redirect to /contacts/
- ✅ SSL/TLS with modern security
- ✅ Security headers (HSTS, XSS protection, etc.)
- ✅ Automatic certificate renewal
- ✅ Docker containerized setup
- ✅ MongoDB database
- ✅ FastAPI application

Created: $(date)
Current Setup: abdulhannan.duckdns.org → /contacts/
