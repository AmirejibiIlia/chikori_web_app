# Chikori Web - Modular Architecture

## Overview

The Chikori Web application has been completely refactored from a static, monolithic structure to a **truly modular and flexible system**. This document explains the new architecture and how to use it.

## 🎯 Key Improvements

### Before (Static)
- ❌ Hardcoded prices (51) in multiple places
- ❌ Duplicate product data in multiple files
- ❌ Static payment options hardcoded in HTML/JS
- ❌ Manual price updates required everywhere
- ❌ Adding products required code changes
- ❌ Payment methods hardcoded in frontend

### After (Modular)
- ✅ **Single source of truth** for all product data
- ✅ **Dynamic price ranges** calculated automatically
- ✅ **Centralized payment configuration**
- ✅ **Dynamic payment routing** system
- ✅ **Admin interface** for product management
- ✅ **Bulk price updates** with one click
- ✅ **Flexible payment method** addition/removal

## 🏗️ Architecture Overview

```
Chikori_Web/
├── config/
│   ├── settings.py          # App configuration
│   └── products.py          # 🆕 Single source of truth for products
├── app/
│   ├── models/
│   │   └── product.py       # Product model (uses config)
│   ├── services/
│   │   ├── flitt_service.py           # Direct payments
│   │   ├── tbc_installment_service.py # Installment loans
│   │   ├── tbc_ecommerce_service.py   # BNPL payments
│   │   └── payment_router.py          # 🆕 Dynamic payment routing
│   ├── views/
│   │   ├── payment_views.py # Payment endpoints
│   │   ├── admin_views.py   # 🆕 Admin interface
│   │   └── ...
│   ├── static/
│   │   └── js/
│   │       └── app_dynamic.js # 🆕 Dynamic frontend
│   └── templates/
│       ├── index.html       # Main page
│       └── admin.html       # 🆕 Admin interface
└── app_new.py              # Main application
```

## 📦 Core Components

### 1. Centralized Product Configuration (`config/products.py`)

**Single source of truth** for all product data:

```python
PRODUCTS = {
    'table': {
        'id': 'table',
        'name': 'კარადა',
        'price': 51.00,  # Change here, updates everywhere!
        'currency': 'GEL',
        'category': 'furniture',
        'rating': 4.9,
        'image': 'https://...',
        'sku': 'TABLE_001',
        'description': '...',
        'active': True
    },
    # ... more products
}
```

**Dynamic Functions:**
- `get_price_ranges()` - Automatically calculates price filter ranges
- `update_product_price()` - Update price in one place
- `add_product()` - Add new products dynamically
- `remove_product()` - Soft delete products

### 2. Dynamic Payment Router (`app/services/payment_router.py`)

**Routes any payment method to the correct service:**

```python
PAYMENT_METHODS = {
    'card': {
        'name': 'ბარათით გადახდა',
        'options': {
            'tbc_card': {
                'name': 'TBC card',
                'service': 'flitt'  # Routes to Flitt service
            },
            'bog_card': {
                'name': 'BoG card', 
                'service': 'flitt'  # Routes to Flitt service
            }
        }
    },
    'installment': {
        'name': 'განვადება',
        'options': {
            'tbc_installment': {
                'name': 'თიბისი',
                'service': 'tbc_installment'  # Routes to TBC service
            }
        }
    }
}
```

### 3. Dynamic Frontend (`app/static/js/app_dynamic.js`)

**Loads everything dynamically from APIs:**

```javascript
// Load all data on page load
window.addEventListener('DOMContentLoaded', async () => {
    // Load products
    const products = await fetch('/api/products').then(r => r.json());
    
    // Load payment methods
    const paymentMethods = await fetch('/api/payment-methods').then(r => r.json());
    
    // Load price ranges
    const priceRanges = await fetch('/api/price-ranges').then(r => r.json());
    
    // Render everything dynamically
    renderProducts(products);
    populatePriceFilter(priceRanges);
});
```

## 🚀 How to Use the New System

### 1. Change Product Prices

**Before:** Had to change prices in multiple files
**Now:** Change in one place - `config/products.py`

