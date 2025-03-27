from flask import Blueprint
from controllers.accountController import (
    save, 
    find_all, 
    find_all_paginate, 
    login, 
    add_account, 
    update_account, 
    delete_account, 
    read_accounts
)

# Create a new Blueprint for the 'account' routes
account_blueprint = Blueprint('account_bp', __name__)

# Route for creating a new account (POST request)
account_blueprint.route('/', methods=['POST'])(save)

# Route to get all accounts (GET request)
account_blueprint.route('/', methods=['GET'])(find_all)

# Route to get accounts with pagination (GET request)
account_blueprint.route('/paginate', methods=['GET'])(find_all_paginate)

# Route for user login (POST request)
account_blueprint.route('/login', methods=['POST'])(login)

# Route for adding a new account (POST request)
account_blueprint.route('/', methods=['POST'])(add_account)

# Route to update an existing account (POST request)
account_blueprint.route('/update', methods=['POST'])(update_account)

# Route for deleting an account (DELETE request)
account_blueprint.route('/delete', methods=['DELETE'])(delete_account)

# Route to read accounts (GET request)
account_blueprint.route('/', methods=['GET'])(read_accounts)
