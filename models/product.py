from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    __tablename__ = "Products"  # The name of the table in the database

    # Primary key for the Product table
    id: Mapped[int] = mapped_column(primary_key=True)  # 'id' is the unique identifier for each product

    # Product name with a maximum length of 225 characters, not nullable
    name: Mapped[str] = mapped_column(db.String(225), nullable=False)  # 'name' of the product; it cannot be empty

    # Product price, not nullable, of type Float
    price: Mapped[float] = mapped_column(db.Float, nullable=False)  # 'price' stores the price of the product; it cannot be empty

    # String representation for easy debugging
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"  # Displays a readable string for debugging
