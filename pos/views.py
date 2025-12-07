"""
Views for MyPOS - CRUD operations for Products, Customers, and Transactions
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Product
from .aws_services import DynamoDBService, S3Service, SNSService, CloudWatchService
from error_handler.error_handler import ErrorHandler, POSError
import uuid
import json


def home(request):
    """Home page"""
    return render(request, 'home.html')


def product_list(request):
    """List all products"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/list.html', {'products': products})


def product_add(request):
    """Add new product"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity', 0)
            
            # Validation
            if not name or not price:
                raise ErrorHandler.handle_validation_error("Name and price are required", "product")
            
            # Create product
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                quantity=int(quantity) if quantity else 0
            )
            
            # Handle image upload to S3
            if 'image' in request.FILES:
                try:
                    S3Service.create_bucket()
                    file = request.FILES['image']
                    filename = f"products/{product.id}/{file.name}"
                    s3_url = S3Service.upload_image(file, filename)
                    product.s3_image_url = s3_url
                    product.save()
                except Exception as e:
                    ErrorHandler.handle_aws_error(e, "upload_product_image", filename)
                    messages.warning(request, f"Product created but image upload failed: {str(e)}")
            
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
            
        except POSError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Error adding product: {str(e)}")
    
    return render(request, 'products/add.html')


def product_edit(request, product_id):
    """Edit product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        try:
            product.name = request.POST.get('name')
            product.description = request.POST.get('description', '')
            product.price = request.POST.get('price')
            product.quantity = int(request.POST.get('quantity', 0))
            
            # Handle image upload to S3
            if 'image' in request.FILES:
                try:
                    S3Service.create_bucket()
                    file = request.FILES['image']
                    filename = f"products/{product.id}/{file.name}"
                    s3_url = S3Service.upload_image(file, filename)
                    product.s3_image_url = s3_url
                except Exception as e:
                    ErrorHandler.handle_aws_error(e, "upload_product_image", filename)
                    messages.warning(request, f"Product updated but image upload failed: {str(e)}")
            
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
            
        except Exception as e:
            messages.error(request, f"Error updating product: {str(e)}")
    
    return render(request, 'products/edit.html', {'product': product})


def product_delete(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'products/delete.html', {'product': product})


def customer_list(request):
    """List all customers from DynamoDB"""
    try:
        DynamoDBService.create_tables()
        customers = DynamoDBService.list_customers()
    except POSError as e:
        messages.error(request, str(e))
        customers = []
    except Exception as e:
        messages.error(request, f"Error loading customers: {str(e)}")
        customers = []
    
    return render(request, 'customers/list.html', {'customers': customers})


def customer_add(request):
    """Add new customer to DynamoDB"""
    if request.method == 'POST':
        try:
            DynamoDBService.create_tables()
            
            customer_data = {
                'customer_id': str(uuid.uuid4()),
                'name': request.POST.get('name'),
                'email': request.POST.get('email', ''),
                'phone': request.POST.get('phone', ''),
                'address': request.POST.get('address', '')
            }
            
            # Validation
            if not customer_data['name']:
                raise ErrorHandler.handle_validation_error("Name is required", "customer")
            
            DynamoDBService.add_customer(customer_data)
            messages.success(request, 'Customer added successfully!')
            return redirect('customer_list')
            
        except POSError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Error adding customer: {str(e)}")
    
    return render(request, 'customers/add.html')


def customer_edit(request, customer_id):
    """Edit customer in DynamoDB"""
    try:
        DynamoDBService.create_tables()
        customer = DynamoDBService.get_customer(customer_id)
        
        if not customer:
            messages.error(request, 'Customer not found!')
            return redirect('customer_list')
        
        if request.method == 'POST':
            try:
                customer_data = {
                    'name': request.POST.get('name'),
                    'email': request.POST.get('email', ''),
                    'phone': request.POST.get('phone', ''),
                    'address': request.POST.get('address', '')
                }
                
                if not customer_data['name']:
                    raise ErrorHandler.handle_validation_error("Name is required", "customer")
                
                DynamoDBService.update_customer(customer_id, customer_data)
                messages.success(request, 'Customer updated successfully!')
                return redirect('customer_list')
                
            except POSError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Error updating customer: {str(e)}")
        
        return render(request, 'customers/edit.html', {'customer': customer})
        
    except POSError as e:
        messages.error(request, str(e))
        return redirect('customer_list')
    except Exception as e:
        messages.error(request, f"Error loading customer: {str(e)}")
        return redirect('customer_list')


def customer_delete(request, customer_id):
    """Delete customer from DynamoDB"""
    try:
        DynamoDBService.create_tables()
        customer = DynamoDBService.get_customer(customer_id)
        
        if not customer:
            messages.error(request, 'Customer not found!')
            return redirect('customer_list')
        
        if request.method == 'POST':
            try:
                DynamoDBService.delete_customer(customer_id)
                messages.success(request, 'Customer deleted successfully!')
                return redirect('customer_list')
            except POSError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Error deleting customer: {str(e)}")
        
        return render(request, 'customers/delete.html', {'customer': customer})
        
    except POSError as e:
        messages.error(request, str(e))
        return redirect('customer_list')
    except Exception as e:
        messages.error(request, f"Error loading customer: {str(e)}")
        return redirect('customer_list')


