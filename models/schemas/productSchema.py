from marshmallow import fields, validate
from . import ma

class ProductSchema(ma.Schema):
    """
    Schema for serializing and deserializing Product data.
    This schema validates and represents the Product object in the system.
    """
    id = fields.Integer(required=False)  # Product ID, not required as it is auto-generated in the database
    name = fields.String(required=False)  # Product name, optional field for serialization
    price = fields.Integer(required=True)  # Product price, required field to ensure product has a valid price

    class Meta:
        """
        Meta configuration to specify which fields should be included in the serialized representation of the product.
        """
        fields = ("id", 'name', 'price')  # Fields to include in the output

# Instantiating schemas for a single product and a list of products
product_schema = ProductSchema()  # Single product schema for serialization/deserialization
products_schema = ProductSchema(many=True)  # Schema for serializing/deserializing a list of products
