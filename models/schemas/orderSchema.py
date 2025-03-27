from marshmallow import fields
from . import ma

class OrderSchema(ma.Schema):
    """
    Schema for serializing and deserializing Order data.
    It defines how an order object is represented and validates the data during serialization/deserialization.
    """
    id = fields.Integer(required=False)  # Order ID, not required as it is auto-generated in the database
    date = fields.Date(required=False)  # Date when the order was placed, optional field
    customer_id = fields.Integer(required=True)  # Foreign key for Customer, mandatory field
    products = fields.Nested('ProductSchema', many=True)  # Nested schema for products related to the order (many-to-many relationship)
    customer = fields.Nested('CustomerOrderSchema')  # Nested schema for customer details, returns a minimal representation

    class Meta:
        """
        Meta configuration to specify the fields that should be included when serializing the order object.
        """
        fields = ("id", 'date', 'customer_id', 'products', 'customer')

# Instantiate schemas for a single order and a list of orders
order_schema = OrderSchema()  # Single order
orders_schema = OrderSchema(many=True)  # List of orders
