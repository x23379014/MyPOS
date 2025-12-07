# MyPOS - ELB Deployment Guide for Cloud9

Complete guide to deploy MyPOS behind an Elastic Load Balancer (ELB) in AWS Academy Learners Lab.

## Overview

This guide will help you deploy MyPOS using:
- **Application Load Balancer (ALB)** - Distributes traffic to multiple EC2 instances
- **EC2 Instances** - Run your Django application
- **Target Groups** - Route traffic to healthy instances
- **Security Groups** - Control access

## Architecture

```
Internet → Application Load Balancer → Target Group → EC2 Instances (Django App)
```

## Prerequisites

- AWS Academy Learners Lab account (active session)
- MyPOS application working in Cloud9
- Basic understanding of AWS services

---

## Part 1: Prepare Your Application for Production

### Step 1: Update Django Settings for Production

Edit `mypos/settings.py`:

```python
# Change these settings for production
DEBUG = False  # IMPORTANT: Set to False for production
ALLOWED_HOSTS = ['*']  # Or specify your ALB DNS name

# Static files - will be served by ALB or S3
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security settings for production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_TLS = True
```

### Step 2: Collect Static Files

In Cloud9, run:

```bash
cd ~/MyPOS
python3 manage.py collectstatic --noinput
```

This collects all static files into `staticfiles/` directory.

---

## Part 2: Create EC2 Instances

### Step 1: Launch EC2 Instance from Cloud9 AMI

1. Go to **AWS Console** → **EC2**
2. Click **"Launch Instance"**
3. Configure:
   - **Name**: `MyPOS-Instance-1`
   - **AMI**: Use Amazon Linux 2 (or same as Cloud9)
   - **Instance Type**: `t2.micro` (free tier) or `t3.small`
   - **Key Pair**: Create new or use existing
   - **Network Settings**: 
     - Create new security group: `mypos-sg`
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow Custom TCP (port 8080) from anywhere (for Django)
   - **Storage**: 8 GB (free tier)
4. Click **"Launch Instance"**

### Step 2: Launch Additional Instance (Optional)

Repeat Step 1 to create `MyPOS-Instance-2` for high availability.

### Step 3: Note Instance IDs

Write down the Instance IDs - you'll need them for the Target Group.

---

## Part 3: Set Up Application Load Balancer

### Step 1: Create Target Group

1. Go to **EC2 Console** → **Target Groups** (under Load Balancing)
2. Click **"Create target group"**
3. Configure:
   - **Target type**: Instances
   - **Name**: `mypos-target-group`
   - **Protocol**: HTTP
   - **Port**: 8080 (Django default)
   - **VPC**: Select your VPC (same as instances)
   - **Health check**:
     - Protocol: HTTP
     - Path: `/` (or `/products/`)
     - Port: 8080
     - Healthy threshold: 2
     - Unhealthy threshold: 2
     - Timeout: 5 seconds
     - Interval: 30 seconds
4. Click **"Next"**
5. **Register targets**:
   - Select your EC2 instances
   - Click **"Include as pending below"**
   - Click **"Create target group"**

### Step 2: Create Application Load Balancer

1. Go to **EC2 Console** → **Load Balancers**
2. Click **"Create Load Balancer"**
3. Select **"Application Load Balancer"**
4. Configure:
   - **Name**: `mypos-alb`
   - **Scheme**: Internet-facing
   - **IP address type**: IPv4
   - **VPC**: Select your VPC
   - **Availability Zones**: Select at least 2 subnets
   - **Security groups**: 
     - Create new: `mypos-alb-sg`
     - Allow HTTP (port 80) from anywhere
     - Allow HTTPS (port 443) from anywhere (optional)
5. Click **"Next"**
6. **Configure routing**:
   - Target group: Select `mypos-target-group`
   - Health check: Use default
7. Click **"Next"** → **"Create load balancer"**

### Step 3: Note ALB DNS Name

After creation, note the **DNS name** (e.g., `mypos-alb-123456789.us-east-1.elb.amazonaws.com`)

---

## Part 4: Deploy Application to EC2 Instances

### Step 1: Connect to EC2 Instance

```bash
# From Cloud9 terminal or your local machine
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

### Step 2: Install Dependencies

```bash
# Update system
sudo yum update -y

# Install Python 3 and pip
sudo yum install -y python3 python3-pip git

# Install other dependencies
sudo yum install -y gcc python3-devel
```

### Step 3: Clone Your Repository

```bash
# Clone from GitHub
cd ~
git clone https://github.com/x23379014/MyPOS.git
cd MyPOS

# Install Python dependencies
pip3 install -r requirements.txt --user
```

### Step 4: Configure Django

```bash
# Edit settings.py
nano mypos/settings.py
```

Update these settings:
```python
DEBUG = False
ALLOWED_HOSTS = ['*']  # Or your ALB DNS name
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Step 5: Set Up Database and Static Files

```bash
# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Initialize AWS resources
python3 manage.py init_aws
```

### Step 6: Create Systemd Service (Optional but Recommended)

Create a service file to run Django as a service:

```bash
sudo nano /etc/systemd/system/mypos.service
```

Add this content:
```ini
[Unit]
Description=MyPOS Django Application
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/MyPOS
Environment="PATH=/home/ec2-user/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 /home/ec2-user/MyPOS/manage.py runserver 0.0.0.0:8080
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mypos
sudo systemctl start mypos
sudo systemctl status mypos
```

### Step 7: Test the Application

