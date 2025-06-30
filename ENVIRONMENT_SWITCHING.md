# 🔄 Environment Switching Guide

This guide shows you exactly how to switch between development and production environments by modifying your `.env` file values.

## 🎯 Your Goal

**By just modifying values in `.env`, you can switch to production level for your real webpage at https://www.ganvadeba.store**

## 📁 Current Setup

Your application is already configured to support both environments. Here's what you have:

### ✅ What's Already Working
- Environment variable loading via `python-dotenv`
- Configuration management in `config.py`
- Production URL detection
- Test mode switching
- Security measures (`.env` in `.gitignore`)

### 🔧 Files Created/Updated
- `env.example` - Template for environment variables
- `config.py` - Enhanced with environment detection
- `app.py` - Added environment check endpoint
- `test_env.py` - Environment testing script
- `DEPLOYMENT.md` - Deployment checklist

## 🔄 How to Switch Environments

### For Local Development (Testing)

Create or modify your `.env` file:

```env
# Development Configuration
FLITT_MERCHANT_ID=your_test_merchant_id
FLITT_SECRET_KEY=your_test_secret_key
FLITT_BASE_URL=http://localhost:8000
FLITT_TEST_MODE=true
FLASK_ENV=development
FLASK_SECRET_KEY=dev_secret_key
```

### For Production (Real Website)

Modify your `.env` file:

```env
# Production Configuration
FLITT_MERCHANT_ID=4054082
FLITT_SECRET_KEY=APvSrPJZn6...
FLITT_BASE_URL=https://www.ganvadeba.store
FLITT_TEST_MODE=false
FLASK_ENV=production
FLASK_SECRET_KEY=460438cbe246a0bf80e05eedad46455318a610ddf871da524b8534da127c0f7b
```

## 🧪 Testing Your Configuration

### 1. Test Environment Variables
```bash
python test_env.py
```

### 2. Test Application Loading
```bash
python -c "from config import FLITT_CONFIG, IS_PRODUCTION; print(f'Environment: {\"PRODUCTION\" if IS_PRODUCTION else \"DEVELOPMENT\"}'); print(f'Base URL: {FLITT_CONFIG[\"base_url\"]}')"
```

### 3. Test Local Development
```bash
python app.py
# Visit http://localhost:8000/api/check-env
```

## 🌍 Environment Detection Logic

Your application automatically detects the environment:

```python
# From config.py
IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('ENVIRONMENT') == 'production'
```

**Development Mode:**
- `FLASK_ENV` not set or set to anything other than 'production'
- Debug mode enabled
- Environment check endpoint available

**Production Mode:**
- `FLASK_ENV=production` or `ENVIRONMENT=production`
- Debug mode disabled
- Environment check endpoint disabled for security

## 🔐 Security Features

### ✅ What's Protected
- `.env` file is in `.gitignore` (never committed to git)
- Production credentials only in environment variables
- Environment check endpoint only available in development
- Sensitive data masked in logs

### 🚨 Important Notes
- Never commit real credentials to git
- Use test credentials for local development
- Use real credentials only in production
- Always verify payment signatures in production

## 📋 Quick Reference

### Development Values
| Variable | Value |
|----------|-------|
| `FLITT_BASE_URL` | `http://localhost:8000` |
| `FLITT_TEST_MODE` | `true` |
| `FLASK_ENV` | `development` |

### Production Values
| Variable | Value |
|----------|-------|
| `FLITT_BASE_URL` | `https://www.ganvadeba.store` |
| `FLITT_TEST_MODE` | `false` |
| `FLASK_ENV` | `production` |

## 🚀 Render Deployment

For your Render deployment, set these environment variables in the Render dashboard:

```env
FLITT_MERCHANT_ID=4054082
FLITT_SECRET_KEY=APvSrPJZn6...
FLITT_BASE_URL=https://www.ganvadeba.store
FLITT_TEST_MODE=false
FLASK_ENV=production
FLASK_SECRET_KEY=460438cbe246a0bf80e05eedad46455318a610ddf871da524b8534da127c0f7b
```

## ✅ Verification Checklist

After switching environments:

- [ ] Run `python test_env.py` - should show correct environment
- [ ] Check base URL matches your environment
- [ ] Verify test mode is correct for your environment
- [ ] Test payment flow (use test cards in development)
- [ ] Check that environment detection works correctly

## 🆘 Troubleshooting

### Common Issues

1. **Wrong URL showing**
   - Check `FLITT_BASE_URL` in `.env`
   - Restart your application after changing `.env`

2. **Test mode not working**
   - Ensure `FLITT_TEST_MODE=true` for development
   - Ensure `FLITT_TEST_MODE=false` for production

3. **Environment not detected**
   - Check `FLASK_ENV` variable
   - Restart application after changes

### Getting Help

- Run `python test_env.py` to diagnose issues
- Check `/api/check-env` endpoint in development
- Review the `DEPLOYMENT.md` checklist

## 🎉 Success!

You now have a fully configured environment switching system. You can:

1. **Switch to development** by setting `FLITT_BASE_URL=http://localhost:8000` and `FLITT_TEST_MODE=true`
2. **Switch to production** by setting `FLITT_BASE_URL=https://www.ganvadeba.store` and `FLITT_TEST_MODE=false`
3. **Deploy to Render** with production environment variables
4. **Test locally** with development environment variables

Your application will automatically adapt to the environment based on your `.env` file values! 