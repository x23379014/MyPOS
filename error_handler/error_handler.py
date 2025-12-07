"""
Custom Error Handling Library for MyPOS
Simple error handling for AWS services and POS operations
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class POSError(Exception):
    """Custom exception for POS operations"""
    
    def __init__(self, message: str, error_type: str = "GENERAL", details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)
    
    def __str__(self):
        return f"[{self.error_type}] {self.message} at {self.timestamp}"


class ErrorHandler:
    """Simple error handler for AWS services and POS operations"""
    
    @staticmethod
    def handle_aws_error(error: Exception, operation: str, resource: str = "") -> POSError:
        """
        Handle AWS service errors and convert to POSError
        
        Args:
            error: The original exception
            operation: What operation was being performed
            resource: Which resource was involved
            
        Returns:
            POSError: Custom error with details
        """
        error_message = str(error)
        error_type = "AWS_ERROR"
        
        # Determine error type based on error message
        if "NoCredentialsError" in error_message or "Credentials" in error_message:
            error_type = "AWS_CREDENTIALS_ERROR"
            message = f"AWS credentials not found. Please check your AWS Academy credentials."
        elif "ResourceNotFoundException" in error_message or "does not exist" in error_message:
            error_type = "AWS_RESOURCE_NOT_FOUND"
            message = f"AWS resource not found: {resource}"
        elif "AccessDenied" in error_message or "Forbidden" in error_message:
            error_type = "AWS_ACCESS_DENIED"
            message = f"Access denied to AWS resource: {resource}"
        else:
            message = f"Error during {operation}: {error_message}"
        
        details = {
            "operation": operation,
            "resource": resource,
            "original_error": error_message
        }
        
        pos_error = POSError(message, error_type, details)
        logger.error(f"POS Error: {pos_error}")
        
        return pos_error
    
    @staticmethod
    def handle_validation_error(message: str, field: str = "") -> POSError:
        """
        Handle validation errors
        
        Args:
            message: Error message
            field: Field that failed validation
            
        Returns:
            POSError: Custom error
        """
        details = {"field": field} if field else {}
        pos_error = POSError(message, "VALIDATION_ERROR", details)
        logger.warning(f"Validation Error: {pos_error}")
        return pos_error
    
    @staticmethod
    def handle_database_error(error: Exception, operation: str) -> POSError:
        """
        Handle database operation errors
        
        Args:
            error: The original exception
            operation: Database operation being performed
            
        Returns:
            POSError: Custom error
        """
        message = f"Database error during {operation}: {str(error)}"
        details = {
            "operation": operation,
            "original_error": str(error)
        }
        pos_error = POSError(message, "DATABASE_ERROR", details)
        logger.error(f"Database Error: {pos_error}")
        return pos_error
    
    @staticmethod
    def log_success(operation: str, resource: str = ""):
        """
        Log successful operations
        
        Args:
            operation: Operation that succeeded
            resource: Resource involved
        """
        message = f"Successfully completed: {operation}"
        if resource:
            message += f" on {resource}"
        logger.info(message)

