# SNS Notification Troubleshooting Guide

## Error: "Transaction created but notification failed"

This error occurs when the transaction is successfully created in DynamoDB, but the SNS notification fails to send.

## Common Causes and Solutions

### 1. SNS Topic Not Created

**Symptom**: Error message mentions "topic not found" or "does not exist"

**Solution**:
```bash
# In Cloud9 terminal
cd ~/MyPOS
python3 manage.py init_aws
```

This will create the SNS topic if it doesn't exist.

### 2. IAM Permissions Issue

**Symptom**: Error message mentions "AccessDenied" or "AuthorizationError"

**Solution**:
1. Go to AWS Console → IAM
2. Check your AWS Academy role permissions
3. Ensure the role has these SNS permissions:
   - `sns:CreateTopic`
   - `sns:ListTopics`
   - `sns:Publish`
   - `sns:GetTopicAttributes`

**Note**: In AWS Academy Learners Lab, permissions are usually pre-configured. If you see this error, your session might have expired or permissions were revoked.

### 3. AWS Region Mismatch

**Symptom**: Topic not found even though it exists

**Solution**:
1. Check `mypos/settings.py`:
   ```python
   AWS_REGION = 'us-east-1'  # Make sure this matches your Cloud9 region
   ```
2. Verify your Cloud9 region:
   ```bash
   aws configure get region
   ```
3. Update `AWS_REGION` in settings.py to match

### 4. Topic Name Mismatch

**Symptom**: Topic exists but can't be found

**Solution**:
The topic name is hardcoded as `mypos-transaction-notifications`. If you created a topic with a different name, either:
- Delete the old topic and run `python3 manage.py init_aws`
- Or update the topic name in `pos/aws_services.py` line 290

### 5. AWS Academy Session Expired

**Symptom**: All AWS services fail

**Solution**:
1. Refresh your AWS Academy Learners Lab session
2. Restart Cloud9 environment if needed
3. Verify credentials:
   ```bash
   aws sts get-caller-identity
   ```

## Verification Steps

### Step 1: Check if Topic Exists

```bash
# In Cloud9 terminal
aws sns list-topics
```

Look for a topic containing `mypos-transaction-notifications`

### Step 2: Check SNS Permissions

```bash
# Test SNS access
aws sns list-topics
```

If this fails, you have a permissions issue.

### Step 3: Manually Create Topic (if needed)

```bash
aws sns create-topic --name mypos-transaction-notifications
```

Note the TopicArn returned and verify it matches what the application expects.

### Step 4: Test SNS Publish

```bash
# Get your topic ARN first
TOPIC_ARN=$(aws sns list-topics --query 'Topics[?contains(TopicArn, `mypos-transaction-notifications`)].TopicArn' --output text)

# Test publish
aws sns publish --topic-arn "$TOPIC_ARN" --message "Test message" --subject "Test"
```

If this fails, check the error message for specific issues.

## Debugging in Code

The updated code now provides more detailed error messages. Check:

1. **Django Logs**: Check the terminal where Django is running for detailed error messages
2. **Error Messages**: The warning message now shows more details about what failed
3. **CloudWatch Logs**: Check CloudWatch for application logs

## Quick Fix

If you just want to get notifications working quickly:

```bash
# 1. Initialize AWS resources
cd ~/MyPOS
python3 manage.py init_aws

# 2. Verify SNS topic was created
aws sns list-topics | grep mypos

# 3. Restart Django server
# Stop current server (Ctrl+C)
python3 manage.py runserver 0.0.0.0:8080

# 4. Try creating a transaction again
```

## Expected Behavior

When working correctly:
- Transaction is created in DynamoDB ✅
- SNS notification is sent ✅
- CloudWatch metrics are recorded ✅
- Success message shows transaction ID ✅

## If Nothing Works

If notifications still fail after trying all solutions:

1. **Check AWS Academy Session**: Make sure your session is active
2. **Verify Region**: Ensure all services are in the same region
3. **Check Service Limits**: AWS Academy may have service limits
4. **Contact Support**: If it's an AWS Academy issue, contact your instructor

## Note

SNS notifications are **optional** for transaction processing. The transaction will still be created successfully even if notifications fail. This is by design - notifications are a "nice to have" feature, not critical for the core functionality.

