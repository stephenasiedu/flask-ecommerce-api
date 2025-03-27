import pytest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash, check_password_hash
from services.customerService import login as customer_login
from services.accountService import login as account_login
from services.productService import create_product
from services.orderService import create_order
from faker import Faker

# Create a Faker instance for generating random data
faker = Faker()

@pytest.fixture
def mock_customer():
    """Mock the customer database call"""
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
    mock_user.username = faker.user_name()
    mock_user.password = generate_password_hash(faker.password())
    return mock_user

@pytest.fixture
def mock_account():
    """Mock the account database call"""
    mock_account = MagicMock()
    mock_account.id = 1
    mock_account.roles = [MagicMock(role_name='admin'), MagicMock(role_name='user')]
    mock_account.username = faker.user_name()
    mock_account.password = generate_password_hash(faker.password())
    return mock_account

@pytest.fixture
def mock_product():
    """Mock the product database call"""
    mock_product = MagicMock()
    mock_product.id = 1
    mock_product.name = faker.word()
    mock_product.price = faker.random_number(digits=2)
    return mock_product

@pytest.fixture
def mock_order():
    """Mock the order database call"""
    mock_order = MagicMock()
    mock_order.id = 1
    mock_order.customer_id = 1
    mock_order.product_id = 1
    mock_order.quantity = 2
    return mock_order

def test_login_customer(mock_customer):
    """Test login functionality for customer"""
    # Mock the return value of the db query
    with patch('services.customerService.db.session.execute') as mock_customer_query:
        mock_customer_query.return_value.scalar_one_or_none.return_value = mock_customer
        
        # Call the function and assert the response
        response = customer_login(mock_customer.username, mock_customer.password)
        
        # Check if the customer login was successful
        assert response['status'] == 'success'  # or 'fail' based on the login function behavior

def test_login_account(mock_account):
    """Test login functionality for account"""
    # Mock the return value of the db query
    with patch('services.accountService.db.session.execute') as mock_account_query:
        mock_account_query.return_value.scalar_one_or_none.return_value = mock_account
        
        # Call the function and assert the response
        response = account_login(mock_account.username, mock_account.password)
        
        # Check if the account login was successful
        assert response['status'] == 'success'  # or 'fail' based on the login function behavior

def test_create_product(mock_product):
    """Test product creation functionality"""
    # Mock the return value of the db query
    with patch('services.productService.db.session.add') as mock_add_product:
        mock_add_product.return_value = mock_product
        
        # Call the function and assert the response
        response = create_product(mock_product)
        
        # Check if product creation was successful
        assert response['status'] == 'success'  # Update based on actual function response

def test_create_order(mock_order):
    """Test order creation functionality"""
    # Mock the return value of the db query
    with patch('services.orderService.db.session.add') as mock_add_order:
        mock_add_order.return_value = mock_order
        
        # Call the function and assert the response
        response = create_order(mock_order)
        
        # Check if order creation was successful
        assert response['status'] == 'success'  # Update based on actual function response
