"""
Cloud9 CSRF Middleware
Automatically allows Cloud9 origins for CSRF verification
"""

from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token
from django.conf import settings


class Cloud9CsrfMiddleware(MiddlewareMixin):
    """
    Custom middleware that automatically adds Cloud9 origins to CSRF_TRUSTED_ORIGINS
    This runs before CSRF middleware to ensure Cloud9 origins are trusted
    """
    
    def process_request(self, request):
        # Check if request is from Cloud9
        origin = request.META.get('HTTP_ORIGIN', '')
        referer = request.META.get('HTTP_REFERER', '')
        host = request.META.get('HTTP_HOST', '')
        
        # Cloud9 URL patterns
        cloud9_patterns = [
            '.vfs.cloud9.',
            '.cloud9.',
            '.c9.',
        ]
        
        # Check if origin, referer, or host matches Cloud9 pattern
        is_cloud9 = False
        cloud9_origin = None
        
        # Check origin header
        if origin:
            is_cloud9 = any(pattern in origin for pattern in cloud9_patterns)
            if is_cloud9:
                cloud9_origin = origin
        
        # Check referer if no origin
        if not cloud9_origin and referer:
            if any(pattern in referer for pattern in cloud9_patterns):
                from urllib.parse import urlparse
                parsed = urlparse(referer)
                cloud9_origin = f"{parsed.scheme}://{parsed.netloc}"
                is_cloud9 = True
        
        # Check host header as fallback
        if not cloud9_origin and host:
            if any(pattern in host for pattern in cloud9_patterns):
                # Construct origin from host
                scheme = 'https' if request.is_secure() else 'http'
                cloud9_origin = f"{scheme}://{host}"
                is_cloud9 = True
        
        # Add to trusted origins if it's a Cloud9 origin and not already there
        if is_cloud9 and cloud9_origin:
            # Use a mutable list to modify trusted origins
            trusted_origins = list(settings.CSRF_TRUSTED_ORIGINS)
            if cloud9_origin not in trusted_origins:
                trusted_origins.append(cloud9_origin)
                # Update settings (this should work for the current request)
                settings.CSRF_TRUSTED_ORIGINS = trusted_origins
        
        return None  # Continue processing

