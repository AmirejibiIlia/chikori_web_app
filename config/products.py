"""
Centralized Product Configuration
This is the single source of truth for all product data, prices, and metadata.
"""

import os

# Product Categories
PRODUCT_CATEGORIES = {
    'furniture': {
        'name': 'ავეჯი',
        'description': 'სახლისა და ოფისის ავეჯი'
    }
}

# Dynamic Product Prices from Environment Variables
PRICE_BED_S = int(os.environ.get('PRICE_BED_S', 260))
PRICE_BED_B = int(os.environ.get('PRICE_BED_B', 500))
PRICE_CORNER_SOFA = int(os.environ.get('PRICE_CORNER_SOFA', 600))
PRICE_TABLE = int(os.environ.get('PRICE_TABLE', 700))


# Product Data - Single source of truth
PRODUCTS = {
    'table': {
        'id': 'corner_sofa',
        'name': 'სამზარეულოს კუთხე',
        'price': PRICE_CORNER_SOFA,
        'currency': 'GEL',
        'category': 'furniture',
        'rating': 4.98,
        'image': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/kutxe.png',
        'sku': 'TABLE_001',
        'description': '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 124x164x83 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> ლამინატი <br><strong>ფერი:</strong> ხისფერი (ვამზადებთ შეკვეთით) <br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი ✅ </strong><br><strong> შეკვეთამდე დაგვიკავშირდით ნომერზე/მოგვწერეთ Facebook-ზე </strong>',
        'features': ['MDF მასალა', 'თეთრი ფერი', '3 დღე დამზადება'],
        'dimensions': '124x164x83',
        'material': 'ლამინატი',
        'color': 'თეთრი',
        'production_time': '3 სამუშაო დღე',
        'delivery': 'აწყობილ მდგომარეობაში',
        'active': True
    },
    'bed': {
        'id': 'table',
        'name': 'ტრანსფორმერი მაგიდა',
        'price': PRICE_TABLE,
        'currency': 'GEL',
        'category': 'furniture',
        'rating': 5.00,
        'image': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/transformeri.png',
        'sku': 'BED_001',
        'description': '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 90x70x50 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> ლამინატი <br><strong>ფერი:</strong> ხისფერი (ვამზადებთ შეკვეთით) <br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი ✅ </strong><br><strong> შეკვეთამდე დაგვიკავშირდით ნომერზე/მოგვწერეთ Facebook-ზე </strong>',
        'features': ['მეტალის კონსტრუქცია', 'შავი ფერი', '3 დღე დამზადება'],
        'dimensions': 'Queen Size',
        'material': 'მეტალი',
        'color': 'შავი',
        'production_time': '3 სამუშაო დღე',
        'delivery': 'აწყობილ მდგომარეობაში',
        'active': True
    },
    'sofa': {
        'id': 'Bed',
        'name': 'საწოლი პატარა',
        'price': PRICE_BED_S,
        'currency': 'GEL',
        'category': 'furniture',
        'rating': 5.0,
        'image': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/1_sawoliani.png',
        'sku': 'SOFA_001',
        'description': '<strong>ძირითადი მახასიათებლები </strong><br><br><strong> ფასი მოცემულია მატრასის გარეშე, მატრასი + 100 ლარიდან </strong><br><br><strong>ზომები:</strong> 90X200 <br><strong>მასალა:</strong> LMNT<br><strong>ფერი:</strong> შეკვეთით <br><strong>დამზადების ვადა:</strong> 2 სამუშაო დღე<br><strong>მიწოდება:</strong> ასაწყობ მდგომარეობაში<br><strong>მიტანის სერვისი ✅ </strong><br><strong> შეკვეთამდე დაგვიკავშირდით ნომერზე/მოგვწერეთ Facebook-ზე </strong>',
        'features': ['MDF/LMNT მასალა', 'ხისფერი ფერი', '2 დღე დამზადება'],
        'dimensions': '124x164x83',
        'material': 'MDF/LMNT',
        'color': 'ხისფერი (მონაცრისფრო)',
        'production_time': '2 სამუშაო დღე',
        'delivery': 'აწყობილ მდგომარეობაში',
        'active': True
    },
    
    'desk': {
        'id': 'desk',
        'name': 'საწოლი დიდი',
        'price': PRICE_BED_B,
        'currency': 'GEL',
        'category': 'furniture',
        'rating': 5.0,
        'image': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/2_sawoliani.png',
        'sku': 'SOFA_002',
        'description': '<strong>ძირითადი მახასიათებლები </strong><br><br><strong> ფასი მოცემულია მატრასის გარეშე, მატრასი + 100 ლარიდან </strong><br><br><strong>ზომები:</strong> 160X200 <br><strong>მასალა:</strong> LMNT<br><strong>ფერი:</strong> შეკვეთით <br><strong>დამზადების ვადა:</strong> 2 სამუშაო დღე<br><strong>მიწოდება:</strong> ასაწყობ მდგომარეობაში<br><strong>მიტანის სერვისი ✅ </strong><br><strong> შეკვეთამდე დაგვიკავშირდით ნომერზე/მოგვწერეთ Facebook-ზე </strong>',
        'features': ['MDF/LMNT მასალა', 'ხისფერი ფერი', '2 დღე დამზადება'],
        'dimensions': '124x164x83',
        'material': 'MDF/LMNT',
        'color': 'ხისფერი (მონაცრისფრო)',
        'production_time': '2 სამუშაო დღე',
        'delivery': 'აწყობილ მდგომარეობაში',
        'active': True
    }
}

