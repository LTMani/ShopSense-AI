from marshmallow import Schema, fields, validate


class CheckoutSchema(Schema):
    shipping_name = fields.String(required=True, validate=validate.Length(min=2, max=150))
    shipping_phone = fields.String(required=False, allow_none=True)
    shipping_address_line1 = fields.String(required=True, validate=validate.Length(min=3, max=255))
    shipping_city = fields.String(required=True, validate=validate.Length(min=2, max=100))
    shipping_state = fields.String(required=True, validate=validate.Length(min=2, max=100))
    shipping_postal_code = fields.String(required=True, validate=validate.Length(min=3, max=20))
    payment_method = fields.String(required=False, load_default='simulated_upi')