```bash
# Test if Django is running
curl http://localhost:8080
```

### Step 8: Repeat for Additional Instances

Repeat Steps 1-7 for any additional EC2 instances.

---

## Part 5: Configure Security Groups

### Step 1: Update EC2 Security Group

1. Go to **EC2 Console** → **Security Groups**
2. Select your EC2 instance security group (`mypos-sg`)
3. **Inbound rules**: 
   - Allow HTTP (port 8080) from ALB security group
   - Allow SSH (port 22) from your IP
4. **Outbound rules**: Allow all (default)

### Step 2: Update ALB Security Group

1. Select ALB security group (`mypos-alb-sg`)
2. **Inbound rules**:
   - Allow HTTP (port 80) from anywhere (0.0.0.0/0)
   - Allow HTTPS (port 443) from anywhere (optional)
3. **Outbound rules**: Allow all (default)

---

## Part 6: Test the Deployment

### Step 1: Check Target Health

1. Go to **EC2 Console** → **Target Groups**
2. Select `mypos-target-group`
3. Check **"Targets"** tab
4. Wait for targets to show as **"healthy"** (may take 1-2 minutes)

### Step 2: Access via ALB

1. Copy the ALB DNS name from Load Balancers
2. Open in browser: `http://your-alb-dns-name.us-east-1.elb.amazonaws.com`
3. You should see the MyPOS home page

### Step 3: Test Functionality

- Navigate to Products, Customers, Transactions
- Test CRUD operations
- Verify AWS services (DynamoDB, S3, SNS, CloudWatch)

---

## Part 7: Optional - Set Up Custom Domain (Optional)

If you have a domain:

1. Go to **Route 53** (or your DNS provider)
2. Create an A record (Alias) pointing to your ALB
3. Update `ALLOWED_HOSTS` in `settings.py`:
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

---

## Part 8: Monitoring and Maintenance

### CloudWatch Metrics

1. Go to **CloudWatch** → **Metrics**
2. View ALB metrics:
   - Request count
   - Target response time
   - Healthy/unhealthy host count
3. View EC2 metrics:
   - CPU utilization
   - Network in/out

### Set Up CloudWatch Dashboard

1. Go to **CloudWatch** → **Dashboards**
2. Create dashboard for:
   - ALB request count
   - Target health
   - EC2 CPU/Memory
   - MyPOS transaction metrics

### Logs

View logs:
- **ALB Access Logs**: Enable in ALB settings
- **EC2 Application Logs**: Check `/var/log/mypos.log` or systemd journal

---

## Troubleshooting

### Issue: Targets Show as Unhealthy

**Solutions**:
1. Check security group rules (EC2 must allow port 8080 from ALB)
2. Verify Django is running: `sudo systemctl status mypos`
3. Test locally: `curl http://localhost:8080`
4. Check health check path in Target Group settings
5. Review CloudWatch logs

### Issue: 502 Bad Gateway

**Solutions**:
1. Check if Django is running on port 8080
2. Verify security groups allow traffic
3. Check application logs
4. Ensure `ALLOWED_HOSTS` includes ALB DNS name

### Issue: Static Files Not Loading

**Solutions**:
1. Run `python3 manage.py collectstatic --noinput`
2. Configure ALB to serve static files (or use S3)
3. Check `STATIC_ROOT` and `STATIC_URL` in settings.py

### Issue: CSRF Errors

**Solutions**:
1. Add ALB DNS name to `CSRF_TRUSTED_ORIGINS`:
   ```python
   CSRF_TRUSTED_ORIGINS = [
       'https://your-alb-dns-name.us-east-1.elb.amazonaws.com',
   ]
   ```
2. Ensure `SECURE_PROXY_SSL_HEADER` is set correctly

### Issue: AWS Services Not Working

**Solutions**:
1. Verify IAM roles are attached to EC2 instances
2. Check AWS credentials (should use instance profile in production)
3. Verify security groups allow outbound HTTPS (port 443)

---

## Quick Reference Commands

### On EC2 Instance

```bash
# Check Django status
sudo systemctl status mypos

# Restart Django
sudo systemctl restart mypos

# View logs
sudo journalctl -u mypos -f

# Update code
cd ~/MyPOS
git pull origin main
sudo systemctl restart mypos
```

### In AWS Console

- **ALB DNS**: EC2 → Load Balancers → Select ALB → Copy DNS name
- **Target Health**: EC2 → Target Groups → Select group → Targets tab
- **Security Groups**: EC2 → Security Groups

---

## Cost Considerations (AWS Academy)

- **ALB**: Usually included in AWS Academy credits
- **EC2 Instances**: Use t2.micro (free tier) or t3.small
- **Data Transfer**: Minimal for testing
- **CloudWatch**: Basic monitoring included

---

## Next Steps

1. ✅ Set up HTTPS/SSL certificate (optional)
2. ✅ Configure auto-scaling (optional)
3. ✅ Set up CloudWatch alarms
4. ✅ Configure backup strategy
5. ✅ Set up CI/CD pipeline (optional)

---

## Important Notes

- **AWS Academy Session**: Your session expires - refresh if services stop working
- **Security**: Never commit AWS credentials to GitHub
- **Production**: This is a basic setup - enhance security for real production use
- **Testing**: Always test in staging before production deployment

---

## Support

If you encounter issues:
1. Check CloudWatch logs
2. Verify security group rules
3. Test application locally on EC2
4. Review AWS Academy service limits

Happy deploying! 🚀

