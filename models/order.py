from typing import List
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.orderProduct import order_product  # Import association table for the many-to-many relationship
from models.product import Product  # Import Product model for the many-to-many relationship
from models.customer import Customer  # Import Customer model for the relationship

class Order(Base):
    """
    The 'Order' class represents an order placed by a customer.
    It contains fields such as the order ID, date, and a relationship to the customer who placed the order.
    Additionally, it has a many-to-many relationship with products via the order_product association table.
    """
    __tablename__ = 'Orders'  # Table name in the database

    # Order fields with column types, constraints, and relationships
    id: Mapped[int] = mapped_column(primary_key=True)  # Unique identifier for the order
    date: Mapped[str] = mapped_column(db.Date, nullable=False)  # The date the order was placed (stored as a db.Date for proper date handling)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'))  # Foreign key referencing the 'Customers' table
    
    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")  # Many-to-one relationship with the Customer table
    products: Mapped[List["Product"]] = relationship("Product", secondary=order_product, lazy="subquery")  # Many-to-many relationship with the Product table through the 'order_product' association table

    # __repr__ method for better debugging and logging
    def __repr__(self):
        """
        Provides a string representation of the Order instance for easier inspection during debugging.
        """
        return f"<Order(id={self.id}, date={self.date}, customer_id={self.customer_id})>"
