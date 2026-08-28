from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.services.business.tax_calculator import IndianGSTTaxCalculator


class CommercialInvoiceGenerator:
    """Generates structured commercial tax invoices for fulfilled orders."""

    @classmethod
    def generate_invoice_document(
        cls,
        order: Any,
        merchant_profile: Optional[Any] = None
    ) -> Dict[str, Any]:
        dest_state = order.shipping_address.state if order.shipping_address else "Karnataka"
        tax_meta = IndianGSTTaxCalculator.compute_gst(order.subtotal_amount, dest_state)

        line_items = []
        for item in order.items:
            line_items.append({
                'sku': item.product_sku,
                'title': item.product_title,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total_price': item.total_price
            })

        return {
            'invoice_number': f"INV-{order.order_number.replace('ORD-', '')}",
            'order_number': order.order_number,
            'invoice_date': order.created_at.strftime('%d %B %Y'),
            'seller_details': {
                'business_name': 'ShopSense AI Merchants Ltd',
                'gstin': '29AAAAA0000A1Z5',
                'address': 'Level 4, Orion Tech Park, Bellandur, Bengaluru, Karnataka - 560103'
            },
            'customer_details': {
                'name': order.shipping_address.name if order.shipping_address else order.customer.full_name,
                'address': f"{order.shipping_address.line1}, {order.shipping_address.city}, {order.shipping_address.state} - {order.shipping_address.postal_code}" if order.shipping_address else "Default Address"
            },
            'line_items': line_items,
            'subtotal': order.subtotal_amount,
            'tax_breakdown': tax_meta,
            'shipping_fee': order.shipping_fee,
            'total_paid': order.total_amount,
            'payment_status': 'PAID (Simulated Transaction)',
            'payment_method': order.payment_method
        }
