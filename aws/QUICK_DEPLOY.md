# Quick AWS Deployment

## One-Command Deploy

```bash
cd aws && ./deploy.sh
```

## After Deployment

1. **Note your public IP** from the output
2. **SSH into server:**
   ```bash
   ssh -i nonprofit-coach-key.pem ubuntu@YOUR_IP
   ```
3. **Add API key:**
   ```bash
   nano /home/ubuntu/nonprofit/nonprofit_coach/.env
   ```
   Add: `ANTHROPIC_API_KEY=sk-ant-your-key`
4. **Restart:**
   ```bash
   sudo systemctl restart nonprofit-coach
   ```
5. **Access:** `http://YOUR_IP`

## Common Commands

```bash
# View logs
sudo journalctl -u nonprofit-coach -f

# Restart
sudo systemctl restart nonprofit-coach

# Update code
cd /home/ubuntu/nonprofit/nonprofit_coach
git pull
sudo systemctl restart nonprofit-coach

# Backup database
scp -i nonprofit-coach-key.pem ubuntu@YOUR_IP:/home/ubuntu/nonprofit/nonprofit_coach/nonprofit.db ./backup.db
```

## Cost

~$18-22/month for t3.small instance

## Need Help?

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.
