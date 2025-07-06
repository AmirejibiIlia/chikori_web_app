# Payment Services Overview

This document outlines the three distinct payment services integrated into the Chikori Web application.

## Service Architecture

```
app/services/
├── flitt_service.py           # Direct payment processing
├── tbc_installment_service.py # Traditional installment loans
└── tbc_ecommerce_service.py   # Buy Now Pay Later (BNPL)
```

## 1. Flitt Service (`flitt_service.py`)

**Purpose**: Direct payment processing
**API**: Flitt Payment Gateway
**Use Case**: Immediate payment with card

### Features:
- Direct card payment processing
- Real-time payment confirmation
- Support for multiple currencies (GEL)
- Merchant integration with Flitt

### Frontend Integration:
- **Button**: "ბარათით გადახდა" (Card Payment)
- **Options**: TBC card, BoG card
- **Process**: Direct payment → Confirmation

---

## 2. TBC Installment Service (`tbc_installment_service.py`)

**Purpose**: Traditional installment loan applications
**API**: TBC Online Installments API
**Use Case**: Loan application with approval process

### Features:
- Traditional loan application process
- Credit review and approval workflow
- Session-based application tracking
- Campaign-based installment plans

### Frontend Integration:
- **Button**: "განვადება" (Installment)
- **Options**: საქართველოს ბანკი, თიბისი
- **Process**: Application → Review → Approval → Loan

### API Endpoints:
- `POST /api/tbc-installment` - Create application
- `GET /tbc-installment-callback` - Handle callbacks
- `POST /api/tbc-installment/{session_id}/confirm` - Confirm application
- `POST /api/tbc-installment/{session_id}/cancel` - Cancel application

---

## 3. TBC E-Commerce Service (`tbc_ecommerce_service.py`)

**Purpose**: Buy Now Pay Later (BNPL)
**API**: TBC E-Commerce API (TPay)
**Use Case**: Instant credit approval for immediate purchase

### Features:
- Instant credit assessment
- Immediate approval/rejection
- Buy now, pay in installments later
- Real-time payment processing

### Frontend Integration:
- **Button**: "განაწილება" (Distribution)
- **Options**: განაწილება (TBC)
- **Process**: Instant check → Approval → Purchase → Installments

### API Endpoints:
- `POST /api/tbc-ecommerce-payment` - Create BNPL payment
- `POST /tbc-ecommerce-callback` - Handle callbacks

---

## Service Comparison

| Feature | Flitt | TBC Installment | TBC E-Commerce |
|---------|-------|-----------------|----------------|
| **Payment Type** | Direct | Loan Application | BNPL |
| **Approval Time** | Instant | Days/Weeks | Instant |
| **Credit Check** | None | Full Review | Quick Check |
| **Product Delivery** | Immediate | After Approval | Immediate |
| **Installment Plan** | No | Yes | Yes |
| **API Complexity** | Low | Medium | Medium |

## Configuration

Each service uses separate configuration sections in `config/settings.py`:

```python
# Flitt Configuration
FLITT_CONFIG = {
    'merchant_id': '...',
    'secret_key': '...',
    'base_url': '...'
}

# TBC Installment Configuration
TBC_CONFIG = {
    'api_key': '...',
    'api_secret': '...',
    'merchant_key': '...',
    'campaign_id': '...'
}

# TBC E-Commerce Configuration
TBC_ECOMMERCE_CONFIG = {
    'api_key': '...',
    'client_id': '...',
    'client_secret': '...',
    'merchant_key': '...'
}
```

## Frontend Integration

The frontend JavaScript (`app/static/js/app.js`) handles all three services:

1. **Flitt**: Direct payment processing
2. **TBC Installment**: Traditional loan applications
3. **TBC E-Commerce**: BNPL payments

Each service has its own error handling, response processing, and user feedback mechanisms.

## Testing

All services can be tested independently:

```bash
# Test Flitt
curl -X POST http://localhost:8000/api/create-payment \
  -H "Content-Type: application/json" \
  -d '{"product_id": "table", "amount": 51}'

# Test TBC Installment
curl -X POST http://localhost:8000/api/tbc-installment \
  -H "Content-Type: application/json" \
  -d '{"product_id": "table", "amount": 51}'

# Test TBC E-Commerce (BNPL)
curl -X POST http://localhost:8000/api/tbc-ecommerce-payment \
  -H "Content-Type: application/json" \
  -d '{"product_id": "table", "amount": 51}'
```

## Maintenance

Each service is now independently maintainable:
- **Isolated code**: Changes to one service don't affect others
- **Clear separation**: Each service has its own file and configuration
- **Easy debugging**: Issues can be traced to specific services
- **Scalable**: New payment providers can be added easily 