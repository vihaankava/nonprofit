# AWS Deployment Guide - Nonprofit Idea Coach

Complete guide to deploy your Flask application to AWS EC2 with public web access.

## Quick Deploy (One Command)

```bash
cd aws
./deploy.sh
```

This will:
- ✅ Create a t3.small EC2 instance (2 vCPU, 2GB RAM, 20GB storage)
- ✅ Set up security groups for HTTP/HTTPS/SSH access
- ✅ Install all dependencies
- ✅ Deploy your application with Gunicorn
- ✅ Configure Nginx as reverse proxy
- ✅ Set up auto-start on boot
- ✅ Make it publicly accessible

**Estimated time:** 5-10 minutes  
**Estimated cost:** ~$15-20/month

---

## What Gets Created

### EC2 Instance
- **Type:** t3.small
- **vCPUs:** 2
- **RAM:** 2 GB
- **Storage:** 20 GB SSD (gp3)
- **OS:** Ubuntu 22.04 LTS
- **Region:** us-east-1 (configurable)

### Security Group
- **Port 22:** SSH access (for management)
- **Port 80:** HTTP access (public web)
- **Port 443:** HTTPS access (for SSL)

### Software Stack
- **Web Server:** Nginx (reverse proxy)
- **App Server:** Gunicorn (4 workers)
- **Python:** 3.10+
- **Database:** SQLite (included)
- **Auto-start:** Systemd service

---

## Prerequisites

1. **AWS Account** with billing enabled
2. **AWS CLI** installed and configured
3. **Git** installed
4. **SSH client** (built into macOS/Linux)

### Verify AWS CLI

```bash
aws --version
aws configure list
```

You should see your credentials configured.

---

## Step-by-Step Deployment

### Step 1: Run the Deployment Script

```bash
cd aws
./deploy.sh
```

The script will:
1. Create SSH key pair (saved as `nonprofit-coach-key.pem`)
2. Create security group with web access rules
3. Launch EC2 instance
4. Wait for instance to be ready
5. Deploy application automatically
6. Configure Nginx and Gunicorn
7. Start services

### Step 2: Configure API Keys

After deployment completes, you'll see the public IP. SSH into your server:

```bash
ssh -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP
```

Edit the configuration:

```bash
cd /home/ubuntu/nonprofit/nonprofit_coach
nano .env
```

Add your API keys:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
SECRET_KEY=your-random-secret-key
BRAVE_API_KEY=your-brave-key-here  # Optional
```

Save and exit (`Ctrl+X`, `Y`, `Enter`)

### Step 3: Restart the Application

```bash
sudo systemctl restart nonprofit-coach
```

### Step 4: Access Your Application

Open your browser to:
```
http://YOUR_PUBLIC_IP
```

You should see your Nonprofit Idea Coach application!

---

## Managing Your Deployment

### View Application Logs

```bash
# Real-time logs
sudo journalctl -u nonprofit-coach -f

# Last 100 lines
sudo journalctl -u nonprofit-coach -n 100
```

### Restart Application

```bash
sudo systemctl restart nonprofit-coach
```

### Stop Application

```bash
sudo systemctl stop nonprofit-coach
```

### Start Application

```bash
sudo systemctl start nonprofit-coach
```

### Check Status

```bash
sudo systemctl status nonprofit-coach
```

### View Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

---

## Updating Your Application

### Method 1: Git Pull (Recommended)

```bash
# SSH into server
ssh -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP

# Navigate to app directory
cd /home/ubuntu/nonprofit/nonprofit_coach

# Pull latest changes
git pull

