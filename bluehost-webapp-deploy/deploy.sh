#!/bin/bash
# Bluehost Web App Deployment Script
# Usage: ./deploy.sh <project-path> <domain>
# Example: ./deploy.sh /home/yousuf/GoogleDrive/PROJECTS/WEBAPPS/apps/MYAPP myapp.com

set -e

PROJECT_PATH="$1"
DOMAIN="$2"
SSH_KEY="$HOME/.ssh/bluehost_wasibbiz"
SSH_HOST="wasibbiz@162.241.217.198"
BUILD_DIR="/tmp/bluehost-build-$$"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[DEPLOY]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Validate arguments
if [ -z "$PROJECT_PATH" ] || [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <project-path> <domain>"
    echo "Example: $0 /path/to/myapp myapp.com"
    exit 1
fi

if [ ! -d "$PROJECT_PATH" ]; then
    error "Project path does not exist: $PROJECT_PATH"
fi

log "Deploying $PROJECT_PATH to $DOMAIN"

# Step 1: Copy to temp directory
log "Copying project to build directory..."
mkdir -p "$BUILD_DIR"
cp -r "$PROJECT_PATH"/* "$BUILD_DIR/"
cd "$BUILD_DIR"

# Step 2: Install dependencies
log "Installing dependencies..."
npm install

# Step 3: Security check
log "Running security checks..."
if grep -r "GEMINI_API_KEY\|OPENAI_API_KEY\|sk-" src/ 2>/dev/null; then
    warn "Potential API keys found in source. Review before continuing."
    read -p "Continue anyway? (y/N): " confirm
    [ "$confirm" != "y" ] && exit 1
fi

# Step 4: Build
log "Building for production..."
npm run build

# Step 5: Verify build
if [ ! -d "dist" ]; then
    error "Build failed - no dist directory"
fi
log "Build successful: $(du -sh dist | cut -f1)"

# Step 6: Check if addon domain exists
log "Checking addon domain on Bluehost..."
if ! ssh -i "$SSH_KEY" "$SSH_HOST" "test -d ~/$DOMAIN"; then
    log "Creating addon domain..."
    SUBDOMAIN=$(echo "$DOMAIN" | cut -d. -f1)
    ssh -i "$SSH_KEY" "$SSH_HOST" "cpapi2 AddonDomain addaddondomain dir=$DOMAIN newdomain=$DOMAIN subdomain=$SUBDOMAIN"
fi

# Step 7: Upload files
log "Uploading to Bluehost..."
scp -i "$SSH_KEY" -r dist/* "$SSH_HOST:~/$DOMAIN/"

# Step 8: Create .htaccess
log "Setting up .htaccess..."
ssh -i "$SSH_KEY" "$SSH_HOST" "cat > ~/$DOMAIN/.htaccess" << 'HTACCESS'
<IfModule mod_headers.c>
    <FilesMatch "\.(html)$">
        Header set Cache-Control "no-cache, must-revalidate"
    </FilesMatch>
    <FilesMatch "\.(js|css)$">
        Header set Cache-Control "public, max-age=31536000, immutable"
    </FilesMatch>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</IfModule>
HTACCESS

# Step 9: Verify
log "Verifying deployment..."
RESPONSE=$(ssh -i "$SSH_KEY" "$SSH_HOST" "curl -s -o /dev/null -w '%{http_code}' http://$DOMAIN/")
if [ "$RESPONSE" = "200" ]; then
    log "Deployment successful!"
else
    warn "Server returned HTTP $RESPONSE - may need DNS propagation"
fi

# Cleanup
log "Cleaning up build directory..."
rm -rf "$BUILD_DIR"

echo ""
log "Done! Site should be live at: http://$DOMAIN"
log "Note: DNS propagation may take up to 48 hours for new domains"
