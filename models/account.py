from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from models.role import Role
from sqlalchemy import String, Integer

class Account(Base):
    """
    This class defines the 'Accounts' table and represents the Account entity in the system.
    It includes fields such as name, email, phone, username, and password for managing user accounts.
    """
    __tablename__ = 'Accounts'  # Table name in the database

    # Account fields with column type, length, and constraints
    id: Mapped[int] = mapped_column(primary_key=True)  # Unique identifier for the account
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # Account owner's name
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)  # Email is unique and indexed for faster searches
    phone: Mapped[str] = mapped_column(String(20), nullable=False)  # Phone number for the account holder
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)  # Unique username for login
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # Store the hashed password
    role_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('Roles.id'), nullable=False)  # Foreign key referencing the 'Roles' table

    # Relationships with other entities
    role: Mapped["Role"] = relationship("Role", back_populates="accounts")  # Relationship with the 'Role' table
    customers: Mapped[List["Customer"]] = relationship("Customer", back_populates="account", cascade="all, delete-orphan")  # One-to-many relationship with customers, with cascading deletes

    # Optional: __repr__ method for easier debugging and logging
    def __repr__(self):
        return f"<Account(id={self.id}, name={self.name}, email={self.email}, username={self.username})>"

    # Optional: Method to hash the password before storing in the database
    def set_password(self, password: str):
        """
        Hashes the given password before saving it.
        Ensure you implement the hash_password function using a secure method (e.g., bcrypt).
        """
        self.password = hash_password(password)  # Make sure to implement the hash_password function elsewhere

    # Optional: Method to verify the password during login
    def check_password(self, password: str) -> bool:
        """
        Compares the provided password with the stored hashed password.
        You should implement the check_password_hash function to securely compare the passwords.
        """
        return check_password_hash(password, self.password)  # Implement the check_password_hash function
