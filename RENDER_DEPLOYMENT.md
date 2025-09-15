# Render Deployment Guide

## 🚀 Deploy AI Code Assessment System to Render

Render is the perfect choice for free hosting! It's reliable, easy to use, and has excellent FastAPI support.

### Prerequisites
- GitHub account
- Render account (free at render.com)
- OpenAI API key

## Step 1: Deploy to Render

### Option A: Deploy from GitHub (Recommended)

1. **Go to [render.com](https://render.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**
5. **Select `codecheck` repository**
6. **Choose `render` branch**
7. **Render will automatically:**
   - Detect it's a Python/FastAPI app
   - Install dependencies from `requirements.txt`
   - Start your app with `python main.py`
   - Assign a public URL

### Option B: Deploy with render.yaml

1. **Upload your code** to Render
2. **Render will use the `render.yaml` configuration**
3. **All settings are pre-configured**

## Step 2: Configure Environment Variables

1. **In Render dashboard, go to your service**
2. **Click on "Environment" tab**
3. **Add these variables:**

   | Variable | Value | Description |
   |----------|-------|-------------|
   | `OPENAI_API_KEY` | `your_actual_openai_api_key` | Your OpenAI API key |
   | `ADMIN_PASSWORD` | `your_secure_password` | Admin panel password |
   | `DATABASE_URL` | `sqlite:///./ai_assessment.db` | Database connection |
   | `RENDER` | `true` | Environment flag |

## Step 3: Test Your Deployment

1. **Visit your Render URL** (something like `https://codecheck.onrender.com`)
2. **Test the upload page:** `https://codecheck.onrender.com/upload`
3. **Test the admin panel:** `https://codecheck.onrender.com/admin`
4. **Test the API docs:** `https://codecheck.onrender.com/docs`

## Step 4: Custom Domain (Optional)

1. **In Render dashboard, go to "Settings"**
2. **Click "Custom Domains"**
3. **Add your custom domain:** `codecheck.website`
4. **Update your DNS** to point to Render's provided CNAME

## Key Features of Render Deployment

### ✅ **Free Tier**
- **750 hours/month** (enough for 24/7 operation)
- **No credit card required**
- **Perfect for small to medium apps**

### ✅ **Automatic Detection**
- Render automatically detects Python/FastAPI
- No manual configuration needed
- Works out of the box

### ✅ **Environment Variables**
- Easy to set in Render dashboard
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

### ✅ **GitHub Integration**
- Auto-deploys on push
- Easy to manage
- Version control integration

## Troubleshooting

### Common Issues:

1. **App won't start:**
   - Check the logs in Render dashboard
   - Verify all environment variables are set
   - Ensure `requirements.txt` is correct

2. **Database errors:**
   - SQLite database is created automatically
   - Check file permissions
   - Verify `DATABASE_URL` is correct

3. **Import errors:**
   - Render handles Python path automatically
   - No relative import issues
   - All dependencies installed correctly

4. **App sleeps after inactivity:**
   - This is normal on free tier
   - First request after sleep takes longer
   - Consider upgrading to paid plan for always-on

### Logs:
- **View logs:** Render dashboard → Your service → Logs
- **Real-time:** Logs update automatically
- **Error details:** Full stack traces available

## Advantages Over Other Platforms

| Feature | Railway | DigitalOcean | Render |
|---------|---------|--------------|--------|
| **Setup Time** | 10+ minutes | 5 minutes | 2 minutes |
| **Configuration** | Complex | Simple | Simple |
| **Environment Variables** | Dashboard UI | Dashboard UI | Dashboard UI |
| **Scaling** | Automatic | Automatic | Automatic |
| **Logs** | Good | Excellent | Excellent |
| **Deployment** | Git push | Git push | Git push |
| **Reliability** | Good | Excellent | Excellent |
| **Free Tier** | $5 credit | $5 credit | 750 hours/month |
| **Branch Selection** | Problematic | Easy | Easy |
| **Cost** | $24/month | $24/month | **FREE** |

## Maintenance

### Updates:
1. **Push changes to `render` branch**
2. **Render automatically redeploys**
3. **No manual intervention needed**

### Monitoring:
1. **Check Render dashboard regularly**
2. **Monitor logs for errors**
3. **Set up alerts if needed**

### Backups:
1. **Database backups** - Render handles this
2. **Code backups** - GitHub handles this
3. **Environment variables** - Stored securely in Render

## Cost

- **Free tier:** 750 hours/month (completely free!)
- **Paid plans:** Start at $7/month for always-on
- **No hidden fees** - Pay only for what you use

## Support

- **Render Community:** Active support
- **Documentation:** Comprehensive guides
- **GitHub Issues:** Direct support from Render team

---

**🎉 Your AI Code Assessment System is now live on Render!**

Visit your Render URL to start using your application. The deployment process is complete and your app is ready for production use - completely free! 🚀
