from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.role import Role
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(Base):
    """
    This class defines the 'Customers' table and represents customer entities in the system.
    It includes fields such as name, email, phone, username, and password for managing customer accounts.
    """
    __tablename__ = 'Customers'  # Table name in the database
    
    # Customer fields with column type, length, and constraints
    id: Mapped[int] = mapped_column(primary_key=True)  # Unique identifier for the customer
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)  # Customer's full name
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False, index=True)  # Unique email with an index for faster lookups
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)  # Customer's phone number
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)  # Unique username for login
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)  # Store the hashed password
    role_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Roles.id'), nullable=False)  # Foreign key referencing the 'Roles' table

    # Relationships with other entities
    role: Mapped["Role"] = relationship("Role", back_populates="customers")  # Relationship with the 'Role' table
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer", cascade="all, delete-orphan")  # One-to-many relationship with orders, with cascading deletes for orphaned orders

    # __repr__ method for better debugging and logging
    def __repr__(self):
        """
        Provides a string representation of the Customer instance for easier inspection during debugging.
        """
        return f"<Customer(id={self.id}, name={self.name}, email={self.email}, username={self.username})>"

    # Method to hash the password before saving it to the database
    def set_password(self, password: str):
        """
        Hashes the provided password using Werkzeug's hashing function before storing it.
        Ensures that the password is securely stored in the database.
        """
        self.password = generate_password_hash(password)  # Hashing password using werkzeug.security

    # Method to check if the provided password matches the stored hash
    def check_password(self, password: str) -> bool:
        """
        Compares the provided password with the stored hashed password to validate login.
        Returns True if the password matches, otherwise False.
        """
        return check_password_hash(self.password, password)  # Verifies the hashed password using werkzeug.security
