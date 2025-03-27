from . import ma
from marshmallow import fields, validates, ValidationError

class AccountSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Account data.
    Utilizes SQLAlchemyAutoSchema to automatically generate fields based on the Account model.
    """
    id = fields.Integer(required=False)  # Primary Key is auto-generated and doesn't need to be included in the payload
    name = fields.String(required=True)  # Name of the account holder, mandatory field
    email = fields.Email(required=True)  # Email address, must be a valid email format
    phone = fields.String(required=True)  # Phone number, mandatory field
    username = fields.String(required=True)  # Unique username, mandatory field
    password = fields.String(required=True)  # Password, mandatory field
    role_id = fields.Integer(required=True)  # Foreign key for Role, mandatory field

    class Meta: 
        """
        Meta configuration to specify which fields to include in the schema.
        Excludes password from accounts list for security purposes.
        """
        fields = ("id", "name", "email", "phone", "username", "password", "role_id")

    @validates('password')
    def validate_password(self, value):
        """
        Custom validation to ensure the password is at least 6 characters long.
        Raises a ValidationError if the password doesn't meet the requirement.
        """
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

# Instantiating schemas for single account and multiple accounts (excluding password in multiple accounts)
account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True, exclude=["password"])

class AccountOrderSchema(ma.Schema):
    """
    Schema for serializing and deserializing Account orders.
    This schema is used for returning account order details without sensitive data like passwords.
    """
    order_id = fields.Integer(required=True)  # Order ID, mandatory field
    name = fields.String(required=True)  # Name of the customer, mandatory field
    email = fields.Email(required=True)  # Email address, mandatory field
    order_date = fields.DateTime(required=True)  # Date and time when the order was placed
