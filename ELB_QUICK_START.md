# ELB Deployment - Quick Start

## 🚀 Quick Deployment Steps

### 1. Create EC2 Instances
- Launch 2 EC2 instances (t2.micro)
- Use Amazon Linux 2 AMI
- Security group: Allow SSH (22) and HTTP (8080)

### 2. Deploy App to EC2
```bash
# SSH into EC2
ssh -i key.pem ec2-user@ec2-ip

# Install and setup
sudo yum install -y python3 python3-pip git
git clone https://github.com/x23379014/MyPOS.git
cd MyPOS
pip3 install -r requirements.txt --user
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py init_aws

# Run Django
python3 manage.py runserver 0.0.0.0:8080
```

### 3. Create Target Group
- EC2 → Target Groups → Create
- Protocol: HTTP, Port: 8080
- Register your EC2 instances
- Health check: HTTP:8080/

### 4. Create Load Balancer
- EC2 → Load Balancers → Create ALB
- Internet-facing
- Select 2+ subnets
- Security group: Allow HTTP (80) from anywhere
- Target group: Select your target group

### 5. Update Django Settings
```python
# In mypos/settings.py
DEBUG = False
ALLOWED_HOSTS = ['*']  # Or your ALB DNS name
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### 6. Access Your App
- Copy ALB DNS name
- Open in browser: `http://your-alb-dns-name.elb.amazonaws.com`

---

## ⚙️ Security Groups

**EC2 Security Group:**
- Inbound: SSH (22) from your IP, HTTP (8080) from ALB SG
- Outbound: All

**ALB Security Group:**
- Inbound: HTTP (80) from anywhere, HTTPS (443) optional
- Outbound: All

---

## 🔍 Troubleshooting

**Targets Unhealthy?**
- Check security groups
- Verify Django running on port 8080
- Test: `curl http://localhost:8080`

**502 Error?**
- Check Django is running
- Verify port 8080 is open
- Check application logs

**CSRF Errors?**
- Add ALB DNS to `CSRF_TRUSTED_ORIGINS`

---

For detailed instructions, see **[ELB_DEPLOYMENT.md](ELB_DEPLOYMENT.md)**

