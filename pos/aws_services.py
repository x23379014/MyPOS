"""
AWS Services Integration for MyPOS
Uses default AWS credentials from AWS Academy Learners Lab
"""

import boto3
import json
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from error_handler.error_handler import ErrorHandler, POSError

# Initialize AWS clients - uses default credentials from environment
dynamodb = boto3.client('dynamodb', region_name=settings.AWS_REGION)
s3 = boto3.client('s3', region_name=settings.AWS_REGION)
sns = boto3.client('sns', region_name=settings.AWS_REGION)
cloudwatch = boto3.client('cloudwatch', region_name=settings.AWS_REGION)


class DynamoDBService:
    """Service for DynamoDB operations"""
    
    @staticmethod
    def create_tables():
        """Create DynamoDB tables if they don't exist"""
        try:
            # Create Customers table
            try:
                dynamodb.create_table(
                    TableName=settings.DYNAMODB_CUSTOMERS_TABLE,
                    KeySchema=[
                        {'AttributeName': 'customer_id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'customer_id', 'AttributeType': 'S'}
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                ErrorHandler.log_success("Created customers table")
            except dynamodb.exceptions.ResourceInUseException:
                pass  # Table already exists
            
            # Create Transactions table
            try:
                dynamodb.create_table(
                    TableName=settings.DYNAMODB_TRANSACTIONS_TABLE,
                    KeySchema=[
                        {'AttributeName': 'transaction_id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'transaction_id', 'AttributeType': 'S'}
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                ErrorHandler.log_success("Created transactions table")
            except dynamodb.exceptions.ResourceInUseException:
                pass  # Table already exists
                
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "create_tables", "DynamoDB")
    
    @staticmethod
    def add_customer(customer_data):
        """Add customer to DynamoDB"""
        try:
            item = {
                'customer_id': {'S': customer_data['customer_id']},
                'name': {'S': customer_data['name']},
                'email': {'S': customer_data.get('email', '')},
                'phone': {'S': customer_data.get('phone', '')},
                'address': {'S': customer_data.get('address', '')},
                'created_at': {'S': datetime.now().isoformat()}
            }
            
            dynamodb.put_item(
                TableName=settings.DYNAMODB_CUSTOMERS_TABLE,
                Item=item
            )
            ErrorHandler.log_success("add_customer", customer_data['customer_id'])
            return True
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "add_customer", "DynamoDB")
    
    @staticmethod
    def get_customer(customer_id):
        """Get customer from DynamoDB"""
        try:
            response = dynamodb.get_item(
                TableName=settings.DYNAMODB_CUSTOMERS_TABLE,
                Key={'customer_id': {'S': customer_id}}
            )
            
            if 'Item' in response:
                item = response['Item']
                return {
                    'customer_id': item['customer_id']['S'],
                    'name': item['name']['S'],
                    'email': item.get('email', {}).get('S', ''),
                    'phone': item.get('phone', {}).get('S', ''),
                    'address': item.get('address', {}).get('S', ''),
                    'created_at': item.get('created_at', {}).get('S', '')
                }
            return None
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "get_customer", customer_id)
    
    @staticmethod
    def list_customers():
        """List all customers from DynamoDB"""
        try:
            response = dynamodb.scan(TableName=settings.DYNAMODB_CUSTOMERS_TABLE)
            customers = []
            
            for item in response.get('Items', []):
                customers.append({
                    'customer_id': item['customer_id']['S'],
                    'name': item['name']['S'],
                    'email': item.get('email', {}).get('S', ''),
                    'phone': item.get('phone', {}).get('S', ''),
                    'address': item.get('address', {}).get('S', ''),
                    'created_at': item.get('created_at', {}).get('S', '')
                })
            
            return customers
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "list_customers", "DynamoDB")
    
    @staticmethod
    def update_customer(customer_id, customer_data):
        """Update customer in DynamoDB"""
        try:
            update_expression = "SET #name = :name, email = :email, phone = :phone, address = :address"
            expression_attribute_names = {'#name': 'name'}
            expression_attribute_values = {
                ':name': {'S': customer_data['name']},
                ':email': {'S': customer_data.get('email', '')},
                ':phone': {'S': customer_data.get('phone', '')},
                ':address': {'S': customer_data.get('address', '')}
            }
            
            dynamodb.update_item(
                TableName=settings.DYNAMODB_CUSTOMERS_TABLE,
                Key={'customer_id': {'S': customer_id}},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
            ErrorHandler.log_success("update_customer", customer_id)
            return True
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "update_customer", customer_id)
    
    @staticmethod
    def delete_customer(customer_id):
        """Delete customer from DynamoDB"""
        try:
            dynamodb.delete_item(
                TableName=settings.DYNAMODB_CUSTOMERS_TABLE,
                Key={'customer_id': {'S': customer_id}}
            )
            ErrorHandler.log_success("delete_customer", customer_id)
            return True
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "delete_customer", customer_id)
    
    @staticmethod
    def add_transaction(transaction_data):
        """Add transaction to DynamoDB"""
        try:
            # Get customer name if not already provided
            customer_name = transaction_data.get('customer_name')
            if not customer_name:
                try:
                    customer = DynamoDBService.get_customer(transaction_data['customer_id'])
                    customer_name = customer['name'] if customer else None
                except:
                    customer_name = None
            
            item = {
                'transaction_id': {'S': transaction_data['transaction_id']},
                'customer_id': {'S': transaction_data['customer_id']},
                'products': {'S': json.dumps(transaction_data['products'])},
                'total_amount': {'N': str(transaction_data['total_amount'])},
                'status': {'S': transaction_data.get('status', 'completed')},
                'created_at': {'S': datetime.now().isoformat()}
            }
            
            # Add customer_name if available
            if customer_name:
                item['customer_name'] = {'S': customer_name}
            
            dynamodb.put_item(
                TableName=settings.DYNAMODB_TRANSACTIONS_TABLE,
                Item=item
            )
            ErrorHandler.log_success("add_transaction", transaction_data['transaction_id'])
            return True
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "add_transaction", "DynamoDB")
    
    @staticmethod
    def get_transaction(transaction_id):
        """Get transaction from DynamoDB"""
        try:
            response = dynamodb.get_item(
                TableName=settings.DYNAMODB_TRANSACTIONS_TABLE,
                Key={'transaction_id': {'S': transaction_id}}
            )
            
            if 'Item' in response:
                item = response['Item']
                transaction = {
                    'transaction_id': item['transaction_id']['S'],
                    'customer_id': item['customer_id']['S'],
                    'products': json.loads(item['products']['S']),
                    'total_amount': float(item['total_amount']['N']),
                    'status': item.get('status', {}).get('S', 'completed'),
                    'created_at': item.get('created_at', {}).get('S', '')
                }
                
                # Get customer_name if stored in transaction
                if 'customer_name' in item:
                    transaction['customer_name'] = item['customer_name']['S']
                else:
                    # Look up customer name if not stored
                    try:
                        customer = DynamoDBService.get_customer(transaction['customer_id'])
                        transaction['customer_name'] = customer['name'] if customer else None
                    except:
                        transaction['customer_name'] = None
                
                return transaction
            return None
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "get_transaction", transaction_id)
    
    @staticmethod
    def list_transactions():
        """List all transactions from DynamoDB"""
        try:
            response = dynamodb.scan(TableName=settings.DYNAMODB_TRANSACTIONS_TABLE)
            transactions = []
            
            for item in response.get('Items', []):
                transaction = {
                    'transaction_id': item['transaction_id']['S'],
                    'customer_id': item['customer_id']['S'],
                    'products': json.loads(item['products']['S']),
                    'total_amount': float(item['total_amount']['N']),
                    'status': item.get('status', {}).get('S', 'completed'),
                    'created_at': item.get('created_at', {}).get('S', '')
                }
                
                # Get customer_name if stored in transaction
                if 'customer_name' in item:
                    transaction['customer_name'] = item['customer_name']['S']
                
                transactions.append(transaction)
            
            # Sort by created_at descending
            transactions.sort(key=lambda x: x['created_at'], reverse=True)
            return transactions
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "list_transactions", "DynamoDB")


