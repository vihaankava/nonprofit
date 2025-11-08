#!/bin/bash
# Diagnostic script for AWS deployment issues

echo "========================================"
echo "Nonprofit Idea Coach - Diagnostics"
echo "========================================"
echo ""

# Check if running on EC2
if [ ! -f /home/ubuntu/nonprofit/nonprofit_coach/app.py ]; then
    echo "ERROR: This script must be run on the EC2 instance"
    echo "SSH into your server first:"
    echo "  ssh -i nonprofit-coach-key.pem ubuntu@YOUR_IP"
    exit 1
fi

echo "1. Checking application service status..."
sudo systemctl status nonprofit-coach --no-pager
echo ""

echo "2. Checking if application is running..."
ps aux | grep gunicorn | grep -v grep
echo ""

echo "3. Checking if port 5001 is listening..."
sudo lsof -i :5001
echo ""

echo "4. Checking Nginx status..."
sudo systemctl status nginx --no-pager
echo ""

echo "5. Checking if port 80 is listening..."
sudo lsof -i :80
echo ""

echo "6. Testing local connection to app..."
curl -I http://localhost:5001 2>&1 | head -5
echo ""

echo "7. Testing Nginx proxy..."
curl -I http://localhost:80 2>&1 | head -5
echo ""

echo "8. Checking recent application logs..."
echo "Last 20 lines:"
sudo journalctl -u nonprofit-coach -n 20 --no-pager
echo ""

echo "9. Checking Nginx error logs..."
echo "Last 10 lines:"
sudo tail -10 /var/log/nginx/error.log
echo ""

echo "10. Checking .env file..."
if [ -f /home/ubuntu/nonprofit/nonprofit_coach/.env ]; then
    echo "✓ .env file exists"
    if grep -q "ANTHROPIC_API_KEY=sk-ant-" /home/ubuntu/nonprofit/nonprofit_coach/.env; then
        echo "✓ API key appears to be set"
    else
        echo "⚠ API key may not be set correctly"
    fi
else
    echo "✗ .env file not found!"
fi
echo ""

echo "11. Checking security group (from instance metadata)..."
INSTANCE_ID=$(ec2-metadata --instance-id | cut -d " " -f 2)
echo "Instance ID: $INSTANCE_ID"
echo ""

echo "12. Checking public IP..."
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "Public IP: $PUBLIC_IP"
echo "Try accessing: http://$PUBLIC_IP"
echo ""

echo "========================================"
echo "Quick Fixes"
echo "========================================"
echo ""
echo "If application is not running:"
echo "  sudo systemctl start nonprofit-coach"
echo ""
echo "If Nginx is not running:"
echo "  sudo systemctl start nginx"
echo ""
echo "To restart everything:"
echo "  sudo systemctl restart nonprofit-coach"
echo "  sudo systemctl restart nginx"
echo ""
echo "To view live logs:"
echo "  sudo journalctl -u nonprofit-coach -f"
echo ""
