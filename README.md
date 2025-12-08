# MyPOS - Point of Sale System

A simple and basic Point of Sale (POS) system built with Django and AWS services. This project is designed for AWS Academy Learners Lab and uses default AWS credentials from Cloud9 environment.

## Features

- **Product Management**: Full CRUD operations for products
  - Add, edit, delete products
  - Upload product images to S3
  - Track product inventory

- **Customer Management**: Full CRUD operations for customers
  - Store customer data in DynamoDB
  - Add, edit, delete customers
  - Customer information tracking

- **Transaction Processing**: Create and view transactions
  - Create transactions with multiple products
  - Store transaction data in DynamoDB
  - Automatic SNS notifications
  - CloudWatch metrics tracking

- **AWS Services Integration**:
  - **DynamoDB**: Stores customer and transaction data
  - **S3**: Stores product images
  - **SNS**: Sends transaction notifications
  - **CloudWatch**: Tracks transaction metrics and provides dashboards

- **Custom Error Handling**: Python library for handling AWS and application errors

## Prerequisites

- Python 3.8 or higher
- AWS Academy Learners Lab account
- Cloud9 environment (or AWS credentials configured)
- Django 4.2+

## Installation

1. Clone or download this project to your Cloud9 environment

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations (for local SQLite database used for products):
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create the necessary AWS resources (tables, buckets, topics) - they will be created automatically on first use, or you can run:
```bash
python manage.py shell
```

Then in the shell:
```python
from pos.aws_services import DynamoDBService, S3Service, SNSService

# Create DynamoDB tables
DynamoDBService.create_tables()

# Create S3 bucket
S3Service.create_bucket()

# Create SNS topic
SNSService.get_or_create_topic()
```

5. Run the development server:
```bash
python manage.py runserver 0.0.0.0:8080
```

6. Access the application in your browser at the Cloud9 preview URL

## Project Structure

```
MyPOS/
├── error_handler/          # Custom error handling library
│   ├── __init__.py
│   └── error_handler.py
├── mypos/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pos/                    # Main application
│   ├── models.py          # Product model (local DB)
│   ├── views.py           # All CRUD views
│   ├── aws_services.py    # AWS service integrations
│   └── apps.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── products/
│   ├── customers/
│   └── transactions/
├── static/                # CSS files
│   └── css/
│       └── style.css
├── manage.py
├── requirements.txt
└── README.md
```

## AWS Services Configuration

### DynamoDB Tables
- **mypos-customers**: Stores customer information
- **mypos-transactions**: Stores transaction data

### S3 Bucket
- **mypos-product-images**: Stores product images

### SNS Topic
- **mypos-transaction-notifications**: Sends transaction notifications

### CloudWatch
- **Namespace**: MyPOS/Transactions
- **Metrics**: TransactionAmount, TransactionCount

## Usage

### Products
1. Navigate to "Products" in the menu
2. Click "Add New Product" to create a product
3. Fill in product details and optionally upload an image
4. Use "Edit" or "Delete" buttons to manage products

### Customers
1. Navigate to "Customers" in the menu
2. Click "Add New Customer" to create a customer
3. Fill in customer information
4. Use "Edit" or "Delete" buttons to manage customers

### Transactions
1. Navigate to "Transactions" in the menu
2. Click "Create New Transaction"
3. Select a customer and add products with quantities
4. The system will:
   - Save the transaction to DynamoDB
   - Send an SNS notification
   - Record metrics in CloudWatch
5. View transaction details by clicking "View"

## Error Handling

The project includes a custom error handling library (`error_handler`) that:
- Handles AWS service errors gracefully
- Provides user-friendly error messages
- Logs errors for debugging
- Converts AWS exceptions to custom POSError exceptions

## Deployment with ELB

For deployment using Elastic Load Balancer (ELB), see the complete guide:

Quick steps:
1. Create EC2 instances from your Cloud9 environment
2. Deploy application to EC2 instances
3. Set up Application Load Balancer (ALB)
4. Configure Target Groups
5. Update Django settings for production
6. Configure Security Groups
