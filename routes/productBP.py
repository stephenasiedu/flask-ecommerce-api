from flask import Blueprint
from controllers.productController import (
    find_all, 
    save, 
    List_products, 
    add_product, 
    update_product, 
    delete_product
)

# Create a new Blueprint for the 'product' routes
product_blueprint = Blueprint('product_bp', __name__)

# Route for creating a new product (POST request)
product_blueprint.route('/', methods=['POST'])(save)

# Route for fetching all products (GET request)
product_blueprint.route('/', methods=['GET'])(find_all)

# Route for adding a new product (POST request)
product_blueprint.route('/add', methods=['POST'])(add_product)

# Route for updating a product (PUT/PATCH request)
product_blueprint.route('/update', methods=['POST'])(update_product)

# Route for listing products (GET request)
product_blueprint.route('/list', methods=['GET'])(List_products)

# Route for deleting a product (DELETE request)
product_blueprint.route('/search', methods=['DELETE'])(delete_product)
