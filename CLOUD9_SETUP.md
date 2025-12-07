# MyPOS - Cloud9 Setup Guide

Complete guide to set up MyPOS in AWS Cloud9 and pull from GitHub.

## Prerequisites

- AWS Academy Learners Lab account
- GitHub account (free account works)
- Access to Cloud9 environment

---

## Part 1: Push Project to GitHub

### Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository name: `MyPOS` (or any name you prefer)
4. Description: "Simple POS System with AWS Services"
5. Choose **Public** or **Private** (Private is recommended)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **"Create repository"**

### Step 2: Initialize Git and Push to GitHub (From Your Local Machine)

Open terminal in your local machine (where MyPOS project is located):

```bash
# Navigate to your project directory
cd /Users/nikhiltamatta/Desktop/MyPOS

# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: MyPOS project"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/MyPOS.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: You'll be prompted for GitHub username and password/token. Use a Personal Access Token if 2FA is enabled.

---

## Part 2: Set Up Cloud9 Environment

### Step 1: Launch Cloud9 in AWS Academy

1. Log in to your **AWS Academy Learners Lab**
2. Click **"AWS Details"** → **"AWS CLI"** to get your credentials
3. Go to **AWS Console** (use the provided link)
4. Search for **"Cloud9"** in the services search bar
5. Click **"Create environment"**

### Step 2: Configure Cloud9 Environment

1. **Name**: `MyPOS-Environment` (or any name)
2. **Description**: "MyPOS Development Environment"
3. **Environment type**: Choose **"Create a new EC2 instance for environment"**
4. **Instance type**: `t2.micro` (free tier) or `t3.small`
5. **Platform**: **Ubuntu Server**
6. Click **"Next step"**
7. Review and click **"Create environment"**

### Step 3: Wait for Cloud9 to Launch

- Cloud9 will take 1-2 minutes to set up
- The IDE will open automatically when ready

---

## Part 3: Clone Project from GitHub in Cloud9

### Step 1: Open Cloud9 Terminal

- The terminal is at the bottom of the Cloud9 IDE
- If not visible, go to **Window** → **New Terminal**

### Step 2: Clone Your GitHub Repository

```bash
# Navigate to your home directory (or preferred location)
cd ~

# Clone your repository (replace YOUR_USERNAME with your GitHub username)
git clone https://github.com/YOUR_USERNAME/MyPOS.git

# Navigate into the project
cd MyPOS

# Verify files are there
ls -la
```

### Step 3: Verify Project Structure

```bash
# Check that all important files exist
ls -la
ls templates/
ls static/
ls pos/
```

You should see:
- `manage.py`
- `requirements.txt`
- `mypos/` directory
- `pos/` directory
- `templates/` directory
- `static/` directory
- `error_handler/` directory

---

## Part 4: Set Up Python Environment in Cloud9

### Step 1: Check Python Version

```bash
python3 --version
# Should show Python 3.x
```

### Step 2: Install Dependencies

```bash
# Install pip if not already installed
sudo apt-get update
sudo apt-get install -y python3-pip

# Install project dependencies
pip3 install -r requirements.txt --user
```

**Note**: If you get permission errors, use `--user` flag or create a virtual environment:

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Part 5: Configure Django in Cloud9

### Step 1: Run Database Migrations

```bash
# Make sure you're in the project directory
cd ~/MyPOS

# Create migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate
```

### Step 2: Initialize AWS Resources

```bash
# Initialize AWS resources (DynamoDB, S3, SNS)
python3 manage.py init_aws
```

**Important Notes**:
- If you get an S3 bucket name conflict, edit `mypos/settings.py`:
  ```python
  S3_BUCKET_NAME = 'mypos-product-images-yourname-12345'  # Make it unique
  ```
- AWS credentials are automatically available in Cloud9 from AWS Academy

### Step 3: Verify AWS Credentials

```bash
# Check AWS credentials (should work automatically in Cloud9)
aws sts get-caller-identity
```

If this works, you're all set! If not, check your AWS Academy session.

---

## Part 6: Run the Application in Cloud9

### Step 1: Start Django Server

```bash
# Make sure you're in the project directory
cd ~/MyPOS

