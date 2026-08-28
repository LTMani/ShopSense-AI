from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class CouponEngine:
    """Multi-tiered discount coupon verification and discount calculator."""

    AVAILABLE_COUPONS = {
        'FIRST10': {
            'code': 'FIRST10',
            'discount_pct': 10.0,
            'max_discount': 2000.0,
            'min_cart_amount': 2999.0,
            'first_order_only': True,
            'description': '10% off on your first order up to ₹2,000'
        },
        'STUDENTAI': {
            'code': 'STUDENTAI',
            'discount_pct': 15.0,
            'max_discount': 3500.0,
            'min_cart_amount': 5000.0,
            'first_order_only': False,
            'description': '15% student discount up to ₹3,500 on study essentials'
        },
        'FLAT500': {
            'code': 'FLAT500',
            'flat_amount': 500.0,
            'min_cart_amount': 4999.0,
            'first_order_only': False,
            'description': 'Flat ₹500 instant discount on orders above ₹4,999'
        },
        'TECHFEST': {
            'code': 'TECHFEST',
            'discount_pct': 8.0,
            'max_discount': 5000.0,
            'min_cart_amount': 15000.0,
            'first_order_only': False,
            'description': '8% discount up to ₹5,000 on high-performance laptops & monitors'
        }
    }

    @classmethod
    def apply_coupon(
        cls,
        code: str,
        cart_subtotal: float,
        is_first_order: bool = False
    ) -> Dict[str, Any]:
        code_upper = code.strip().upper()
        rule = cls.AVAILABLE_COUPONS.get(code_upper)

        if not rule:
            return {
                'valid': False,
                'discount_amount': 0.0,
                'message': f"Coupon code '{code}' is invalid or expired."
            }

        if cart_subtotal < rule['min_cart_amount']:
            return {
                'valid': False,
                'discount_amount': 0.0,
                'message': f"Minimum cart subtotal of ₹{rule['min_cart_amount']:,.0f} required for coupon '{code_upper}'."
            }

        if rule.get('first_order_only') and not is_first_order:
            return {
                'valid': False,
                'discount_amount': 0.0,
                'message': f"Coupon '{code_upper}' is only applicable on your first purchase."
            }

        # Calculate discount
        if 'flat_amount' in rule:
            discount = float(rule['flat_amount'])
        else:
            discount = (cart_subtotal * (rule['discount_pct'] / 100.0))
            if 'max_discount' in rule:
                discount = min(discount, rule['max_discount'])

        discount = round(discount, 2)
        new_subtotal = max(0.0, round(cart_subtotal - discount, 2))

        return {
            'valid': True,
            'coupon_code': code_upper,
            'discount_amount': discount,
            'discount_description': rule['description'],
            'new_subtotal': new_subtotal,
            'message': f"Applied coupon '{code_upper}'! You saved ₹{discount:,.2f}."
        }
