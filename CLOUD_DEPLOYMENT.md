# RH Agent Cloud Deployment Guide

## 🌐 Cloud Deployment Options

### 1. **Heroku** (Recommended for beginners)
### 2. **Railway** (Modern alternative)
### 3. **Render** (Free tier available)
### 4. **AWS/GCP/Azure** (Enterprise solutions)

---

## 🚀 Heroku Deployment

### **Step 1: Prepare Your Application**

1. **Create a `Procfile`** in your server directory:
```
web: python main.py
```

2. **Create `runtime.txt`** to specify Python version:
```
python-3.11.0
```

3. **Update `requirements.txt`** (already done):
```
Flask==2.3.3
flask-cors==4.0.0
pymongo==4.6.0
python-dotenv==1.0.0
google-generativeai==0.3.2
pandas==2.1.4
gunicorn==21.2.0
```

### **Step 2: Environment Variables**

Set these in Heroku dashboard or CLI:

```bash
# MongoDB Atlas credentials
user_pass=your_mongodb_username
pass_key=your_mongodb_password

# Gemini AI API key
gemini_ai_key=your_gemini_api_key

# Flask environment
FLASK_ENV=production
```

### **Step 3: Deploy to Heroku**

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create your-rh-agent-app

# Set environment variables
heroku config:set user_pass=your_mongodb_username
heroku config:set pass_key=your_mongodb_password
heroku config:set gemini_ai_key=your_gemini_api_key

# Deploy
git add .
git commit -m "Deploy RH Agent to Heroku"
git push heroku main

# Open your app
heroku open
```

---

## 🚂 Railway Deployment

### **Step 1: Connect Repository**

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select your project

### **Step 2: Environment Variables**

Add these in Railway dashboard:
```
user_pass=your_mongodb_username
pass_key=your_mongodb_password
gemini_ai_key=your_gemini_api_key
PORT=5000
```

### **Step 3: Deploy**

Railway will automatically detect your Python app and deploy it.

---

## 🔧 Environment Configuration

### **Local Development (.env file)**
```env
# MongoDB Atlas
user_pass=your_mongodb_username
pass_key=your_mongodb_password

# Gemini AI
gemini_ai_key=your_gemini_api_key

# Flask
FLASK_ENV=development
```

### **Cloud Production**
Set these as environment variables in your cloud platform:
- `user_pass`: MongoDB username
- `pass_key`: MongoDB password
- `gemini_ai_key`: Google Gemini API key
- `PORT`: Port number (usually 5000 or provided by platform)

---

## 🗄️ MongoDB Atlas Configuration

### **1. Network Access**
- Add your cloud platform's IP ranges
- Or add `0.0.0.0/0` for all IPs (less secure)

### **2. Database User**
- Create a user with read/write permissions
- Use these credentials in environment variables

### **3. Connection String**
Your connection string should be:
```
mongodb+srv://username:password@cluster0.ggtqgzr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

---

## 🔒 Security Best Practices

### **1. Environment Variables**
- Never commit `.env` files to Git
- Use cloud platform's environment variable system
- Rotate credentials regularly

### **2. MongoDB Security**
- Use strong passwords
- Enable IP whitelisting
- Use database users with minimal required permissions

### **3. API Security**
- Add authentication if needed
- Use HTTPS in production
- Implement rate limiting

---

## 📊 Monitoring & Logs

### **Heroku**
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

### **Railway**
- View logs in Railway dashboard
- Monitor resource usage

---

## 🐛 Troubleshooting

### **Common Issues:**

1. **Database Connection Failed**
   - Check environment variables
   - Verify MongoDB Atlas network access
   - Check connection string format

2. **Module Import Errors**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

3. **Port Issues**
   - Use `os.environ.get('PORT', 5000)` for dynamic port
   - Check if platform assigns specific port

### **Debug Commands:**

```bash
# Check environment variables
heroku config

# Test database connection
heroku run python -c "from helper.tool import db; print('DB connected:', db is not None)"

# View detailed logs
heroku logs --tail --source app
```

---

## 🚀 Quick Deploy Script

Create `deploy.sh`:

```bash
#!/bin/bash
echo "🚀 Deploying RH Agent to Heroku..."

# Check if logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Please login to Heroku first: heroku login"
    exit 1
fi

# Set environment variables
echo "📝 Setting environment variables..."
heroku config:set user_pass=$MONGODB_USERNAME
heroku config:set pass_key=$MONGODB_PASSWORD
heroku config:set gemini_ai_key=$GEMINI_API_KEY

# Deploy
echo "🚀 Deploying..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

echo "✅ Deployment complete!"
echo "🌐 Your app: https://your-app-name.herokuapp.com"
```

---

## 📈 Scaling Considerations

### **Free Tier Limits:**
- Heroku: 550-1000 dyno hours/month
- Railway: 500 hours/month
- Render: 750 hours/month

### **Upgrading:**
- Monitor usage and upgrade when needed
- Consider database connection pooling
- Implement caching for better performance

---

## 🔄 CI/CD Pipeline

### **GitHub Actions Example:**

```yaml
name: Deploy to Heroku
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "your-app-name"
          heroku_email: "your-email@example.com"
```

---

## 📞 Support

If you encounter issues:

1. Check the logs first
2. Verify environment variables
3. Test database connection
4. Check platform-specific documentation

Your RH Agent is now ready for cloud deployment! 🎉