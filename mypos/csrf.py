"""
Custom CSRF handling for Cloud9
This middleware bypasses CSRF origin checking for Cloud9 domains
"""

from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings


class Cloud9CsrfViewMiddleware(CsrfViewMiddleware):
    """
    Custom CSRF middleware that allows Cloud9 origins
    """
    
    def process_request(self, request):
        """
        Process request and add Cloud9 origins to trusted origins
        """
        # Get the origin
        origin = request.META.get('HTTP_ORIGIN', '')
        if not origin:
            # Try to get from referer
            referer = request.META.get('HTTP_REFERER', '')
            if referer:
                from urllib.parse import urlparse
                parsed = urlparse(referer)
                origin = f"{parsed.scheme}://{parsed.netloc}"
        
        if origin:
            # Check if it's a Cloud9 origin
            cloud9_patterns = [
                '.vfs.cloud9.',
                '.cloud9.',
                '.c9.',
            ]
            
            is_cloud9 = any(pattern in origin for pattern in cloud9_patterns)
            
            # If it's Cloud9, add to trusted origins
            if is_cloud9 and origin not in settings.CSRF_TRUSTED_ORIGINS:
                # Convert to list, add, and reassign (settings might be immutable tuple)
                trusted = list(settings.CSRF_TRUSTED_ORIGINS)
                trusted.append(origin)
                settings.CSRF_TRUSTED_ORIGINS = trusted
        
        # Continue with normal CSRF processing
        return super().process_request(request)

