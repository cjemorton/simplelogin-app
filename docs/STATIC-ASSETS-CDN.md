# Static Asset Configuration Guide

This guide explains how to configure SimpleLogin to serve static assets from a CDN or external storage.

## Overview

Static assets (CSS, JS, images) can be served from:
1. **Local** - Served directly from the application container (default)
2. **CDN** - Served from a Content Delivery Network (e.g., Cloudflare, CloudFront)
3. **Object Storage** - Served from cloud storage (e.g., S3, GCS, Azure Blob)

## Benefits of External Static Hosting

- **Performance**: Assets served from edge locations closer to users
- **Reduced Load**: Application servers don't serve static files
- **Caching**: Better caching strategies and cache invalidation
- **Cost**: Cheaper bandwidth for static content
- **Scalability**: CDN handles traffic spikes

## Configuration

### Environment Variables

Add these to your `.env` file or environment configuration:

```bash
# Static asset serving mode: 'local', 'cdn', or 's3'
STATIC_ASSET_MODE=local

# Base URL for static assets (used when STATIC_ASSET_MODE != 'local')
# Examples:
# - CDN: https://cdn.yourdomain.com/static
# - S3: https://yourbucket.s3.amazonaws.com/static
# - Cloudflare Pages: https://your-project.pages.dev/static
STATIC_URL=

# For S3/object storage
AWS_S3_BUCKET=
AWS_S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# For Cloudflare
CLOUDFLARE_ACCOUNT_ID=
CLOUDFLARE_PROJECT_NAME=
```

### Application Configuration

Update `app/config.py` to use the configuration:

```python
import os

# Static asset configuration
STATIC_ASSET_MODE = os.environ.get("STATIC_ASSET_MODE", "local")
STATIC_URL = os.environ.get("STATIC_URL", "/static")

# Ensure STATIC_URL has no trailing slash
STATIC_URL = STATIC_URL.rstrip("/")
```

## Deployment Options

### Option 1: Cloudflare Pages (Recommended for Simplicity)

**Pros:**
- Free tier available
- Automatic SSL
- Global CDN
- Simple deployment

**Setup:**

1. **Create a Cloudflare Pages project**
   ```bash
   # From /static directory
   npm run build  # if you have a build step
   ```

2. **Deploy**
   - Connect GitHub repository
   - Set build directory to `/static`
   - Cloudflare auto-deploys on push

3. **Configure SimpleLogin**
   ```bash
   STATIC_ASSET_MODE=cdn
   STATIC_URL=https://your-project.pages.dev
   ```

### Option 2: AWS S3 + CloudFront

**Pros:**
- Full control
- Integrates with AWS infrastructure
- Highly scalable

**Setup:**

1. **Create S3 bucket**
   ```bash
   aws s3 mb s3://simplelogin-static
   aws s3api put-bucket-policy --bucket simplelogin-static --policy file://bucket-policy.json
   ```

2. **Upload static assets**
   ```bash
   aws s3 sync ./static/ s3://simplelogin-static/static/ \
     --acl public-read \
     --cache-control "public, max-age=31536000"
   ```

3. **Create CloudFront distribution**
   - Origin: S3 bucket
   - Enable compression
   - Set cache policies

4. **Configure SimpleLogin**
   ```bash
   STATIC_ASSET_MODE=s3
   STATIC_URL=https://d123456789.cloudfront.net/static
   AWS_S3_BUCKET=simplelogin-static
   ```

### Option 3: Self-hosted CDN (e.g., Nginx)

**Pros:**
- Full control
- No external dependencies
- Good for on-premise deployments

**Setup:**

1. **Configure Nginx as reverse proxy**
   ```nginx
   # /etc/nginx/sites-available/simplelogin-static
   server {
       listen 80;
       server_name static.yourdomain.com;
       
       root /var/www/simplelogin/static;
       
       location / {
           expires 1y;
           add_header Cache-Control "public, immutable";
           add_header X-Content-Type-Options "nosniff";
       }
       
       # Enable compression
       gzip on;
       gzip_types text/css application/javascript image/svg+xml;
   }
   ```

2. **Configure SimpleLogin**
   ```bash
   STATIC_ASSET_MODE=cdn
   STATIC_URL=https://static.yourdomain.com
   ```

## Implementation in Templates

### Update Jinja2 Templates

Replace hardcoded `/static/` paths with the `STATIC_URL` variable:

**Before:**
```jinja2
<link rel="stylesheet" href="/static/style.css">
<script src="/static/js/app.js"></script>
<img src="/static/logo.png">
```

**After:**
```jinja2
<link rel="stylesheet" href="{{ config.STATIC_URL }}/style.css">
<script src="{{ config.STATIC_URL }}/js/app.js"></script>
<img src="{{ config.STATIC_URL }}/logo.png">
```

