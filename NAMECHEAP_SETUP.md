# Namecheap Domain Setup for PythonAnywhere

## Step-by-Step Guide (Updated for PythonAnywhere CNAME Method)

### 1. PythonAnywhere Web App Setup (Do This First)

1. **Log into PythonAnywhere**
2. **Go to "Web" tab**
3. **Click "Add a new web app"**
4. **Choose "Manual configuration"**
5. **Select Python 3.9 or 3.10**
6. **In the domain field, enter:** `www.yourdomain.com` (not just yourdomain.com)
7. **Complete the web app setup**

### 2. Get Your PythonAnywhere CNAME Value

1. **In PythonAnywhere "Web" tab**
2. **Find your web app**
3. **Look for the CNAME value** (it will be something like `webapp-XXXX.pythonanywhere.com`)
4. **Copy this value** - you'll need it for Namecheap

### 3. Namecheap DNS Configuration

1. **Log into your Namecheap account**
2. **Go to "Domain List"**
3. **Click "Manage" next to your domain**
4. **Go to "Advanced DNS" tab**
5. **Add a CNAME record:**

```
Type: CNAME Record
Host: www
Value: webapp-XXXX.pythonanywhere.com (your actual value from PythonAnywhere)
TTL: 30
```

**Important Notes:**
- Use `www` as the Host (not @)
- The Value should be your PythonAnywhere CNAME (like `webapp-1234.pythonanywhere.com`)
- Do NOT use A records - PythonAnywhere recommends CNAME for better reliability

### 4. Wait for DNS Propagation

- **Can take 24-48 hours** for DNS changes to propagate
- **You can check propagation** using:
  - [whatsmydns.net](https://whatsmydns.net)
  - [dnschecker.org](https://dnschecker.org)

### 5. SSL Certificate Setup

1. **Wait for DNS propagation** (check PythonAnywhere "Web" tab for warnings)
2. **In PythonAnywhere "Web" tab**
3. **Click "Add security"**
4. **Choose "Let's Encrypt"**
5. **Enter your domain:** `www.yourdomain.com`
6. **Follow the prompts**

### 6. Optional: Naked Domain Redirect

If you want `yourdomain.com` to redirect to `www.yourdomain.com`:

1. **In Namecheap Advanced DNS**
2. **Add URL Redirect Record:**

```
Type: URL Redirect Record
Host: @
Value: http://www.yourdomain.com
TTL: 30
```

### 7. Testing Your Domain

Once DNS has propagated:

1. **Visit:** `https://www.yourdomain.com`
2. **Test upload page:** `https://www.yourdomain.com/upload`
3. **Test admin page:** `https://www.yourdomain.com/admin`

### Troubleshooting

#### CNAME Not Working?

1. **Check PythonAnywhere "Web" tab** for warnings
2. **Verify CNAME value** matches exactly
3. **Wait longer** for DNS propagation
4. **Use CNAME lookup tool:** [whatsmydns.net](https://whatsmydns.net)

#### SSL Certificate Issues?

1. **Wait 24 hours** after adding domain
2. **Ensure domain is accessible** before requesting SSL
3. **Check PythonAnywhere logs** for errors

#### Common Issues:

- **Domain shows parking page:** DNS hasn't propagated yet
- **SSL certificate fails:** Domain not properly configured
- **Site not loading:** Check PythonAnywhere web app is running

### Quick Commands

```bash
# Check if domain resolves
ping www.yourdomain.com

# Check CNAME records
nslookup www.yourdomain.com

# Test HTTPS
curl -I https://www.yourdomain.com
```

### Support Resources

- **PythonAnywhere Help:** [help.pythonanywhere.com](https://help.pythonanywhere.com)
- **Namecheap Support:** [support.namecheap.com](https://support.namecheap.com)
- **DNS Propagation Checker:** [whatsmydns.net](https://whatsmydns.net)
- **CNAME Lookup Tool:** [whatsmydns.net](https://whatsmydns.net)

### Important Notes

- ✅ **Use CNAME, not A records** (PythonAnywhere recommendation)
- ✅ **Include www in domain** (www.yourdomain.com, not yourdomain.com)
- ✅ **Wait for DNS propagation** before setting up SSL
- ✅ **Check PythonAnywhere "Web" tab** for warnings about CNAME 