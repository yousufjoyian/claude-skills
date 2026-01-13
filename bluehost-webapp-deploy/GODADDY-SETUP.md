# GoDaddy to Bluehost Domain Setup

Step-by-step guide for pointing a GoDaddy domain to Bluehost hosting.

## Step 1: Change Nameservers in GoDaddy

1. Log into GoDaddy
2. Go to **My Products** → find your domain
3. Click **DNS** or **Manage DNS**
4. Scroll to **Nameservers** section
5. Click **Change** or **Edit**
6. Select **"Enter my own nameservers (advanced)"**
7. Enter:
   ```
   ns1.bluehost.com
   ns2.bluehost.com
   ```
8. **Delete** any other nameservers (ns27.domaincontrol.com, etc.)
9. Save

## Step 2: Disconnect GoDaddy Services

**Critical**: Connected services interfere even with correct nameservers.

1. Go to **My Products**
2. Look for these products connected to your domain:
   - WordPress Hosting
   - Website Builder
   - Professional Email
   - SSL Certificate (GoDaddy-issued)
3. For each connected service:
   - Click on it
   - Find **Cancel** or **Remove** or **Disconnect**
   - Confirm cancellation

**Symptom if not done**: Domain resolves to correct IP, but browser shows GoDaddy parking page or "Nurturing Young Minds" placeholder.

## Step 3: Verify Changes

Wait 5-10 minutes, then check:

```bash
# Check nameservers
nslookup -type=NS yourdomain.com

# Should show:
# nameserver = ns1.bluehost.com
# nameserver = ns2.bluehost.com
```

If still showing domaincontrol.com nameservers, changes haven't propagated yet.

## Step 4: Add Domain on Bluehost

See main SKILL.md for Bluehost addon domain setup.

## Common GoDaddy Issues

| Issue | Solution |
|-------|----------|
| Can't delete old nameservers | Select "Enter my own nameservers" first, then clear all and add Bluehost NS |
| "DNS managed by GoDaddy" message | You're in wrong section; go to Nameservers, not DNS Records |
| WordPress service won't cancel | May need to wait for billing cycle; contact GoDaddy support |
| Domain shows as "pending" | Normal during nameserver change; wait 24-48h |
| A records still visible | Ignored once nameservers point elsewhere; don't need to delete |

## DNS Propagation Timeline

- **Nameserver change**: 24-48 hours (often 1-4 hours)
- **First-time setup**: Usually slower than updates
- **Check propagation**: https://www.whatsmydns.net/

## Parking Page Still Showing?

If the GoDaddy parking page ("Nurturing Young Minds", contact form, "Protect your domain") still shows:

1. **Verify nameservers** are set correctly (only ns1/ns2.bluehost.com)
2. **Disconnect all GoDaddy services** for this domain
3. **Clear browser cache** completely (or use different browser)
4. **Wait** - ISP DNS cache may take hours to update
5. **Test with curl** to bypass browser cache:
   ```bash
   curl -I http://yourdomain.com
   # Should show Bluehost server headers
   ```
