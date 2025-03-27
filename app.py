import os
from flask import Flask
from flask_cors import CORS
from database import db
from models.schemas import ma
from limiter import limiter
from caching import cache
from flask_swagger_ui import get_swaggerui_blueprint

# Import route blueprints for different modules in the application
from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.accountBP import account_blueprint

# Swagger UI Setup for API Documentation
SWAGGER_URL = '/api/docs'  # URL endpoint for the Swagger UI documentation
API_URL = '/static/swagger.yaml'  # Path to the Swagger YAML file containing API specifications

# Register the Swagger UI blueprint for interactive API documentation
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "E-commerce API"})

def create_app(config_name='ProductionConfig'):
    """
    Factory method to create and configure the Flask application.

    :param config_name: The configuration to use for the app (defaults to 'ProductionConfig')
    :return: The Flask app instance
    """
    app = Flask(__name__)

    # Dynamically load configuration settings based on the environment
    # Uses an environment variable to determine the correct configuration class
    config_class = os.getenv('FLASK_CONFIG', config_name)
    app.config.from_object(f'config.{config_class}')
    
    # Initialize various extensions for database, serialization, caching, etc.
    db.init_app(app)  # Initialize the database (SQLAlchemy)
    ma.init_app(app)  # Initialize Marshmallow (for serialization)
    limiter.init_app(app)  # Initialize rate limiting for API requests
    cache.init_app(app)  # Initialize caching for improved performance
    CORS(app)  # Enable Cross-Origin Resource Sharing for the application

    # Configure the rate limiter for the application globally
    # The rate limit configuration ensures that the app does not get overloaded
    rate_limit_config()

    # Register blueprints for modular route management across various resources
    blueprint_config(app)

    return app

def blueprint_config(app):
    """
    Register the route blueprints for different API endpoints of the application.

    :param app: The Flask app instance
    """
    # Register each blueprint under their respective URL prefixes
    # This modular approach helps in organizing the code efficiently
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(account_blueprint, url_prefix='/account')

    # Register the Swagger UI documentation blueprint to visualize API docs
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

def rate_limit_config():
    """
    Configure the global rate limiting for the application.
    This helps prevent abuse and limits excessive API calls.
    """
    # The global rate limit is set to 100 requests per day across the entire app
    limiter.limit("100 per day")

# Factory method that creates the app with the configuration 'ProductionConfig' by default
app = create_app(config_name=os.getenv('FLASK_ENV', 'ProductionConfig'))

# Database initialization section (recommended for development environments only)
# Note: Dropping and recreating tables on each startup is not ideal for production.
#       Database migrations should be handled via Flask-Migrate in production environments.
with app.app_context():
    # Caution: Dropping and creating all tables on every startup is only for development and debugging
    # db.drop_all()  # Uncomment for development/debugging only
    db.create_all()  # Creates all database tables for the app

# Run the application in debug mode if the environment configuration allows it
if __name__ == '__main__':
    # Running the app in debug mode allows for easier debugging and error tracing
    app.run(debug=app.config['DEBUG'])
