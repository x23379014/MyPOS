# Fix: AWS Security Token Invalid Error

## Error Message
```
UnrecognizedClientException: The security token included in the request is invalid
```

## Cause
Your AWS Academy Learners Lab credentials have **expired**. AWS Academy sessions expire after a certain time period (usually 1-4 hours).

---

## Solution: Refresh AWS Credentials in Cloud9

### Step 1: Get New AWS Credentials from AWS Academy

1. **Go to AWS Academy Learners Lab**
2. Click **"AWS Details"** → **"AWS CLI"**
3. You'll see your credentials in this format:
   ```
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   AWS_SESSION_TOKEN=...
   ```

### Step 2: Update Credentials in Cloud9

**Option A: Update via AWS CLI (Recommended)**

```bash
# In Cloud9 terminal, run:
aws configure

# When prompted, enter:
# AWS Access Key ID: [paste your AWS_ACCESS_KEY_ID]
# AWS Secret Access Key: [paste your AWS_SECRET_ACCESS_KEY]
# Default region name: us-east-1 (or your region)
# Default output format: json

# Then set the session token:
export AWS_SESSION_TOKEN="your-session-token-here"
```

**Option B: Set Environment Variables Directly**

```bash
# In Cloud9 terminal, run these commands (replace with your actual credentials):
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_SESSION_TOKEN="your-session-token"
export AWS_DEFAULT_REGION="us-east-1"

# Verify credentials are set
aws sts get-caller-identity
```

**Option C: Update Credentials File (Permanent until session expires)**

```bash
# Edit the credentials file
nano ~/.aws/credentials

# Add or update:
[default]
aws_access_key_id = your-access-key-id
aws_secret_access_key = your-secret-access-key
aws_session_token = your-session-token

# Save and exit (Ctrl+X, then Y, then Enter)

# Also update config file
nano ~/.aws/config

# Add or update:
[default]
region = us-east-1
output = json

# Save and exit
```

### Step 3: Verify Credentials Work

```bash
# Test AWS credentials
aws sts get-caller-identity

# You should see output like:
# {
#     "UserId": "...",
#     "Account": "...",
#     "Arn": "..."
# }
```

### Step 4: Restart Django Server

```bash
# Stop the server (Ctrl+C if running)
# Then restart:
cd ~/MyPOS
python3 manage.py runserver 0.0.0.0:8080
```

---

## Quick Fix Script

Create a script to quickly update credentials:

```bash
# Create a script file
nano ~/update_aws_creds.sh
```

Paste this content (replace with your credentials from AWS Academy):

```bash
#!/bin/bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_SESSION_TOKEN="your-session-token"
export AWS_DEFAULT_REGION="us-east-1"

echo "AWS credentials updated!"
aws sts get-caller-identity
```

Make it executable:
```bash
chmod +x ~/update_aws_creds.sh
```

Then whenever credentials expire, just run:
```bash
source ~/update_aws_creds.sh
```

---

## Alternative: Use AWS Academy Auto-Refresh

Some Cloud9 environments in AWS Academy automatically refresh credentials. If yours doesn't:

1. **Check if Cloud9 auto-refresh is enabled**:
   ```bash
   # Check if credentials are auto-refreshed
   cat ~/.aws/credentials
   ```

2. **If not, you need to manually refresh** every time the session expires

---

## Prevention Tips

1. **Check session expiration time** in AWS Academy Learners Lab dashboard
2. **Refresh credentials proactively** before they expire
3. **Use the quick fix script** above for faster credential updates
4. **Monitor CloudWatch logs** to catch credential expiration early

---

## Verify Everything Works

After updating credentials, test:

1. **Test AWS connection**:
   ```bash
   aws sts get-caller-identity
   ```

2. **Test DynamoDB**:
   ```bash
   aws dynamodb list-tables
   ```

3. **Test S3**:
   ```bash
   aws s3 ls
   ```

4. **Test SNS**:
   ```bash
   aws sns list-topics
   ```

5. **Test in Django**:
   - Create a new transaction
   - Check that it works without errors

---

## Common Issues

### Issue: "Credentials still not working after update"

**Solution**:
- Make sure you copied the **entire** session token (it's very long)
- Check that there are no extra spaces or quotes
- Verify the credentials are from the **current** AWS Academy session
- Try logging out and back into AWS Academy to get fresh credentials

### Issue: "Session token expired immediately"

**Solution**:
- AWS Academy sessions have a time limit
- Get new credentials from AWS Academy
- Make sure you're using the **latest** credentials from the dashboard

### Issue: "Can't find AWS Details in AWS Academy"

**Solution**:
- Make sure you're logged into the correct AWS Academy Learners Lab
- Look for "AWS CLI" or "Credentials" in the dashboard
- Some interfaces show it as "Show AWS CLI" or "View Credentials"

---

## Notes

- **Credentials expire**: AWS Academy credentials typically expire after 1-4 hours
- **No hardcoding needed**: The project uses default AWS credentials automatically
- **Cloud9 integration**: Cloud9 should auto-detect credentials, but manual refresh may be needed
- **Region**: Make sure you're using the correct AWS region (usually `us-east-1` for AWS Academy)

---

## After Fixing

Once credentials are updated:
1. ✅ Restart Django server
2. ✅ Test creating a transaction
3. ✅ Verify customer name displays correctly
4. ✅ Check that SNS notifications work

Your application should now work correctly! 🚀

