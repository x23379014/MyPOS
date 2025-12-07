#!/usr/bin/env python
"""
Quick SNS Test Script
Run this to diagnose SNS notification issues
Usage: python3 test_sns.py
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypos.settings')
django.setup()

from pos.aws_services import SNSService
from error_handler.error_handler import ErrorHandler
import boto3
from django.conf import settings

def test_sns():
    print("=" * 60)
    print("SNS Diagnostic Test")
    print("=" * 60)
    
    # Test 1: Check AWS credentials
    print("\n1. Checking AWS credentials...")
    try:
        sts = boto3.client('sts', region_name=settings.AWS_REGION)
        identity = sts.get_caller_identity()
        print(f"   ✓ AWS credentials valid")
        print(f"   Account: {identity.get('Account', 'N/A')}")
        print(f"   Region: {settings.AWS_REGION}")
    except Exception as e:
        print(f"   ✗ AWS credentials error: {str(e)}")
        print("   → Solution: Refresh your AWS Academy session")
        return
    
    # Test 2: Check SNS access
    print("\n2. Checking SNS access...")
    try:
        sns = boto3.client('sns', region_name=settings.AWS_REGION)
        topics = sns.list_topics()
        print(f"   ✓ SNS access granted")
        print(f"   Found {len(topics.get('Topics', []))} topic(s)")
    except Exception as e:
        print(f"   ✗ SNS access error: {str(e)}")
        print("   → Solution: Check IAM permissions for SNS")
        return
    
    # Test 3: Check for existing topic
    print("\n3. Checking for existing topic...")
    topic_name = 'mypos-transaction-notifications'
    try:
        sns = boto3.client('sns', region_name=settings.AWS_REGION)
        topics = sns.list_topics()
        found = False
        for topic in topics.get('Topics', []):
            topic_arn = topic.get('TopicArn', '')
            if topic_name.lower() in topic_arn.lower():
                print(f"   ✓ Topic found: {topic_arn}")
                found = True
                break
        
        if not found:
            print(f"   ✗ Topic '{topic_name}' not found")
            print("   → Solution: Run 'python3 manage.py init_aws'")
    except Exception as e:
        print(f"   ✗ Error checking topics: {str(e)}")
    
    # Test 4: Try to get or create topic
    print("\n4. Testing get_or_create_topic()...")
    try:
        topic_arn = SNSService.get_or_create_topic()
        if topic_arn:
            print(f"   ✓ Topic ARN: {topic_arn}")
        else:
            print("   ✗ Topic ARN is None")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return
    
    # Test 5: Try to send a test notification
    print("\n5. Testing send_notification()...")
    try:
        test_message = "Test notification from MyPOS diagnostic script"
        message_id = SNSService.send_notification(test_message, "Test Notification")
        if message_id:
            print(f"   ✓ Notification sent successfully!")
            print(f"   Message ID: {message_id}")
        else:
            print("   ✗ Notification failed - no MessageId returned")
    except Exception as e:
        print(f"   ✗ Notification failed: {str(e)}")
        print("\n   Common issues:")
        print("   - Topic doesn't exist: Run 'python3 manage.py init_aws'")
        print("   - Permissions issue: Check IAM permissions")
        print("   - Region mismatch: Check AWS_REGION in settings.py")
        return
    
    print("\n" + "=" * 60)
    print("All tests passed! SNS should be working correctly.")
    print("=" * 60)

if __name__ == '__main__':
    test_sns()

