from models.product import Product
from database import db
from sqlalchemy import select

def save(product_data):
    """Save a new product."""
    new_product = Product(name=product_data['name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    db.session.refresh(new_product)

    return new_product

def find_all():
    """Find all products."""
    query = select(Product)
    all_products = db.session.execute(query).scalars().all()
    return all_products

def search_product(search_term):
    """Search for products based on a search term."""
    query = select(Product).where(Product.name.like(f'%{search_term}%'))
    search_products = db.session.execute(query).scalars().all()
    return search_products

def read_product(product_id):
    """Read a product by its ID."""
    query = select(Product).where(Product.id == product_id)
    product = db.session.execute(query).scalar_one_or_none()  # Use scalar_one_or_none for a single result
    return product

def update_product(product_data):
    """Update an existing product."""
    query = select(Product).where(Product.id == product_data['id'])
    product = db.session.execute(query).scalar_one_or_none()

    if product:  # Check if product exists
        product.name = product_data['name']
        product.price = product_data['price']
        db.session.commit()
        return product
    else:
        return None  # Return None if product not found

def delete_product(product_id):
    """Delete a product by its ID."""
    query = select(Product).where(Product.id == product_id)
    product = db.session.execute(query).scalar_one_or_none()

    if product:  # Check if product exists
        db.session.delete(product)
        db.session.commit()
        return product
    else:
        return None  # Return None if product not found

def list_products():
    """List all products."""
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products
