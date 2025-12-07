# CSRF Error Fix for Cloud9

## Quick Fix

If you're getting CSRF errors in Cloud9, follow these steps:

### Step 1: Update settings.py in Cloud9

1. Open `mypos/settings.py` in Cloud9
2. Find the `CSRF_TRUSTED_ORIGINS` section (around line 27-31)
3. Make sure your Cloud9 URL is in the list:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://1319ddcff73146a496c752c092761686.vfs.cloud9.us-east-1.amazonaws.com',
    # Add your Cloud9 URL here if it's different
]
```

**Important**: Replace the URL above with YOUR actual Cloud9 URL from the error message or browser address bar.

### Step 2: Restart the Django Server

After updating settings.py, you MUST restart the server:

```bash
# Stop the current server (press Ctrl+C in the terminal)
# Then restart:
cd ~/MyPOS
python3 manage.py runserver 0.0.0.0:8080
```

### Step 3: Clear Browser Cache (Optional)

If the error persists:
- Clear your browser cache
- Or use an incognito/private window
- Or hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)

## Finding Your Cloud9 URL

Your Cloud9 URL is shown in:
1. The error message: `Origin checking failed - https://[YOUR-URL] does not match...`
2. Your browser's address bar when viewing the application
3. Cloud9 preview URL

## Alternative: Disable CSRF for Development (NOT RECOMMENDED)

If you absolutely need to disable CSRF for development (NOT for production):

```python
# In mypos/settings.py, add this (ONLY for development):
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Comment this out
    'mypos.csrf.Cloud9CsrfViewMiddleware',  # Use custom middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**WARNING**: Only do this in development. Never disable CSRF in production!

## Still Having Issues?

1. Make sure you've pulled the latest code from GitHub:
   ```bash
   cd ~/MyPOS
   git pull origin main
   ```

2. Verify the URL in settings.py matches your Cloud9 URL exactly

3. Restart the server after making changes

4. Check that `Cloud9CsrfViewMiddleware` is in the MIDDLEWARE list in settings.py

