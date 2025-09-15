# DigitalOcean App Platform Deployment Guide

## 🚀 Deploy AI Code Assessment System to DigitalOcean

DigitalOcean App Platform is reliable, easy to use, and has excellent FastAPI support. No complex configuration needed!

### Prerequisites
- GitHub account
- DigitalOcean account (free $5 credit)
- OpenAI API key

## Step 1: Deploy to DigitalOcean

### Option A: Deploy from GitHub (Recommended)

1. **Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)**
2. **Sign up/Login** with your GitHub account
3. **Click "Create App"**
4. **Select "GitHub" as source**
5. **Choose your `codecheck` repository**
6. **Select `digitalocean` branch**
7. **DigitalOcean will automatically:**
   - Detect it's a Python/FastAPI app
   - Install dependencies from `requirements.txt`
   - Start your app with `python main.py`
   - Assign a public URL

### Option B: Deploy with .do/app.yaml

1. **Upload your code** to DigitalOcean
2. **DigitalOcean will use the `.do/app.yaml` configuration**
3. **All settings are pre-configured**

## Step 2: Configure Environment Variables

1. **In DigitalOcean dashboard, go to your app**
2. **Click on "Settings" tab**
3. **Go to "Environment Variables"**
4. **Add these variables:**

   | Variable | Value | Description |
   |----------|-------|-------------|
   | `OPENAI_API_KEY` | `your_actual_openai_api_key` | Your OpenAI API key |
   | `ADMIN_PASSWORD` | `your_secure_password` | Admin panel password |
   | `DATABASE_URL` | `sqlite:///./ai_assessment.db` | Database connection |
   | `DIGITALOCEAN_ENVIRONMENT` | `production` | Environment flag |

## Step 3: Test Your Deployment

1. **Visit your DigitalOcean URL** (something like `https://your-app-name.ondigitalocean.app`)
2. **Test the upload page:** `https://your-app-name.ondigitalocean.app/upload`
3. **Test the admin panel:** `https://your-app-name.ondigitalocean.app/admin`
4. **Test the API docs:** `https://your-app-name.ondigitalocean.app/docs`

## Step 4: Custom Domain (Optional)

1. **In DigitalOcean dashboard, go to "Settings"**
2. **Click "Domains"**
3. **Add your custom domain:** `codecheck.website`
4. **Update your DNS** to point to DigitalOcean's provided CNAME

## Key Features of DigitalOcean Deployment

### ✅ **Automatic Detection**
- DigitalOcean automatically detects Python/FastAPI
- No manual configuration needed
- Works out of the box

### ✅ **Environment Variables**
- Easy to set in DigitalOcean dashboard
- Secure storage
- No command-line complexity

### ✅ **Automatic Scaling**
- Scales based on traffic
- No manual server management
- Built-in load balancing

### ✅ **Database Support**
- SQLite works out of the box
- Can upgrade to PostgreSQL easily
- Automatic backups

### ✅ **Logs & Monitoring**
- Real-time logs in dashboard
- Error tracking
- Performance metrics

### ✅ **Health Checks**
- Automatic health monitoring
- Auto-restart on failures
- Built-in monitoring

## Troubleshooting

### Common Issues:

1. **App won't start:**
   - Check the logs in DigitalOcean dashboard
   - Verify all environment variables are set
   - Ensure `requirements.txt` is correct

2. **Database errors:**
   - SQLite database is created automatically
   - Check file permissions
   - Verify `DATABASE_URL` is correct

3. **Import errors:**
   - DigitalOcean handles Python path automatically
   - No relative import issues
   - All dependencies installed correctly

### Logs:
- **View logs:** DigitalOcean dashboard → Your app → Runtime Logs
- **Real-time:** Logs update automatically
- **Error details:** Full stack traces available

## Advantages Over Railway

| Feature | Railway | DigitalOcean |
|---------|---------|--------------|
| **Setup Time** | 10+ minutes | 5 minutes |
| **Configuration** | Complex | Simple |
| **Environment Variables** | Dashboard UI | Dashboard UI |
| **Scaling** | Automatic | Automatic |
| **Logs** | Good | Excellent |
| **Deployment** | Git push | Git push |
| **Reliability** | Good | Excellent |
| **Free Tier** | $5 credit | $5 credit |
| **Branch Selection** | Problematic | Easy |

## Maintenance

### Updates:
1. **Push changes to `digitalocean` branch**
2. **DigitalOcean automatically redeploys**
3. **No manual intervention needed**

### Monitoring:
1. **Check DigitalOcean dashboard regularly**
2. **Monitor logs for errors**
3. **Set up alerts if needed**

### Backups:
1. **Database backups** - DigitalOcean handles this
2. **Code backups** - GitHub handles this
3. **Environment variables** - Stored securely in DigitalOcean

## Cost

- **Free tier:** $5/month credit (more than enough for small apps)
- **Paid plans:** Start at $5/month for more resources
- **No hidden fees** - Pay only for what you use

## Support

- **DigitalOcean Community:** Active support
- **Documentation:** Comprehensive guides
- **GitHub Issues:** Direct support from DigitalOcean team

---

**🎉 Your AI Code Assessment System is now live on DigitalOcean!**

Visit your DigitalOcean URL to start using your application. The deployment process is complete and your app is ready for production use!
