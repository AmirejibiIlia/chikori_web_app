# Chikori Web - Online Furniture Store with Flitt Payment Integration

This is an online furniture store built with Flask and JavaScript, integrated with Flitt payment gateway for secure online payments.

## Features

- Product catalog with search and filtering
- Multiple payment options (installment, card payment)
- Flitt payment gateway integration for TBC card payments
- Responsive design
- Payment status handling

## 🌍 Environment Configuration

This application supports both development and production environments. You can switch between them by modifying environment variables.

### Quick Setup

1. **Copy the environment template:**
   ```bash
   cp env.example .env
   ```

2. **Fill in your credentials in `.env`:**
   ```env
   # Development (testing)
   FLITT_MERCHANT_ID=your_test_merchant_id
   FLITT_SECRET_KEY=your_test_secret_key
   FLITT_BASE_URL=http://localhost:8000
   FLITT_TEST_MODE=true
   
   # Production (real payments)
   FLITT_MERCHANT_ID=your_real_merchant_id
   FLITT_SECRET_KEY=your_real_secret_key
   FLITT_BASE_URL=https://www.ganvadeba.store
   FLITT_TEST_MODE=false
   ```

### Environment Variables

| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `FLITT_MERCHANT_ID` | Test ID | Real ID | Your Flitt merchant ID |
| `FLITT_SECRET_KEY` | Test Key | Real Key | Your Flitt secret key |
| `FLITT_BASE_URL` | `http://localhost:8000` | `https://www.ganvadeba.store` | Your website URL |
| `FLITT_TEST_MODE` | `true` | `false` | Enable/disable test mode |
| `FLASK_ENV` | `development` | `production` | Flask environment |
| `FLASK_SECRET_KEY` | Any string | Secure random | Flask secret key |

### Switching Environments

#### For Local Development:
```env
FLITT_BASE_URL=http://localhost:8000
FLITT_TEST_MODE=true
FLASK_ENV=development
```

#### For Production (Render):
Set these in Render Environment Variables:
```env
FLITT_BASE_URL=https://www.ganvadeba.store
FLITT_TEST_MODE=false
FLASK_ENV=production
```

### Environment Check

Visit `/api/check-env` in development to verify your configuration:
```bash
curl http://localhost:8000/api/check-env
```

This endpoint is only available in development mode for security.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Flitt Credentials

Create a `.env` file in your project root with your Flitt credentials:

```env
# Flitt Configuration
FLITT_MERCHANT_ID=your_real_merchant_id
FLITT_SECRET_KEY=your_real_secret_key
FLITT_API_DOMAIN=pay.flitt.com
FLITT_CURRENCY=GEL
FLITT_LANG=ka
FLITT_TEST_MODE=false
FLITT_BASE_URL=https://yourdomain.com
FLITT_SENDER_EMAIL=your@email.com
FLITT_SENDER_PHONE=+995555123456

# Flask Configuration
FLASK_SECRET_KEY=your_flask_secret_key
FLASK_ENV=production
```

**Important**: The test credentials (`1549901`/`test`) from Flitt documentation are **NOT valid for API use**. You need real credentials from Flitt.

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:8000`

## Payment Flow

1. User clicks "შეძენა" (Buy) on a product
2. User selects "ბარათით გადახდა" (Pay by Card)
3. User clicks "TBC card"
4. System creates a payment order via Flitt API
5. User is redirected to Flitt payment page
6. After payment, user is redirected back to the store
7. Payment status is displayed to the user

## API Endpoints

- `POST /api/create-payment` - Creates a payment order and returns Flitt checkout URL
- `GET /payment-result` - Handles payment result redirect from Flitt
- `POST /payment-callback` - Handles server callback from Flitt

## Troubleshooting

### Common Issues

#### 1. Error Code 1002 - "Application error"
**Cause**: Invalid credentials or merchant not enabled for API access
**Solution**: 
- Contact Flitt support to get real credentials
- Verify your merchant account is enabled for API access
- Check if you need a sandbox environment

#### 2. Error Code 1001 - "Invalid signature"
**Cause**: Wrong secret key or signature generation
**Solution**:
- Verify your secret key is correct
- Check that signature generation follows Flitt's requirements

#### 3. Error Code 1003 - "Invalid request parameters"
**Cause**: Missing or invalid required fields
**Solution**:
- Ensure all required fields are present
- Check field formats (amount in cents, valid currency, etc.)

### Testing

For testing, you need:
1. **Real Flitt credentials** (not the documentation test ones)
2. **A sandbox environment** if available
3. **Test card numbers** from Flitt

### Getting Real Credentials

1. Contact Flitt support at their official website
2. Request API access for your merchant account
3. Ask for sandbox/test environment credentials
4. Get test card numbers for payment testing

## Production Deployment

For production deployment:

1. Use environment variables for sensitive credentials
2. Set up proper SSL certificates
3. Configure your domain in Flitt merchant settings
4. Update callback URLs to use your production domain
5. Set `FLITT_TEST_MODE=false`
6. Use real merchant credentials

## File Structure

```
├── app.py              # Flask backend with payment API
├── app.js              # Frontend JavaScript with payment handling
├── index.html          # Main HTML page
├── style.css           # CSS styles
├── config.py           # Flitt configuration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # This file
```

## Security Notes

- Always verify signatures in payment callbacks
- Use HTTPS in production
- Store sensitive credentials securely in environment variables
- Implement proper error handling
- Log payment transactions for audit purposes
- Never commit `.env` files to version control

## Environment Variables and Configuration

All Flitt and Flask configuration is managed via environment variables. You can set these in a `.env` file at the project root (see above for an example). This makes it easy to switch between test and production environments.

- To use production, set your real merchant ID and secret, and set `FLITT_TEST_MODE=false`.
- To use test mode, use your test credentials and set `FLITT_TEST_MODE=true`.

The app will automatically load these variables on startup. 