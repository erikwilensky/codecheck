# Railway Deployment Guide

## 🚀 Deploy AI Code Assessment System to Railway

Railway is the easiest way to deploy your FastAPI application. No complex configuration, no WSGI issues, just connect and deploy!

### Prerequisites
- GitHub account
- Railway account (free at railway.app)
- OpenAI API key

## Step 1: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)

1. **Go to [railway.app](https://railway.app)**
2. **Sign up/Login** with your GitHub account
3. **Click "Deploy from GitHub repo"**
4. **Select your `codecheck` repository**
5. **Choose the `railway-clean` branch**
6. **Railway will automatically:**
   - Detect it's a Python/FastAPI app
   - Install dependencies from `requirements.txt`
   - Start your app with `python main.py`
   - Assign a public URL

## Step 2: Configure Environment Variables

1. **In Railway dashboard, go to your project**
2. **Click on "Variables" tab**
3. **Add these environment variables:**

   | Variable | Value | Description |
   |----------|-------|-------------|
   | `OPENAI_API_KEY` | `your_actual_openai_api_key` | Your OpenAI API key |
   | `ADMIN_PASSWORD` | `your_secure_password` | Admin panel password |
   | `DATABASE_URL` | `sqlite:///./ai_assessment.db` | Database connection |
   | `RAILWAY_ENVIRONMENT` | `production` | Environment flag |

## Step 3: Test Your Deployment

1. **Visit your Railway URL** (something like `https://your-app-name.railway.app`)
2. **Test the upload page:** `https://your-app-name.railway.app/upload`
3. **Test the admin panel:** `https://your-app-name.railway.app/admin`
4. **Test the API docs:** `https://your-app-name.railway.app/docs`

## Step 4: Custom Domain (Optional)

1. **In Railway dashboard, go to "Settings"**
2. **Click "Domains"**
3. **Add your custom domain:** `codecheck.website`
4. **Update your DNS** to point to Railway's provided CNAME

## Key Features of Railway Deployment

### ✅ **Automatic Detection**
- Railway automatically detects Python/FastAPI
- No manual configuration needed
- Works out of the box

### ✅ **Environment Variables**
- Easy to set in Railway dashboard
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

## Troubleshooting

### Common Issues:

1. **App won't start:**
   - Check the logs in Railway dashboard
   - Verify all environment variables are set
   - Ensure `requirements.txt` is correct

2. **Database errors:**
   - SQLite database is created automatically
   - Check file permissions
   - Verify `DATABASE_URL` is correct

3. **Import errors:**
   - Railway handles Python path automatically
   - No relative import issues
   - All dependencies installed correctly

### Logs:
- **View logs:** Railway dashboard → Your project → Logs
- **Real-time:** Logs update automatically
- **Error details:** Full stack traces available

## Advantages Over PythonAnywhere

| Feature | PythonAnywhere | Railway |
|---------|----------------|---------|
| **Setup Time** | 30+ minutes | 5 minutes |
| **Configuration** | Complex WSGI/ASGI | Automatic |
| **Environment Variables** | Command-line only | Dashboard UI |
| **Scaling** | Manual | Automatic |
| **Logs** | Hard to access | Real-time dashboard |
| **Deployment** | Git + commands | Git push |
| **Reliability** | Good | Excellent |
| **Free Tier** | Limited | Generous |

## Maintenance

### Updates:
1. **Push changes to `railway-clean` branch**
2. **Railway automatically redeploys**
3. **No manual intervention needed**

### Monitoring:
1. **Check Railway dashboard regularly**
2. **Monitor logs for errors**
3. **Set up alerts if needed**

### Backups:
1. **Database backups** - Railway handles this
2. **Code backups** - GitHub handles this
3. **Environment variables** - Stored securely in Railway

## Cost

- **Free tier:** $5/month credit (more than enough for small apps)
- **Paid plans:** Start at $5/month for more resources
- **No hidden fees** - Pay only for what you use

## Support

- **Railway Discord:** Active community support
- **Documentation:** Comprehensive guides
- **GitHub Issues:** Direct support from Railway team

---

**🎉 Your AI Code Assessment System is now live on Railway!**

Visit your Railway URL to start using your application. The deployment process is complete and your app is ready for production use!
