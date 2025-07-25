"""
Centralized Product Configuration
This is the single source of truth for all product data, prices, and metadata.
"""

# Product Categories
PRODUCT_CATEGORIES = {
    'furniture': {
        'name': 'ავეჯი',
        'description': 'სახლისა და ოფისის ავეჯი'
    }
}

# Product Data - Single source of truth
PRODUCTS = {
    'table': {
        'id': 'table',
        'name': 'სამზარეულოს კუთხე',
        'price': 620,
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
        'id': 'bed',
        'name': 'ტრანსფორმერი მაგიდა',
        'price': 260,
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
        'id': 'sofa',
        'name': 'სამზარეულოს კუთხე',
        'price': 31.00,
        'currency': 'GEL',
        'category': 'furniture',
        'rating': 5.0,
        'image': 'https://zeelproject.com/uploads/posts/2021-02-15/1613392761_2.jpg',
        'sku': 'SOFA_001',
        'description': '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 124x164x83 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> MDF/LMNT<br><strong>ფერი:</strong> ხისფერი (მონაცრისფრო)<br><strong>დამზადების ვადა:</strong> 2 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>',
        'features': ['MDF/LMNT მასალა', 'ხისფერი ფერი', '2 დღე დამზადება'],
        'dimensions': '124x164x83',
        'material': 'MDF/LMNT',
        'color': 'ხისფერი (მონაცრისფრო)',
        'production_time': '2 სამუშაო დღე',
        'delivery': 'აწყობილ მდგომარეობაში',
        'active': False
    },
    'desk': {
        'id': 'desk',
        'name': 'სამუშაო მაგიდა',
        'price': 41.00,
        'currency': 'GEL',
        'category': 'furniture',
        'rating': 4.8,
        'image': 'https://gorgia.ge/images/ab__webp/thumbnails/1223/1000/detailed/65/BM-00141262_jpg.webp',
        'sku': 'DESK_001',
        'description': '<strong>ძირითადი მახასიათებლები</strong><br><br><strong>ზომები:</strong> 140x70x40 - ასევე ვამზადებთ შეკვეთით<br><strong>მასალა:</strong> MDF/LMNT<br><strong>ფერი:</strong> ხისფერი<br><strong>დამზადების ვადა:</strong> 3 სამუშაო დღე<br><strong>მიწოდება:</strong> აწყობილ მდგომარეობაში<br><strong>მიტანის სერვისი</strong>',
        'features': ['MDF/LMNT მასალა', 'ხისფერი ფერი', '3 დღე დამზადება'],
        'dimensions': '140x70x40',
        'material': 'MDF/LMNT',
        'color': 'ხისფერი',
        'production_time': '3 სამუშაო დღე',
        'delivery': 'აწყობილ მდგომარეობაში',
        'active': False
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
        'name': 'განაწილებით',
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