# Run the server (Cloud9 uses port 8080)
python3 manage.py runserver 0.0.0.0:8080
```

### Step 2: Access the Application

1. In Cloud9, click **"Preview"** → **"Preview Running Application"**
2. Or click the **"Share"** button and copy the preview URL
3. The application will open in a new browser tab

**Alternative**: You can also access via:
- Cloud9 preview URL (shown in the IDE)
- Format: `https://xxxxx.vfs.cloud9.us-east-1.amazonaws.com`

---

## Part 7: Verify Everything Works

### Test the Application

1. **Home Page**: Should show the MyPOS welcome page
2. **Add a Product**: 
   - Go to Products → Add New Product
   - Fill in details and save
3. **Add a Customer**:
   - Go to Customers → Add New Customer
   - Fill in details and save
4. **Create a Transaction**:
   - Go to Transactions → Create New Transaction
   - Select customer and products
   - Complete the transaction

### Check AWS Services

1. **DynamoDB**: Go to AWS Console → DynamoDB
   - Verify tables: `mypos-customers` and `mypos-transactions`
2. **S3**: Go to AWS Console → S3
   - Verify bucket: `mypos-product-images` (or your custom name)
3. **SNS**: Go to AWS Console → SNS
   - Verify topic: `mypos-transaction-notifications`
4. **CloudWatch**: Go to AWS Console → CloudWatch
   - Check metrics under namespace: `MyPOS/Transactions`

---

## Troubleshooting

### Issue: "AWS Credentials Not Found"

**Solution**:
```bash
# Check if AWS credentials are set
aws configure list

# If empty, your AWS Academy session might have expired
# Refresh your AWS Academy Learners Lab session
```

### Issue: "S3 Bucket Already Exists"

**Solution**:
1. Edit `mypos/settings.py`
2. Change `S3_BUCKET_NAME` to something unique:
   ```python
   S3_BUCKET_NAME = 'mypos-product-images-yourname-12345'
   ```
3. Run `python3 manage.py init_aws` again

### Issue: "Port 8080 Already in Use"

**Solution**:
```bash
# Find what's using port 8080
sudo lsof -i :8080

# Kill the process or use a different port
python3 manage.py runserver 0.0.0.0:8081
```

### Issue: "Static Files Not Loading"

**Solution**:
```bash
# Collect static files
python3 manage.py collectstatic --noinput

# Or check that static files are in the right place
ls static/css/
```

### Issue: "Git Clone Fails"

**Solution**:
- Make sure the repository is public, OR
- Use SSH instead of HTTPS:
  ```bash
  git clone git@github.com:YOUR_USERNAME/MyPOS.git
  ```
- Or use a Personal Access Token for HTTPS

---

## Quick Reference Commands

```bash
# Navigate to project
cd ~/MyPOS

# Pull latest changes from GitHub
git pull origin main

# Run migrations
python3 manage.py migrate

# Start server
python3 manage.py runserver 0.0.0.0:8080

# Initialize AWS resources
python3 manage.py init_aws

# Check AWS credentials
aws sts get-caller-identity
```

---

## Next Steps After Setup

1. ✅ Test all CRUD operations (Products, Customers, Transactions)
2. ✅ Verify AWS services are working (DynamoDB, S3, SNS, CloudWatch)
3. ✅ Create a CloudWatch dashboard for transaction metrics
4. ✅ Set up ELB (Elastic Load Balancer) for production deployment (if needed)

---

## Important Notes

- **AWS Academy Session**: Your AWS Academy session expires after a certain time. Refresh it if services stop working.
- **Cloud9 Auto-Save**: Cloud9 auto-saves your work, but commit to GitHub regularly:
  ```bash
  git add .
  git commit -m "Your commit message"
  git push origin main
  ```
- **Port Configuration**: Cloud9 uses port 8080 by default. The application is configured to run on this port.
- **No Hardcoded Credentials**: The project uses default AWS credentials from Cloud9 automatically.

---

## Support

If you encounter issues:
1. Check the error messages in the terminal
2. Verify AWS Academy session is active
3. Check AWS service permissions in AWS Console
4. Review the README.md and SETUP.md files

Happy coding! 🚀

