from flask import Blueprint
from controllers.customerController import (
    save, 
    find_all, 
    find_all_paginate, 
    login, 
    add_customer, 
    update_customer, 
    delete_customer, 
    read_customer
)

# Create a new Blueprint for the 'customer' routes
customer_blueprint = Blueprint('customer_bp', __name__)

# Route for creating a new customer (POST request)
customer_blueprint.route('/', methods=['POST'])(save)

# Route to get all customers (GET request)
customer_blueprint.route('/', methods=['GET'])(find_all)

# Route to get customers with pagination (GET request)
customer_blueprint.route('/paginate', methods=['GET'])(find_all_paginate)

# Route for customer login (POST request)
customer_blueprint.route('/login', methods=['POST'])(login)

# Route for adding a new customer (POST request)
customer_blueprint.route('/', methods=['POST'])(add_customer)

# Route to read customer details (GET request)
customer_blueprint.route('/', methods=['GET'])(read_customer)

# Route to update an existing customer (POST request)
customer_blueprint.route('/update', methods=['POST'])(update_customer)

# Route for deleting a customer (DELETE request)
customer_blueprint.route('/', methods=['DELETE'])(delete_customer)
