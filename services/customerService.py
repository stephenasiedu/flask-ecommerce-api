from database import db
from models.customer import Customer
from utils.util import encode_token
from werkzeug.security import generate_password_hash, check_password_hash  # Import for password hashing

from sqlalchemy import select

def login(username, password):
    """Log in the customer by validating credentials and generating a token"""
    query = select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and check_password_hash(customer.password, password):  # Compare hashed passwords
        auth_token = encode_token(customer.id, customer.role.role_name)

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return response
    else:
        response = {
            "status": "fail",
            "message": "Invalid username or password"
        }
        return response

def save(customer_data):
    """Create a new customer"""
    customer_data['password'] = generate_password_hash(customer_data['password'])  # Hash the password before saving
    new_customer = Customer(
        name=customer_data['name'], 
        email=customer_data['email'], 
        password=customer_data['password'], 
        phone=customer_data['phone'], 
        username=customer_data['username']
    )
    db.session.add(new_customer)
    db.session.commit()

    db.session.refresh(new_customer)
    return new_customer

def find_all():
    """Get all customers"""
    query = select(Customer)
    all_customers = db.session.execute(query).scalars().all()
    return all_customers

def find_all_paginate(page, per_page):
    """Get paginated list of customers"""
    customers = db.session.execute(
        select(Customer).limit(per_page).offset((page - 1) * per_page)
    ).scalars().all()
    return customers

def add_customer(customer_data):
    """Create a new customer (Similar to `save` method)"""
    return save(customer_data)  # Use the same `save` method to avoid redundancy

def read_customer(customer_data):
    """Read a customer by ID"""
    query = select(Customer).where(Customer.id == customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()
    return customer

def update_customer(customer_data):
    """Update customer details"""
    query = select(Customer).where(Customer.id == customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()

    if customer:
        customer.name = customer_data['name']
        customer.email = customer_data['email']
        customer.password = generate_password_hash(customer_data['password'])  # Hash the new password
        customer.phone = customer_data['phone']
        customer.username = customer_data['username']
        db.session.commit()

    return customer

def delete_customer(customer_data):
    """Delete a customer by ID"""
    query = select(Customer).where(Customer.id == customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()

    if customer:
        db.session.delete(customer)
        db.session.commit()

    return customer
