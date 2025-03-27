from database import db
from models.order import Order
from models.customer import Customer
from models.product import Product
from sqlalchemy import select
from datetime import date

def save(order_data):
    """Save a new order."""
    new_order = Order(date=date.today(), customer_id=order_data["customer_id"])

    for item_id in order_data['products_ids']:
        # Fetch product and check if it exists
        query = select(Product).filter(Product.id == item_id)
        item = db.session.execute(query).scalar_one_or_none()  # Use scalar_one_or_none() to fetch one product
        if item:
            new_order.products.append(item)
        else:
            print(f"Product with ID {item_id} not found.")  # Log product not found

    db.session.add(new_order)
    db.session.commit()

    db.session.refresh(new_order)
    return new_order

def find_all():
    """Find all orders."""
    query = select(Order)
    all_orders = db.session.execute(query).scalars().all()
    return all_orders

def find_by_id(id):
    """Find order by its ID."""
    query = select(Order).where(Order.id == id)
    order = db.session.execute(query).scalar_one_or_none()  # Use scalar_one_or_none to get a single result
    return order

def find_by_customer_id(id):
    """Find all orders by customer ID."""
    query = select(Order).where(Order.customer_id == id)
    orders = db.session.execute(query).scalars().all()
    return orders

def find_by_customer_email(email):
    """Find all orders by customer email."""
    query = select(Order).join(Customer).where(Customer.id == Order.customer_id).filter(Customer.email == email)
    orders = db.session.execute(query).scalars().all()
    return orders

def place_order(order_data):
    """Place a new order (Similar to save but might be called with different logic in the future)."""
    new_order = Order(date=date.today(), customer_id=order_data["customer_id"])

    for item_id in order_data['products_ids']:
        query = select(Product).filter(Product.id == item_id)
        item = db.session.execute(query).scalar_one_or_none()  # Fetch product and check if it exists
        if item:
            new_order.products.append(item)
        else:
            print(f"Product with ID {item_id} not found.")  # Log product not found

    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)

    return new_order  # Return the new order for confirmation

def retrieve_order(id):
    """Retrieve an order by ID."""
    query = select(Order).where(Order.id == id)
    order = db.session.execute(query).scalar_one_or_none()  # Use scalar_one_or_none to get one order
    return order
