from marshmallow import Schema, fields, validate


class CopilotMessageSchema(Schema):
    conversation_id = fields.Integer(required=False, allow_none=True)
    message = fields.String(required=True, validate=validate.Length(min=1, max=2000))
