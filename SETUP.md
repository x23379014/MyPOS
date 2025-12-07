# MyPOS Setup Guide

## Quick Start for AWS Academy Learners Lab

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Initialize AWS Resources
```bash
python manage.py init_aws
```

**Note**: If you get an S3 bucket name conflict error, edit `mypos/settings.py` and change `S3_BUCKET_NAME` to something unique (S3 bucket names must be globally unique).

### Step 4: Run the Server
```bash
python manage.py runserver 0.0.0.0:8080
```

### Step 5: Access the Application
- In Cloud9, click "Preview" and then "Preview Running Application"
- Or use the Cloud9 preview URL shown in the terminal

## First Time Usage

1. **Add Products**: Go to Products → Add New Product
   - Add at least one product to create transactions later

2. **Add Customers**: Go to Customers → Add New Customer
   - Add at least one customer to create transactions

3. **Create Transactions**: Go to Transactions → Create New Transaction
   - Select a customer
   - Add products with quantities
   - The system will automatically:
     - Save to DynamoDB
     - Send SNS notification
     - Record CloudWatch metrics

## Troubleshooting

### "AWS Credentials Not Found"
- Make sure you're running in Cloud9 environment
- Verify your AWS Academy session is active
- Check that AWS credentials are configured in Cloud9

### "S3 Bucket Already Exists"
- Edit `mypos/settings.py`
- Change `S3_BUCKET_NAME` to a unique name (e.g., `mypos-product-images-yourname`)
- Run `python manage.py init_aws` again

### "DynamoDB Table Already Exists"
- This is normal - the tables are created automatically on first use
- You can ignore this message

### Static Files Not Loading
- Run: `python manage.py collectstatic` (optional, for production)
- In development, static files should work automatically

## AWS Services Checklist

After running `init_aws`, verify in AWS Console:

-  DynamoDB: Tables `mypos-customers` and `mypos-transactions` exist
-  S3: Bucket `mypos-product-images` (or your custom name) exists
-  SNS: Topic `mypos-transaction-notifications` exists
-  CloudWatch: Metrics namespace `MyPOS/Transactions` will appear after first transaction

## Next Steps

1. Create some products
2. Add customers
3. Create a transaction
4. Check CloudWatch dashboard for metrics
5. Check SNS for transaction notifications