# Activate venv and update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart application
sudo systemctl restart nonprofit-coach
```

### Method 2: Manual File Upload

```bash
# From your local machine
scp -i nonprofit-coach-key.pem -r nonprofit_coach/* ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/nonprofit/nonprofit_coach/

# Then SSH and restart
ssh -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP
sudo systemctl restart nonprofit-coach
```

---

## Adding SSL/HTTPS (Optional but Recommended)

### Using Let's Encrypt (Free)

```bash
# SSH into server
ssh -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP

# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is set up automatically
```

### Using a Custom Domain

1. **Buy a domain** (from Namecheap, GoDaddy, etc.)
2. **Point DNS to your EC2 IP:**
   - Create an A record pointing to your public IP
3. **Update Nginx config:**
   ```bash
   sudo nano /etc/nginx/sites-available/nonprofit-coach
   ```
   Change `server_name _;` to `server_name yourdomain.com;`
4. **Restart Nginx:**
   ```bash
   sudo systemctl restart nginx
   ```
5. **Add SSL** (see above)

---

## Backup and Restore

### Backup Database

```bash
# From your local machine
scp -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/nonprofit/nonprofit_coach/nonprofit.db ./backup-$(date +%Y%m%d).db
```

### Restore Database

```bash
# Upload backup
scp -i nonprofit-coach-key.pem ./backup-20240108.db ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/nonprofit/nonprofit_coach/nonprofit.db

# Restart application
ssh -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP "sudo systemctl restart nonprofit-coach"
```

### Backup Generated Sites

```bash
scp -i nonprofit-coach-key.pem -r ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/nonprofit/nonprofit_coach/generated_sites ./backup-sites/
```

---

## Monitoring and Performance

### Check Resource Usage

```bash
# CPU and memory
htop

# Disk usage
df -h

# Application memory
ps aux | grep gunicorn
```

### Performance Tuning

Edit Gunicorn workers in systemd service:

```bash
sudo nano /etc/systemd/system/nonprofit-coach.service
```

Change `-w 4` to `-w 2` (for less memory) or `-w 8` (for more performance)

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl restart nonprofit-coach
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u nonprofit-coach -n 50

# Check if port is in use
sudo lsof -i :5001

# Verify Python environment
cd /home/ubuntu/nonprofit/nonprofit_coach
source venv/bin/activate
python app.py  # Test manually
```

### Can't Access from Browser

```bash
# Check if Nginx is running
sudo systemctl status nginx

# Check if application is running
sudo systemctl status nonprofit-coach

# Verify security group allows port 80
aws ec2 describe-security-groups --group-ids YOUR_SG_ID
```

### Out of Memory

```bash
# Check memory usage
free -h

# If needed, add swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Disk Full

```bash
# Check disk usage
df -h

# Clean up
sudo apt autoremove
sudo apt clean
sudo journalctl --vacuum-time=7d

# Check large files
du -sh /home/ubuntu/nonprofit/nonprofit_coach/*
```

---

## Cost Management

### Current Setup Cost (Approximate)

- **EC2 t3.small:** ~$15/month
- **20GB EBS storage:** ~$2/month
- **Data transfer:** ~$1-5/month (depends on traffic)
- **Total:** ~$18-22/month

### Cost Optimization

1. **Use Reserved Instances** (save 30-40% for 1-year commitment)
2. **Stop instance when not in use:**
   ```bash
   aws ec2 stop-instances --instance-ids YOUR_INSTANCE_ID
   ```
3. **Use AWS Free Tier** (t2.micro for 12 months if eligible)
4. **Set up billing alerts** in AWS Console

---

## Scaling Up

### Upgrade Instance Type

```bash
# Stop instance
aws ec2 stop-instances --instance-ids YOUR_INSTANCE_ID
aws ec2 wait instance-stopped --instance-ids YOUR_INSTANCE_ID

# Change instance type
aws ec2 modify-instance-attribute \
    --instance-id YOUR_INSTANCE_ID \
    --instance-type "{\"Value\": \"t3.medium\"}"

# Start instance
aws ec2 start-instances --instance-ids YOUR_INSTANCE_ID
```

### Add Load Balancer (For High Traffic)

See AWS documentation for setting up Application Load Balancer.

---

## Security Best Practices

### 1. Restrict SSH Access

Edit security group to allow SSH only from your IP:

```bash
aws ec2 revoke-security-group-ingress \
    --group-id YOUR_SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id YOUR_SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr YOUR_IP/32
```

### 2. Enable Automatic Updates

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Set Up Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 4. Regular Backups

Set up a cron job for automatic backups:

```bash
crontab -e
```

Add:
```
0 2 * * * cp /home/ubuntu/nonprofit/nonprofit_coach/nonprofit.db /home/ubuntu/backups/nonprofit-$(date +\%Y\%m\%d).db
```

---

## Cleanup / Uninstall

### Terminate Instance

```bash
aws ec2 terminate-instances --instance-ids YOUR_INSTANCE_ID
```

### Delete Security Group

```bash
aws ec2 delete-security-group --group-id YOUR_SG_ID
```

### Delete Key Pair

```bash
aws ec2 delete-key-pair --key-name nonprofit-coach-key
rm nonprofit-coach-key.pem
```

---

## Support

- **AWS Documentation:** https://docs.aws.amazon.com/
- **Application Issues:** https://github.com/vihaankava/nonprofit/issues
- **AWS Support:** Available in AWS Console

---

## Quick Reference Commands

```bash
# Deploy
./deploy.sh

# SSH into server
ssh -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP

# View logs
sudo journalctl -u nonprofit-coach -f

# Restart app
sudo systemctl restart nonprofit-coach

# Update app
cd /home/ubuntu/nonprofit/nonprofit_coach && git pull && sudo systemctl restart nonprofit-coach

# Backup database
scp -i nonprofit-coach-key.pem ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/nonprofit/nonprofit_coach/nonprofit.db ./backup.db
```

---

**Your application is now live on AWS!** 🚀