class S3Service:
    """Service for S3 operations"""
    
    @staticmethod
    def create_bucket():
        """Create S3 bucket if it doesn't exist and configure for public read access"""
        try:
            # Check if bucket exists
            try:
                s3.head_bucket(Bucket=settings.S3_BUCKET_NAME)
                ErrorHandler.log_success("S3 bucket already exists", settings.S3_BUCKET_NAME)
            except s3.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    # Bucket doesn't exist, create it
                    try:
                        s3.create_bucket(Bucket=settings.S3_BUCKET_NAME)
                        ErrorHandler.log_success("Created S3 bucket", settings.S3_BUCKET_NAME)
                    except s3.exceptions.ClientError as create_error:
                        # Bucket might have been created by another process, or name conflict
                        if create_error.response['Error']['Code'] != 'BucketAlreadyOwnedByYou':
                            raise
                elif error_code == '403':
                    # Access denied - bucket might exist but we don't have permission
                    ErrorHandler.log_success("S3 bucket exists (access verified)", settings.S3_BUCKET_NAME)
                else:
                    raise
            
            # Try to configure bucket policy for public read access (for product images)
            # Note: This may fail if bucket policy is managed elsewhere or permissions don't allow - that's okay
            try:
                bucket_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "PublicReadGetObject",
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:GetObject",
                            "Resource": f"arn:aws:s3:::{settings.S3_BUCKET_NAME}/*"
                        }
                    ]
                }
                s3.put_bucket_policy(
                    Bucket=settings.S3_BUCKET_NAME,
                    Policy=json.dumps(bucket_policy)
                )
                ErrorHandler.log_success("Configured S3 bucket policy for public read", settings.S3_BUCKET_NAME)
            except Exception as policy_error:
                # Policy might already be set or we don't have permission - that's okay
                # The ACL on individual objects will still work if bucket allows it
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Could not set bucket policy (may already be configured or need manual setup): {str(policy_error)}")
                
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "create_bucket", settings.S3_BUCKET_NAME)
    
    @staticmethod
    def upload_image(file, filename):
        """Upload product image to S3 with public read access"""
        try:
            # Upload with public-read ACL so images can be accessed via URL
            s3.upload_fileobj(
                file, 
                settings.S3_BUCKET_NAME, 
                filename,
                ExtraArgs={'ACL': 'public-read', 'ContentType': file.content_type if hasattr(file, 'content_type') else 'image/jpeg'}
            )
            url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
            ErrorHandler.log_success("upload_image", filename)
            return url
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "upload_image", filename)


