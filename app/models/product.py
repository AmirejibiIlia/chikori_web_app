from config.products import get_product_by_id as get_product_by_id_config, get_all_products as get_all_products_config

def get_product_by_id(product_id):
    """Get product details by ID"""
    return get_product_by_id_config(product_id)

def get_all_products():
    """Get all products"""
    return get_all_products_config() 