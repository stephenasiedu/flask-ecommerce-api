from flask import Blueprint
from controllers.orderController import (
    find_all, 
    save, 
    find_by_id, 
    find_by_customer_id, 
    find_by_customer_email, 
    place_order, 
    retrieve_order
)

# Create a new Blueprint for the 'order' routes
order_blueprint = Blueprint('order_bp', __name__)

# Route for creating a new order (POST request)
order_blueprint.route('/', methods=['POST'])(save)

# Route for fetching all orders (GET request)
order_blueprint.route('/', methods=['GET'])(find_all)

# Route for fetching a specific order by its ID (GET request)
order_blueprint.route('/<int:id>', methods=['GET'])(find_by_id)

# Route for fetching orders by a customer's ID (GET request)
order_blueprint.route('/customer/<int:id>', methods=['GET'])(find_by_customer_id)

# Route for fetching orders by a customer's email (POST request)
order_blueprint.route('/customer/email', methods=['POST'])(find_by_customer_email)

# Route for placing an order (POST request)
order_blueprint.route('/<int:id>', methods=['POST'])(place_order)

# Route for retrieving a specific order (GET request)
order_blueprint.route('/retrieve', methods=['GET'])(retrieve_order)