class SNSService:
    """Service for SNS operations"""
    
    _topic_arn = None
    
    @classmethod
    def get_or_create_topic(cls):
        """Get or create SNS topic for transaction notifications"""
        try:
            if cls._topic_arn:
                return cls._topic_arn
            
            topic_name = 'mypos-transaction-notifications'
            try:
                # Try to find existing topic
                topics = sns.list_topics()
                for topic in topics.get('Topics', []):
                    if topic_name in topic['TopicArn']:
                        cls._topic_arn = topic['TopicArn']
                        return cls._topic_arn
                
                # Create new topic
                response = sns.create_topic(Name=topic_name)
                cls._topic_arn = response['TopicArn']
                ErrorHandler.log_success("Created SNS topic", topic_name)
                return cls._topic_arn
            except Exception as e:
                raise ErrorHandler.handle_aws_error(e, "get_or_create_topic", "SNS")
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "get_or_create_topic", "SNS")
    
    @classmethod
    def send_notification(cls, message, subject="Transaction Notification"):
        """Send transaction notification via SNS"""
        try:
            # Get or create topic
            topic_arn = cls.get_or_create_topic()
            
            if not topic_arn:
                raise Exception("SNS topic ARN is None. Topic may not have been created.")
            
            # Validate message length (SNS has limits)
            if len(message) > 262144:  # 256 KB limit
                message = message[:262000] + "... (truncated)"
            
            # Publish message
            response = sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject[:100]  # Subject has 100 char limit
            )
            
            if 'MessageId' in response:
                ErrorHandler.log_success("send_notification", response['MessageId'])
                return response['MessageId']
            else:
                raise Exception("SNS publish succeeded but no MessageId returned")
                
        except sns.exceptions.ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            
            if error_code == 'NotFound':
                raise Exception(f"SNS topic not found. Please run 'python3 manage.py init_aws' to create the topic. Error: {error_message}")
            elif error_code == 'AuthorizationError' or error_code == 'AccessDenied':
                raise Exception(f"SNS access denied. Check IAM permissions for SNS Publish. Error: {error_message}")
            elif error_code == 'InvalidParameter':
                raise Exception(f"Invalid SNS parameters. Error: {error_message}")
            else:
                raise ErrorHandler.handle_aws_error(e, "send_notification", "SNS")
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "send_notification", "SNS")


class CloudWatchService:
    """Service for CloudWatch metrics"""
    
    @staticmethod
    def put_transaction_metric(amount, transaction_id):
        """Put transaction metric to CloudWatch"""
        try:
            cloudwatch.put_metric_data(
                Namespace='MyPOS/Transactions',
                MetricData=[
                    {
                        'MetricName': 'TransactionAmount',
                        'Value': amount,
                        'Unit': 'None',
                        'Timestamp': datetime.now(),
                        'Dimensions': [
                            {
                                'Name': 'TransactionID',
                                'Value': transaction_id
                            }
                        ]
                    },
                    {
                        'MetricName': 'TransactionCount',
                        'Value': 1,
                        'Unit': 'Count',
                        'Timestamp': datetime.now()
                    }
                ]
            )
            ErrorHandler.log_success("put_transaction_metric", transaction_id)
        except Exception as e:
            raise ErrorHandler.handle_aws_error(e, "put_transaction_metric", "CloudWatch")

