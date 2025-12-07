"""
Models for MyPOS - Simple Product model for local storage
Customer and Transaction data stored in DynamoDB
"""

from django.db import models


class Product(models.Model):
    """Product model - stored locally, image in S3"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    s3_image_url = models.URLField(blank=True, null=True)  # URL of image in S3
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

