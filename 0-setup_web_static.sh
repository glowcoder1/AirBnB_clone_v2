#!/usr/bin/env bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/{releases/test,shared}
sudo chown -R ubuntu:ubuntu /data/

# Create a fake HTML file for testing
echo "<html><head><title>Test Page</title></head><body>Hello, this is a test page!</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Update Nginx configuration
sudo sed -i '/hbnb_static/ { n; s|^.*$|        alias /data/web_static/current/;| }' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0

