from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Role(Base):
    __tablename__ = "Roles"  # The name of the table in the database

    # Primary key for the Role table
    id: Mapped[int] = mapped_column(primary_key=True)  # 'id' is the unique identifier for each role

    # Role name with a maximum length of 100 characters, ensuring uniqueness
    role_name: Mapped[str] = mapped_column(db.String(100), unique=True)  # 'role_name' stores the name of the role, it must be unique across all roles
