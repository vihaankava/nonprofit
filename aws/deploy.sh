#!/bin/bash
# AWS EC2 Deployment Script for Nonprofit Idea Coach
# This script automates the deployment to AWS EC2

set -e

echo "========================================"
echo "Nonprofit Idea Coach - AWS Deployment"
echo "========================================"
echo ""

# Configuration
INSTANCE_TYPE="t3.small"  # 2 vCPU, 2GB RAM
REGION="us-east-1"
AMI_ID="ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS in us-east-1
KEY_NAME="nonprofit-coach-key"
SECURITY_GROUP_NAME="nonprofit-coach-sg"
INSTANCE_NAME="nonprofit-idea-coach"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "ERROR: AWS CLI not found. Please install it first."
    exit 1
fi

# Check if key pair exists
echo "Step 1: Checking SSH key pair..."
if ! aws ec2 describe-key-pairs --key-names "$KEY_NAME" --region "$REGION" &> /dev/null; then
    echo "Creating new key pair..."
    aws ec2 create-key-pair \
        --key-name "$KEY_NAME" \
        --region "$REGION" \
        --query 'KeyMaterial' \
        --output text > "${KEY_NAME}.pem"
    chmod 400 "${KEY_NAME}.pem"
    echo "✓ Key pair created and saved to ${KEY_NAME}.pem"
else
    echo "✓ Key pair already exists"
fi

# Create security group
echo ""
echo "Step 2: Setting up security group..."
SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$SECURITY_GROUP_NAME" \
    --region "$REGION" \
    --query 'SecurityGroups[0].GroupId' \
    --output text 2>/dev/null)

if [ "$SG_ID" == "None" ] || [ -z "$SG_ID" ]; then
    echo "Creating security group..."
    SG_ID=$(aws ec2 create-security-group \
        --group-name "$SECURITY_GROUP_NAME" \
        --description "Security group for Nonprofit Idea Coach" \
        --region "$REGION" \
        --query 'GroupId' \
        --output text)
    
    # Allow SSH (port 22)
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp \
        --port 22 \
        --cidr 0.0.0.0/0 \
        --region "$REGION"
    
    # Allow HTTP (port 80)
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp \
        --port 80 \
        --cidr 0.0.0.0/0 \
        --region "$REGION"
    
    # Allow HTTPS (port 443)
    aws ec2 authorize-security-group-ingress \
        --group-id "$SG_ID" \
        --protocol tcp \
        --port 443 \
        --cidr 0.0.0.0/0 \
        --region "$REGION"
    
    echo "✓ Security group created: $SG_ID"
else
    echo "✓ Security group already exists: $SG_ID"
fi

# Launch EC2 instance
echo ""
echo "Step 3: Launching EC2 instance ($INSTANCE_TYPE)..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name "$KEY_NAME" \
    --security-group-ids "$SG_ID" \
    --region "$REGION" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":20,"VolumeType":"gp3"}}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✓ Instance launched: $INSTANCE_ID"
echo "  Waiting for instance to be running..."

aws ec2 wait instance-running \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION"

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "✓ Instance is running!"
echo "  Public IP: $PUBLIC_IP"

# Wait for SSH to be ready
echo ""
echo "Step 4: Waiting for SSH to be ready..."
sleep 30

MAX_RETRIES=30
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if ssh -i "${KEY_NAME}.pem" -o StrictHostKeyChecking=no -o ConnectTimeout=5 ubuntu@$PUBLIC_IP "echo 'SSH ready'" &> /dev/null; then
        echo "✓ SSH is ready!"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "  Attempt $RETRY_COUNT/$MAX_RETRIES..."
    sleep 10
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "ERROR: Could not connect via SSH"
    exit 1
fi

# Deploy application
echo ""
echo "Step 5: Deploying application..."
echo "  Copying deployment script..."

# Create deployment script
cat > /tmp/setup-server.sh << 'DEPLOY_SCRIPT'
#!/bin/bash
set -e

echo "Installing system packages..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git

echo "Cloning application..."
cd /home/ubuntu
git clone https://github.com/vihaankava/nonprofit.git
cd nonprofit/nonprofit_coach

echo "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

echo "Creating .env file..."
cp .env.example .env

echo "Setting up systemd service..."
sudo tee /etc/systemd/system/nonprofit-coach.service > /dev/null << 'EOF'
[Unit]
Description=Nonprofit Idea Coach
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/nonprofit/nonprofit_coach
Environment="PATH=/home/ubuntu/nonprofit/nonprofit_coach/venv/bin"
ExecStart=/home/ubuntu/nonprofit/nonprofit_coach/venv/bin/gunicorn -w 4 -b 0.0.0.0:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/nonprofit-coach > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 10M;
}
EOF

sudo ln -sf /etc/nginx/sites-available/nonprofit-coach /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable nonprofit-coach
sudo systemctl start nonprofit-coach
sudo systemctl restart nginx

echo "Deployment complete!"
DEPLOY_SCRIPT

# Copy and execute deployment script
scp -i "${KEY_NAME}.pem" -o StrictHostKeyChecking=no /tmp/setup-server.sh ubuntu@$PUBLIC_IP:/tmp/
ssh -i "${KEY_NAME}.pem" -o StrictHostKeyChecking=no ubuntu@$PUBLIC_IP "chmod +x /tmp/setup-server.sh && /tmp/setup-server.sh"

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "Instance Details:"
echo "  Instance ID: $INSTANCE_ID"
echo "  Public IP: $PUBLIC_IP"
echo "  Instance Type: $INSTANCE_TYPE"
echo "  Region: $REGION"
echo ""
echo "Access your application:"
echo "  URL: http://$PUBLIC_IP"
echo ""
echo "SSH into your server:"
echo "  ssh -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP"
echo ""
echo "Configure your API keys:"
echo "  1. SSH into the server"
echo "  2. Edit: nano /home/ubuntu/nonprofit/nonprofit_coach/.env"
echo "  3. Add your ANTHROPIC_API_KEY"
echo "  4. Restart: sudo systemctl restart nonprofit-coach"
echo ""
echo "View logs:"
echo "  sudo journalctl -u nonprofit-coach -f"
echo ""
echo "Important files saved:"
echo "  - SSH Key: ${KEY_NAME}.pem (keep this safe!)"
echo "  - Security Group ID: $SG_ID"
echo ""
