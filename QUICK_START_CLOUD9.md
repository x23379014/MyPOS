# Quick Start - Cloud9 Setup (Cheat Sheet)

## Quick Steps

### 1. Push to GitHub (From Your Local Machine)

```bash
cd /Users/nikhiltamatta/Desktop/MyPOS
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/MyPOS.git
git branch -M main
git push -u origin main
```

### 2. In Cloud9 - Clone and Setup

```bash
# Clone repository
cd ~
git clone https://github.com/YOUR_USERNAME/MyPOS.git
cd MyPOS

# Install dependencies
pip3 install -r requirements.txt --user

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Initialize AWS resources
python3 manage.py init_aws

# Run server
python3 manage.py runserver 0.0.0.0:8080
```

### 3. Access Application

- Click **"Preview"** → **"Preview Running Application"** in Cloud9
- Or use the Cloud9 preview URL

---

## Common Issues

**S3 Bucket Name Conflict?**
```bash
# Edit mypos/settings.py and change S3_BUCKET_NAME to something unique
```

**AWS Credentials Error?**
```bash
# Check credentials
aws sts get-caller-identity
# Refresh AWS Academy session if needed
```

**Port Already in Use?**
```bash
# Use different port
python3 manage.py runserver 0.0.0.0:8081
```

---

For detailed instructions, see **CLOUD9_SETUP.md**

