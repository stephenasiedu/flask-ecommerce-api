from database import db, Base

# Association table for the many-to-many relationship between Orders and Products
# This table connects the 'Orders' table and the 'Products' table, allowing each order to have multiple products and vice versa.
order_product = db.Table(
    'Order_Product',  # Name of the association table in the database
    Base.metadata,    # Base metadata that stores table and column definitions
    db.Column('order_id', db.ForeignKey("Orders.id"), primary_key=True),  # Foreign key referencing the 'Orders' table, forming a many-to-many link
    db.Column('product_id', db.ForeignKey("Products.id"), primary_key=True)  # Foreign key referencing the 'Products' table, forming a many-to-many link
)
