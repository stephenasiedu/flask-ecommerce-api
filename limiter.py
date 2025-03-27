import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from redis import Redis
from werkzeug.exceptions import TooManyRequests

# ----------- Configuration Class ----------- #
# Configuring the app’s settings, keeping them modular and adaptable for various environments.

class Config:
    """
    Configuration class for the Flask app.
    This allows centralized management of configuration variables like Redis connection,
    rate-limiting rules, and general app settings.
    """
    # Redis configuration for rate-limiting storage
    # Adjust these values to your environment as necessary.
    REDIS_HOST = 'localhost'  # Host for the Redis server
    REDIS_PORT = 6379  # Port where Redis server is listening
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"  # Connection URL for Redis

    # Rate-limiting rule: 5 requests per minute per IP
    RATE_LIMIT = "5 per minute"  # Default rate limit rule for endpoints

# ----------- Base Model Setup for SQLAlchemy ----------- #
# Declarative base class for all models. Ensures consistent database schema creation.

class Base(DeclarativeBase):
    """
    Base class for all models, inheriting from SQLAlchemy's DeclarativeBase.
    This is used for creating a consistent schema for all models.
    """
    pass  # This is intentionally left empty. All models will inherit from this.

# Initialize the SQLAlchemy object and link it to the Base model for ORM functionality.
db = SQLAlchemy(model_class=Base)
"""
This initializes the SQLAlchemy object `db` which is tied to the `Base` class.
This allows us to map models to database tables using the ORM system.
"""

# ----------- Application Factory ----------- #
# The app factory pattern allows flexibility and modularity, facilitating testing and configuration.

def create_app():
    """
    Application factory function to create and configure the Flask app.
    This function sets up extensions like Redis, Flask-Limiter for rate-limiting, and SQLAlchemy for database interaction.
    """
    app = Flask(__name__)

    # Load configuration settings from the Config class
    app.config.from_object(Config)

    # ----------- Redis Connection for Rate Limiting ----------- #
    # Redis is used for rate-limiting as a persistent storage solution. 
    # It helps track requests and ensure limits are enforced across different instances of the app.

    try:
        redis_storage = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
        app.logger.info(f"Successfully connected to Redis at {app.config['REDIS_URL']}")
    except Exception as e:
        app.logger.error(f"Error connecting to Redis: {e}")
        raise  # Raise an exception to stop the app if Redis connection fails

    # ----------- Flask-Limiter Setup ----------- #
    # Flask-Limiter is used to implement rate-limiting in the app. Redis will be used as the backend storage for rate limit data.

    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    limiter = Limiter(
        key_func=get_remote_address,  # Using the client IP address as the key for rate-limiting
        storage_uri=app.config['REDIS_URL']  # Storing rate-limit data in Redis
    )
    limiter.init_app(app)  # Bind the limiter to the Flask app to apply rate-limiting

    # ----------- Database Initialization ----------- #
    # Set up SQLAlchemy with Flask. This connects the app to the database and allows ORM functionality.

    db.init_app(app)

    # ----------- Define Routes ----------- #
    # Example route with rate-limiting. This shows how to apply the limiter to specific routes.

    @app.route("/testendpoint")
    @limiter.limit(app.config['RATE_LIMIT'])  # Apply rate limit to this route: 5 requests per minute per IP.
    def some_endpoint():
        """
        A simple test endpoint that is rate-limited. 
        It returns a JSON response with a message indicating it's rate-limited.
        """
        return jsonify({"message": "This is a rate-limited endpoint"}), 200

    # ----------- Error Handling ----------- #
    # Custom error handling for rate-limit exceeded. The error handler sends a friendly response to users.

    @app.errorhandler(TooManyRequests)
    def handle_rate_limit_error(e):
        """
        Handles the 429 Too Many Requests error (rate limit exceeded).
        Returns a user-friendly message when the rate limit is exceeded.
        """
        return jsonify({"error": "Too many requests, please try again later."}), 429

    return app

# ----------- Running the Application ----------- #
# Create the app and start the server. In production, consider using a production-ready WSGI server.

if __name__ == "__main__":
    app = create_app()

    # Run database migrations and table creation if necessary.
    # This is typically done with a migration tool like Flask-Migrate, but for simplicity, we use `db.create_all()`.
    with app.app_context():
        db.create_all()  # Creates tables based on the models defined in the app.

    app.run(debug=True)  # Run the Flask app with debugging enabled for development.
