# 🚀 Deployment Checklist for Chikori Web

This checklist ensures your application is properly configured for production deployment on Render.

## ✅ Pre-Deployment Checklist

### 1. Environment Variables Setup

**In Render Environment Variables, set:**

```env
# Production Flitt Credentials
FLITT_MERCHANT_ID=your_real_merchant_id
FLITT_SECRET_KEY=your_real_secret_key

# Production Configuration
FLITT_BASE_URL=https://www.ganvadeba.store
FLITT_TEST_MODE=false
FLASK_ENV=production

# Security
FLASK_SECRET_KEY=your_secure_random_secret_key

# Optional
FLITT_SENDER_EMAIL=your@email.com
FLITT_SENDER_PHONE=+995555123456
```

### 2. Flitt Merchant Configuration

- [ ] Verify your Flitt merchant account is active
- [ ] Confirm API access is enabled for your account
- [ ] Set callback URLs in Flitt dashboard:
  - Success URL: `https://www.ganvadeba.store/payment-result`
  - Callback URL: `https://www.ganvadeba.store/payment-callback`
- [ ] Test with real credentials (not documentation test ones)

### 3. Domain Configuration

- [ ] Ensure `https://www.ganvadeba.store` is properly configured
- [ ] SSL certificate is active
- [ ] Domain points to your Render application

### 4. Application Files

- [ ] `app.py` - Main Flask application
- [ ] `config.py` - Configuration management
- [ ] `requirements.txt` - Python dependencies
- [ ] `gunicorn.conf.py` - Production server config
- [ ] All static files (HTML, CSS, JS, images)

## 🔧 Render Configuration

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
gunicorn app:app
```

### Environment Variables
Set all variables listed in section 1 above.

## 🧪 Testing Checklist

### 1. Local Testing
```bash
# Test environment configuration
python test_env.py

# Test local development
python app.py
# Visit http://localhost:8000
# Visit http://localhost:8000/api/check-env
```

### 2. Production Testing
- [ ] Visit `https://www.ganvadeba.store`
- [ ] Test product browsing
- [ ] Test payment flow (use test cards)
- [ ] Verify payment callbacks work
- [ ] Check error handling

### 3. Payment Testing
- [ ] Test with Flitt test cards
- [ ] Verify payment success flow
- [ ] Verify payment failure flow
- [ ] Check callback signature verification

## 🚨 Security Checklist

- [ ] No sensitive data in code files
- [ ] `.env` file in `.gitignore`
- [ ] Production credentials only in Render environment
- [ ] HTTPS enabled
- [ ] Proper error handling (no sensitive data in errors)
- [ ] Payment signature verification active

## 📊 Monitoring

### Logs to Monitor
- Payment creation attempts
- Payment callback responses
- Error messages
- Environment configuration on startup

### Health Checks
- Application startup logs
- Payment API connectivity
- Database connectivity (if applicable)

## 🔄 Environment Switching

### To Switch to Development:
1. Create `.env` file locally
2. Set `FLITT_BASE_URL=http://localhost:8000`
3. Set `FLITT_TEST_MODE=true`
4. Use test credentials

### To Switch to Production:
1. Set environment variables in Render
2. Set `FLITT_BASE_URL=https://www.ganvadeba.store`
3. Set `FLITT_TEST_MODE=false`
4. Use real credentials

## 🆘 Troubleshooting

### Common Issues

1. **Payment API Errors**
   - Check merchant credentials
   - Verify API access is enabled
   - Check callback URLs

2. **Environment Issues**
   - Run `python test_env.py` locally
   - Check Render environment variables
   - Verify `.env` file exists locally

3. **Domain Issues**
   - Check SSL certificate
   - Verify domain configuration
   - Test with and without www

### Support Contacts
- Flitt Support: For payment gateway issues
- Render Support: For deployment issues
- Your hosting provider: For domain/SSL issues

## 📝 Post-Deployment

After successful deployment:
1. Test all payment flows
2. Monitor logs for errors
3. Set up monitoring/alerting
4. Document any custom configurations
5. Create backup of environment variables

## User Registration System

### Data Persistence
The user registration system uses file-based storage in the `data/` directory:
- User data is stored in `data/users.json`
- This directory is excluded from Git (see `.gitignore`)
- Data persists between deployments on Render

### Security Features
- ✅ Passwords are hashed (SHA256)
- ✅ Session-based authentication
- ✅ Input validation
- ✅ Duplicate email prevention

### User Flow
1. Users click "შესვლა" → Redirected to `/login`
2. Can choose to login or register
3. After successful login → Redirected to home page
4. Login button shows user email when logged in

## File Structure
```
Chikori_Web/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── gunicorn.conf.py    # Gunicorn configuration
├── data/               # User data (created automatically)
│   └── users.json      # User accounts (not in Git)
├── index.html          # Main page
├── style.css           # Styles
├── app.js              # Frontend JavaScript
└── .gitignore          # Git ignore rules
```

## Monitoring

### Logs
- View logs in Render Dashboard
- Monitor for registration/login errors
- Check payment processing logs

### Health Checks
- Main page: `https://your-app.onrender.com/`
- User status: `https://your-app.onrender.com/api/user-status`
- Login page: `https://your-app.onrender.com/login`
- Register page: `https://your-app.onrender.com/register`

## Troubleshooting

### Common Issues
1. **Users not saving**: Check if `data/` directory exists and is writable
2. **Login failures**: Verify password hashing is working
3. **Session issues**: Check `SECRET_KEY` is set correctly

### Debug Endpoints (Development Only)
- `/api/check-env` - Check environment variables
- `/api/debug-tbc-payment` - Debug payment flow

## Security Notes
- Never commit `data/users.json` to Git
- Keep `SECRET_KEY` secure and unique
- Monitor for suspicious registration activity
- Consider rate limiting for registration/login

## Backup Strategy
- User data is stored in `data/users.json`
- Consider implementing database backup
- Monitor Render's persistent storage limits

## Updates
When updating the application:
1. Push changes to GitHub
2. Render will auto-deploy
3. User data persists in `data/` directory
4. No manual intervention needed

## Support
For issues with:
- **Render deployment**: Check Render documentation
- **Payment processing**: Check Flitt API documentation
- **User registration**: Check logs for specific errors 