```python
# Change this line
'price': 51.00,  # Old price

# To this
'price': 75.00,  # New price
```

**Result:** Price updates everywhere automatically!

### 2. Add New Products

**Before:** Had to modify code files
**Now:** Use the admin interface or API

**Via Admin Interface:**
1. Go to `http://localhost:8000/admin`
2. Fill out the product form
3. Click "Save Product"

**Via API:**
```bash
curl -X POST http://localhost:8000/api/admin/add-product \
  -H "Content-Type: application/json" \
  -d '{
    "id": "chair",
    "name": "სავარძელი",
    "price": 45.00,
    "category": "furniture",
    "rating": 4.8,
    "image": "https://...",
    "sku": "CHAIR_001",
    "description": "..."
  }'
```

### 3. Bulk Price Updates

**Before:** Had to change each product individually
**Now:** Update all prices at once

**Via Admin Interface:**
1. Go to `http://localhost:8000/admin`
2. Enter multiplier (e.g., 1.1 for 10% increase)
3. Click "Update All Prices"

**Via API:**
```bash
curl -X POST http://localhost:8000/api/admin/update-prices \
  -H "Content-Type: application/json" \
  -d '{"multiplier": 1.1}'
```

### 4. Add New Payment Methods

**Before:** Had to modify frontend code
**Now:** Just update the configuration

```python
# In config/products.py, add to PAYMENT_METHODS
'new_method': {
    'name': 'New Payment Method',
    'options': {
        'new_option': {
            'name': 'New Option',
            'bank': 'NEW_BANK',
            'icon': 'https://...',
            'service': 'new_service'  # Routes to new service
        }
    }
}
```

## 🔧 API Endpoints

### Product Management
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get single product
- `POST /api/admin/add-product` - Add/update product
- `PUT /api/admin/update-product/<id>` - Update product
- `DELETE /api/admin/delete-product/<id>` - Delete product
- `POST /api/admin/update-prices` - Bulk price update

### Dynamic Configuration
- `GET /api/payment-methods` - Get payment methods config
- `GET /api/price-ranges` - Get dynamic price ranges

### Dynamic Payments
- `POST /api/dynamic-payment` - Route to appropriate payment service

## 🎨 Frontend Features

### Dynamic Price Filtering
- Price ranges calculated automatically from actual product prices
- No hardcoded ranges in HTML
- Updates when prices change

### Dynamic Payment Options
- Payment methods loaded from configuration
- New payment methods appear automatically
- Icons and names from configuration

### Responsive Design
- All dynamic content works on mobile and desktop
- No page reloads needed for updates

## 🔒 Security & Best Practices

### Admin Interface
- Currently no authentication (add for production)
- All changes are immediate
- Validation on all inputs

### Data Validation
- Required fields checked
- Price validation
- URL validation for images

### Error Handling
- Graceful fallbacks for missing data
- User-friendly error messages
- Console logging for debugging

## 🚀 Deployment Benefits

### Scalability
- Easy to add new products
- Easy to add new payment methods
- Easy to modify prices

### Maintainability
- Single source of truth
- Clear separation of concerns
- Modular architecture

### Flexibility
- Dynamic configuration
- No code changes for content updates
- Admin interface for non-technical users

## 📝 Migration Guide

### From Old System
1. **Products:** All product data moved to `config/products.py`
2. **Payments:** New dynamic routing system
3. **Frontend:** New dynamic JavaScript file
4. **Admin:** New admin interface available

### Backward Compatibility
- Old API endpoints still work
- Old payment methods still supported
- Gradual migration possible

## 🎯 Future Enhancements

### Planned Features
- [ ] Database integration for persistence
- [ ] User authentication for admin
- [ ] Product categories management
- [ ] Inventory tracking
- [ ] Order management
- [ ] Analytics dashboard

### Extensibility
- Easy to add new payment services
- Easy to add new product types
- Easy to add new features

## 📞 Support

For questions or issues with the new modular system:
1. Check the API documentation
2. Review the configuration files
3. Test with the admin interface
4. Check browser console for errors

---

**The new modular architecture makes Chikori Web truly flexible and maintainable! 🎉** 