from database import db
from models.account import Account
from utils.util import encode_token
from werkzeug.security import generate_password_hash, check_password_hash  # Import for password hashing

from sqlalchemy import select

def login(username, password):
    """Log in the user by validating credentials and generating a token"""
    query = select(Account).where(Account.username == username)
    account = db.session.execute(query).scalar_one_or_none()

    if account and check_password_hash(account.password, password):  # Compare hashed passwords
        auth_token = encode_token(account.id, account.role.role_name)

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

def save(account_data):
    """Create a new account"""
    account_data['password'] = generate_password_hash(account_data['password'])  # Hash password
    new_account = Account(
        name=account_data['name'], 
        email=account_data['email'], 
        password=account_data['password'], 
        phone=account_data['phone'], 
        username=account_data['username']
    )
    db.session.add(new_account)
    db.session.commit()

    db.session.refresh(new_account)
    return new_account

def find_all():
    """Get all accounts"""
    query = select(Account)
    all_accounts = db.session.execute(query).scalars().all()
    return all_accounts

def find_all_paginate(page, per_page):
    """Get paginated list of accounts"""
    accounts = db.session.execute(
        select(Account).limit(per_page).offset((page - 1) * per_page)
    ).scalars().all()
    return accounts

def add_account(account_data):
    """Alias for saving a new account (can merge with `save` method)"""
    account_data['password'] = generate_password_hash(account_data['password'])
    new_account = Account(
        name=account_data['name'], 
        email=account_data['email'], 
        password=account_data['password'], 
        phone=account_data['phone'], 
        username=account_data['username']
    )
    db.session.add(new_account)
    db.session.commit()

    db.session.refresh(new_account)
    return new_account

def read_account(account_data):
    """Read an account by ID"""
    query = select(Account).where(Account.id == account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    return account

def update_account(account_data):
    """Update account details"""
    query = select(Account).where(Account.id == account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    
    if account:
        account.name = account_data['name']
        account.email = account_data['email']
        account.password = generate_password_hash(account_data['password'])  # Hash new password
        account.phone = account_data['phone']
        account.username = account_data['username']
        db.session.commit()

    return account

def delete_account(account_data):
    """Delete an account by ID"""
    query = select(Account).where(Account.id == account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    
    if account:
        db.session.delete(account)
        db.session.commit()
    
    return account