# Price Filter Ranges (automatically calculated from product prices)
def get_price_ranges():
    """Dynamically calculate price ranges based on actual product prices"""
    prices = [product['price'] for product in PRODUCTS.values() if product.get('active', True)]
    if not prices:
        return []
    
    min_price = min(prices)
    max_price = max(prices)
    
    # Create dynamic ranges
    ranges = []
    
    # Add "All Prices" option
    ranges.append({'value': '', 'label': 'ფასი'})
    
    # Create ranges based on actual price distribution
    if max_price <= 50:
        ranges.append({'value': f'0-{max_price}', 'label': f'0₾ - {max_price}₾'})
    elif max_price <= 100:
        ranges.extend([
            {'value': f'0-50', 'label': '0₾ - 50₾'},
            {'value': f'50-{max_price}', 'label': f'50₾ - {max_price}₾'}
        ])
    else:
        ranges.extend([
            {'value': '0-50', 'label': '0₾ - 50₾'},
            {'value': '50-100', 'label': '50₾ - 100₾'},
            {'value': '100+', 'label': '100₾ +'}
        ])
    
    return ranges

# Payment Methods Configuration
PAYMENT_METHODS = {
    'later': {
        'name': 'განაწილება 4 თვეზე 0%',
        'options': {
            'bog_later': {
                'name': 'ნაწილ-ნაწილ',
                'bank': 'BOG',
                'icon': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/bog.png',
                'service': None  # Not implemented yet
            },
            'tbc_later': {
                'name': 'განაწილება',
                'bank': 'TBC',
                'icon': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/tbc.png',
                'service': 'tbc_ecommerce'
            }
        }
    },
    'installment': {
        'name': 'განვადება',
        'options': {
            'bog_installment': {
                'name': 'საქართველოს ბანკი',
                'bank': 'BOG',
                'icon': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/bog.png',
                'service': None  # Not implemented yet
            },
            'tbc_installment': {
                'name': 'თიბისი',
                'bank': 'TBC',
                'icon': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/tbc.png',
                'service': 'tbc_installment'
            }
        }
    },
    'card': {
        'name': 'ბარათით გადახდა',
        'options': {
            'tbc_card': {
                'name': 'TBC card',
                'bank': 'TBC',
                'icon': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/tbc.png',
                'service': 'flitt'
            },
            'bog_card': {
                'name': 'BoG card',
                'bank': 'BOG',
                'icon': 'https://raw.githubusercontent.com/AmirejibiIlia/chikori_web_app/refs/heads/main/app/static/images/bog.png',
                'service': 'flitt'
            }
        }
    }
}

# Helper functions
def get_product_by_id(product_id):
    """Get product by ID"""
    return PRODUCTS.get(product_id)

def get_all_products():
    """Get all active products"""
    return [product for product in PRODUCTS.values() if product.get('active', True)]

def get_products_by_category(category):
    """Get products by category"""
    return [product for product in PRODUCTS.values() 
            if product.get('category') == category and product.get('active', True)]

def update_product_price(product_id, new_price):
    """Update product price"""
    if product_id in PRODUCTS:
        PRODUCTS[product_id]['price'] = new_price
        return True
    return False

def add_product(product_data):
    """Add new product"""
    product_id = product_data.get('id')
    if product_id and product_id not in PRODUCTS:
        PRODUCTS[product_id] = product_data
        return True
    return False

def remove_product(product_id):
    """Remove product (soft delete)"""
    if product_id in PRODUCTS:
        PRODUCTS[product_id]['active'] = False
        return True
    return False

def get_payment_methods():
    """Get all payment methods configuration"""
    return PAYMENT_METHODS

def get_payment_service(method_type, option_key):
    """Get payment service for specific method"""
    return PAYMENT_METHODS.get(method_type, {}).get('options', {}).get(option_key, {}).get('service') 