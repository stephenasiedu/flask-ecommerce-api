from flask_caching import Cache
import os

# Initialize Cache object. The cache configuration will be set up later within the app.
cache = Cache()

def init_cache(app):
    """
    Initialize caching for the Flask app. This function configures the caching mechanism 
    based on the application’s environment settings.
    
    :param app: The Flask app instance that will be configured.
    """
    # Fetch the cache type from the application's configuration, defaulting to 'SimpleCache'
    # SimpleCache is suitable for development or lightweight caching. Other options could include 
    # Redis or Memcached for production environments.
    cache_type = app.config.get('CACHE_TYPE', 'SimpleCache')

    # Initialize the cache with the appropriate configuration.
    # The 'CACHE_TYPE' is dynamically chosen based on the app’s environment, ensuring flexibility.
    cache.init_app(app, config={'CACHE_TYPE': cache_type})

    # Log the cache initialization with the chosen cache type, this helps with monitoring and debugging.
    app.logger.info(f"Cache initialized with type: {cache_type}")
