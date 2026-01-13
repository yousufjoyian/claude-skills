# Bluehost Web App Deployment Skill

Deploy static web applications (React, Vite, vanilla JS) to Bluehost shared hosting with custom domains.

## Prerequisites

- SSH key configured for Bluehost: `~/.ssh/bluehost_wasibbiz`
- SSH command: `ssh -i ~/.ssh/bluehost_wasibbiz wasibbiz@162.241.217.198`
- Domain purchased from registrar (GoDaddy, Namecheap, etc.)

---

## Phase 1: Domain Configuration

### 1.1 Point Domain to Bluehost Nameservers

At your domain registrar (e.g., GoDaddy):

1. Go to Domain Settings → DNS → Nameservers
2. Select "Enter my own nameservers" (or "Custom")
3. **REPLACE** (not add) with:
   ```
   ns1.bluehost.com
   ns2.bluehost.com
   ```
4. Save changes

**Critical**: Remove ALL other nameservers. Having both registrar and Bluehost nameservers causes conflicts.

### 1.2 Disconnect Registrar Services

If the registrar has any connected services (WordPress, Website Builder, Email Hosting):
- Go to Products/Services
- Find services connected to this domain
- **Cancel/Disconnect** them

These services can intercept traffic even when nameservers point elsewhere.

### 1.3 Add Addon Domain in Bluehost

Via SSH:
```bash
ssh -i ~/.ssh/bluehost_wasibbiz wasibbiz@162.241.217.198

# Add the addon domain (creates ~/DOMAIN/ directory)
cpapi2 AddonDomain addaddondomain dir=DOMAIN.TLD newdomain=DOMAIN.TLD subdomain=DOMAIN
```

Example:
```bash
cpapi2 AddonDomain addaddondomain dir=ilm.kids newdomain=ilm.kids subdomain=ilm
```

Verify:
```bash
ls -la ~/DOMAIN.TLD/
```

---

## Phase 2: Build the Application

### 2.1 Prepare Build Environment

**Important**: Don't build in Google Drive synced folders - node_modules causes sync issues.

```bash
# Copy project to /tmp for building
cp -r /path/to/project /tmp/project-build
cd /tmp/project-build

# Install dependencies
npm install

# Build for production
npm run build
```

### 2.2 Common Build Issues

| Issue | Solution |
|-------|----------|
| Invalid package name (special chars) | Edit package.json, use alphanumeric + hyphens only |
| npm install hangs | Build in /tmp, not synced folders |
| Missing dependencies | Check package.json, run `npm install` again |

### 2.3 Security Audit Before Deploy

Before deploying, check for exposed secrets:

```bash
# Search for API keys, secrets, tokens
grep -r "API_KEY\|SECRET\|TOKEN\|PASSWORD" dist/
grep -r "sk-\|pk_\|GEMINI\|OPENAI" dist/

# Check for .env files (should NOT be in dist)
ls -la dist/.env*
```

**Remove/disable**:
- API key imports and usage in source code
- SDK imports that aren't needed client-side
- .env files from deployment

---

## Phase 3: Deploy to Bluehost

### 3.1 Upload Built Files

```bash
# Upload dist/ contents to domain folder
scp -i ~/.ssh/bluehost_wasibbiz -r /tmp/project-build/dist/* wasibbiz@162.241.217.198:~/DOMAIN.TLD/
```

### 3.2 Create .htaccess for Security & Caching

```bash
ssh -i ~/.ssh/bluehost_wasibbiz wasibbiz@162.241.217.198

cat > ~/DOMAIN.TLD/.htaccess << 'EOF'
# Cache control for static assets
<IfModule mod_headers.c>
    # Force revalidation for HTML
    <FilesMatch "\.(html)$">
        Header set Cache-Control "no-cache, must-revalidate"
    </FilesMatch>

    # Cache JS/CSS with long expiry (files have hash in name)
    <FilesMatch "\.(js|css)$">
        Header set Cache-Control "public, max-age=31536000, immutable"
    </FilesMatch>
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Enable CORS for fonts
<FilesMatch "\.(ttf|otf|eot|woff|woff2)$">
    <IfModule mod_headers.c>
        Header set Access-Control-Allow-Origin "*"
    </IfModule>
</FilesMatch>

# SPA routing fallback (for React Router, Vue Router, etc.)
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</IfModule>
EOF
```

### 3.3 Verify Deployment

```bash
# Check files are in place
ls -la ~/DOMAIN.TLD/

# Test from server
curl -s http://DOMAIN.TLD/ | head -20
```

---

## Phase 4: DNS Propagation & Troubleshooting

### 4.1 DNS Propagation Timeline

- **Nameserver changes**: 24-48 hours (often faster)
- **A record changes**: 1-4 hours typical
- **TTL**: Check current TTL; can't speed up until it expires

### 4.2 Diagnostic Commands

```bash
# Check DNS resolution
ping DOMAIN.TLD

# Check what IP the domain resolves to
nslookup DOMAIN.TLD

# Check nameservers
dig NS DOMAIN.TLD

# Test what Bluehost actually serves (bypasses browser cache)
curl -s http://DOMAIN.TLD/

# Check with specific DNS server
nslookup DOMAIN.TLD 8.8.8.8
```

### 4.3 Common Issues & Solutions

| Symptom | Cause | Solution |
|---------|-------|----------|
| Old page shows in browser | Browser cache | Hard refresh: Ctrl+Shift+R or Cmd+Shift+R |
| Registrar parking page | Connected services | Disconnect WordPress/Website Builder at registrar |
| Ping shows wrong IP | DNS not propagated | Wait; check nameservers are correct |
| Ping correct but wrong page | Browser/ISP cache | Try different browser, clear cache, wait |
| 404 errors | Wrong directory | Verify files in ~/DOMAIN.TLD/ |
| Blank page | Build error | Check browser console, verify index.html |

### 4.4 Force Browser Cache Clear

Tell users to:
1. Hard refresh: `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
2. Clear browser cache completely
3. Try incognito/private window
4. Try different browser

---

## Quick Reference Commands

```bash
# SSH to Bluehost
ssh -i ~/.ssh/bluehost_wasibbiz wasibbiz@162.241.217.198

# Add addon domain
cpapi2 AddonDomain addaddondomain dir=DOMAIN newdomain=DOMAIN subdomain=SUBDOMAIN

# List addon domains
cpapi2 AddonDomain listaddondomains

# Upload files
scp -i ~/.ssh/bluehost_wasibbiz -r /tmp/build/dist/* wasibbiz@162.241.217.198:~/DOMAIN/

# Test site from server
curl -s http://DOMAIN/ | head -20

# Check disk usage
du -sh ~/DOMAIN/
```

---

## Checklist for New Deployments

- [ ] Domain purchased
- [ ] Nameservers changed to ns1/ns2.bluehost.com
- [ ] Registrar services (WordPress, etc.) disconnected
- [ ] Addon domain created on Bluehost
- [ ] Project copied to /tmp for building
- [ ] npm install completed
- [ ] Security audit: no API keys in build
- [ ] npm run build completed
- [ ] Files uploaded to ~/DOMAIN/
- [ ] .htaccess created with security headers
- [ ] curl test shows correct content
- [ ] Browser test (with cache clear) works