def transaction_list(request):
    """List all transactions from DynamoDB"""
    try:
        DynamoDBService.create_tables()
        transactions = DynamoDBService.list_transactions()
        
        # Get customer names for each transaction
        for transaction in transactions:
            try:
                customer = DynamoDBService.get_customer(transaction['customer_id'])
                transaction['customer_name'] = customer['name'] if customer else 'Unknown'
            except:
                transaction['customer_name'] = 'Unknown'
                
    except POSError as e:
        messages.error(request, str(e))
        transactions = []
    except Exception as e:
        messages.error(request, f"Error loading transactions: {str(e)}")
        transactions = []
    
    return render(request, 'transactions/list.html', {'transactions': transactions})


def transaction_add(request):
    """Add new transaction to DynamoDB"""
    try:
        DynamoDBService.create_tables()
        S3Service.create_bucket()
        
        # Get products and customers for the form
        products = Product.objects.all()
        customers = DynamoDBService.list_customers()
        
        if request.method == 'POST':
            try:
                customer_id = request.POST.get('customer_id')
                product_ids = request.POST.getlist('product_ids')
                quantities = request.POST.getlist('quantities')
                
                if not customer_id or not product_ids:
                    raise ErrorHandler.handle_validation_error("Customer and at least one product are required", "transaction")
                
                # Build products list
                transaction_products = []
                total_amount = 0.0
                
                for i, product_id in enumerate(product_ids):
                    try:
                        product = Product.objects.get(id=product_id)
                        quantity = int(quantities[i]) if i < len(quantities) and quantities[i] else 1
                        subtotal = float(product.price) * quantity
                        total_amount += subtotal
                        
                        transaction_products.append({
                            'product_id': str(product.id),
                            'product_name': product.name,
                            'quantity': quantity,
                            'price': float(product.price),
                            'subtotal': subtotal
                        })
                    except Product.DoesNotExist:
                        continue
                
                if not transaction_products:
                    raise ErrorHandler.handle_validation_error("No valid products selected", "transaction")
                
                # Create transaction
                transaction_id = str(uuid.uuid4())
                transaction_data = {
                    'transaction_id': transaction_id,
                    'customer_id': customer_id,
                    'products': transaction_products,
                    'total_amount': total_amount,
                    'status': 'completed'
                }
                
                DynamoDBService.add_transaction(transaction_data)
                
                # Send SNS notification
                try:
                    customer = DynamoDBService.get_customer(customer_id)
                    customer_name = customer['name'] if customer else 'Customer'
                    notification_message = f"""
Transaction Completed!

Transaction ID: {transaction_id}
Customer: {customer_name}
Total Amount: ${total_amount:.2f}
Products: {len(transaction_products)} items

Thank you for your purchase!
                    """
                    SNSService.send_notification(notification_message.strip(), "New Transaction - MyPOS")
                except Exception as e:
                    ErrorHandler.handle_aws_error(e, "send_transaction_notification", "SNS")
                    messages.warning(request, "Transaction created but notification failed")
                
                # Send CloudWatch metrics
                try:
                    CloudWatchService.put_transaction_metric(total_amount, transaction_id)
                except Exception as e:
                    ErrorHandler.handle_aws_error(e, "put_transaction_metric", "CloudWatch")
                    messages.warning(request, "Transaction created but metrics failed")
                
                messages.success(request, f'Transaction created successfully! Transaction ID: {transaction_id}')
                return redirect('transaction_list')
                
            except POSError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Error creating transaction: {str(e)}")
        
        return render(request, 'transactions/add.html', {
            'products': products,
            'customers': customers
        })
        
    except POSError as e:
        messages.error(request, str(e))
        return render(request, 'transactions/add.html', {'products': [], 'customers': []})
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return render(request, 'transactions/add.html', {'products': [], 'customers': []})


def transaction_view(request, transaction_id):
    """View transaction details"""
    try:
        DynamoDBService.create_tables()
        transaction = DynamoDBService.get_transaction(transaction_id)
        
        if not transaction:
            messages.error(request, 'Transaction not found!')
            return redirect('transaction_list')
        
        # Get customer details
        try:
            customer = DynamoDBService.get_customer(transaction['customer_id'])
            transaction['customer'] = customer
        except:
            transaction['customer'] = None
        
        return render(request, 'transactions/view.html', {'transaction': transaction})
        
    except POSError as e:
        messages.error(request, str(e))
        return redirect('transaction_list')
    except Exception as e:
        messages.error(request, f"Error loading transaction: {str(e)}")
        return redirect('transaction_list')

