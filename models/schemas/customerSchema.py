from . import ma
from marshmallow import fields, validates, ValidationError

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Customer data.
    Utilizes SQLAlchemyAutoSchema to automatically generate fields based on the Customer model.
    """
    id = fields.Integer(required=False)  # Primary Key is auto-generated and doesn't need to be included in the payload
    name = fields.String(required=True)  # Name of the customer, mandatory field
    email = fields.Email(required=True)  # Email address, must be a valid email format
    phone = fields.String(required=True)  # Phone number, mandatory field
    username = fields.String(required=True)  # Unique username, mandatory field
    password = fields.String(required=True)  # Password, mandatory field
    role_id = fields.Integer(required=True)  # Foreign key for Role, mandatory field

    class Meta: 
        """
        Meta configuration to specify which fields to include in the schema.
        Excludes password from customer list for security purposes.
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

# Instantiating schemas for single customer and multiple customers (excluding password in multiple customers)
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True, exclude=["password"])

class CustomerOrderSchema(ma.Schema):
    """
    Schema for serializing and deserializing Customer order data.
    Used for returning customer order details without sensitive data like passwords.
    """
    order_id = fields.Integer(required=True)  # Order ID, mandatory field
    name = fields.String(required=True)  # Name of the customer, mandatory field
    email = fields.Email(required=True)  # Email address, mandatory field
    order_date = fields.DateTime(required=True)  # Date and time when the order was placed