Or use Flask's `url_for()` with CDN support:

```jinja2
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### Flask Configuration for `url_for()`

Update Flask to use external static URL:

```python
# app/__init__.py
from flask import Flask

app = Flask(__name__)

# Configure static URL
if config.STATIC_ASSET_MODE != 'local':
    app.config['STATIC_URL'] = config.STATIC_URL
else:
    app.config['STATIC_URL'] = '/static'
```

## Deployment Script

Create a script to deploy static assets:

```bash
#!/usr/bin/env bash
# scripts/deploy-static.sh

set -e

MODE="${STATIC_ASSET_MODE:-local}"

if [ "$MODE" = "s3" ]; then
    echo "Deploying static assets to S3..."
    aws s3 sync ./static/ "s3://${AWS_S3_BUCKET}/static/" \
        --delete \
        --acl public-read \
        --cache-control "public, max-age=31536000" \
        --exclude "*.md" \
        --exclude "package*.json"
    
    echo "Invalidating CloudFront cache..."
    aws cloudfront create-invalidation \
        --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" \
        --paths "/static/*"

elif [ "$MODE" = "cdn" ]; then
    echo "Deploying to Cloudflare Pages..."
    cd static
    npx wrangler pages publish . \
        --project-name="$CLOUDFLARE_PROJECT_NAME" \
        --branch=main

else
    echo "Static assets will be served locally (no deployment needed)"
fi
```

## Cache Busting

### Using Asset Versioning

Add version/hash to filenames:

```python
# app/static_helpers.py
import hashlib
import os

def asset_url(filename):
    """Generate versioned asset URL"""
    if config.STATIC_ASSET_MODE == 'local':
        # Use file hash for cache busting
        filepath = os.path.join(app.static_folder, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()[:8]
            return f"{config.STATIC_URL}/{filename}?v={file_hash}"
    
    # For CDN, use app version
    return f"{config.STATIC_URL}/{filename}?v={config.VERSION}"
```

### Using Query Parameters

```jinja2
<link rel="stylesheet" href="{{ config.STATIC_URL }}/style.css?v={{ config.VERSION }}">
```

## Testing

### Local Testing

```bash
# Test with local assets
STATIC_ASSET_MODE=local docker-compose up

# Test with CDN (mock)
STATIC_ASSET_MODE=cdn STATIC_URL=https://cdn.example.com docker-compose up
```

### Verify Assets Load

```bash
# Check if assets load from CDN
curl -I https://cdn.yourdomain.com/static/style.css

# Should return:
# HTTP/2 200
# cache-control: public, max-age=31536000
# x-cache: Hit from cloudfront
```

## Migration Checklist

- [ ] Choose CDN/storage provider
- [ ] Set up CDN/storage account
- [ ] Update environment variables
- [ ] Update templates to use `STATIC_URL` or `url_for()`
- [ ] Deploy static assets to CDN
- [ ] Test asset loading in staging
- [ ] Update DNS if needed (CNAME for static subdomain)
- [ ] Enable SSL for static domain
- [ ] Monitor CDN metrics
- [ ] Set up cache invalidation workflow

## Security Considerations

1. **CORS Headers**: If serving from different domain
   ```nginx
   add_header Access-Control-Allow-Origin "https://app.yourdomain.com";
   ```

2. **Content Security Policy**: Update CSP headers
   ```python
   CSP_STATIC_DOMAINS = ['static.yourdomain.com', 'cdn.cloudflare.com']
   ```

3. **Subresource Integrity (SRI)**: For critical assets
   ```html
   <script src="https://cdn.yourdomain.com/app.js"
           integrity="sha384-..."
           crossorigin="anonymous"></script>
   ```

## Performance Monitoring

Track CDN performance:

```python
# Add to monitoring
cdn_metrics = {
    'cache_hit_rate': ...,
    'bandwidth_saved': ...,
    'avg_response_time': ...,
}
```

## Rollback

If issues occur:

```bash
# Switch back to local serving
STATIC_ASSET_MODE=local
# Restart application
docker-compose restart app
```

## Cost Estimation

### Cloudflare Pages (Free Tier)
- Bandwidth: Unlimited
- Builds: 500/month
- Cost: $0

### AWS S3 + CloudFront
- S3 storage: ~$0.02/GB/month
- CloudFront data transfer: $0.085/GB (first 10 TB)
- Requests: Minimal cost
- **Estimated**: $5-20/month for small-medium deployments

### Self-hosted
- Server cost: Existing infrastructure
- Bandwidth: Depends on provider
- **Estimated**: Minimal incremental cost

## See Also

- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [AWS S3 Static Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Flask Static Files](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/)
