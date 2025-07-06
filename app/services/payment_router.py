"""
Dynamic Payment Router
Routes payment requests to the appropriate service based on configuration
"""

from config.products import get_payment_service, get_product_by_id
from app.services.flitt_service import create_flitt_payment
from app.services.tbc_installment_service import create_tbc_installment_application
from app.services.tbc_ecommerce_service import create_tbc_ecommerce_payment

class PaymentRouter:
    """Routes payment requests to appropriate services"""
    
    def __init__(self):
        self.services = {
            'flitt': create_flitt_payment,
            'tbc_installment': create_tbc_installment_application,
            'tbc_ecommerce': create_tbc_ecommerce_payment
        }
    
    def route_payment(self, method_type, option_key, product_id, amount, **kwargs):
        """
        Route payment to appropriate service
        
        Args:
            method_type: 'later', 'installment', or 'card'
            option_key: specific option like 'tbc_card', 'bog_installment', etc.
            product_id: product ID
            amount: payment amount
            **kwargs: additional parameters for specific services
        
        Returns:
            Payment result from the appropriate service
        """
        try:
            # Get the service name for this payment method
            service_name = get_payment_service(method_type, option_key)
            
            if not service_name:
                return {
                    'success': False,
                    'error': f'Payment method {method_type}/{option_key} not implemented'
                }
            
            # Get the service function
            service_func = self.services.get(service_name)
            
            if not service_func:
                return {
                    'success': False,
                    'error': f'Service {service_name} not found'
                }
            
            # Validate product exists
            product = get_product_by_id(product_id)
            if not product:
                return {
                    'success': False,
                    'error': 'Product not found'
                }
            
            # Route to appropriate service
            if service_name == 'flitt':
                return service_func(product_id, amount)
            elif service_name == 'tbc_installment':
                return service_func(product_id, amount, kwargs.get('user_ip_address'))
            elif service_name == 'tbc_ecommerce':
                return service_func(product_id, amount, kwargs.get('user_ip_address'))
            else:
                return {
                    'success': False,
                    'error': f'Unknown service: {service_name}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Payment routing error: {str(e)}'
            }
    
    def get_available_services(self):
        """Get list of available payment services"""
        return list(self.services.keys())
    
    def is_service_available(self, service_name):
        """Check if a service is available"""
        return service_name in self.services

# Global payment router instance
payment_router = PaymentRouter() 