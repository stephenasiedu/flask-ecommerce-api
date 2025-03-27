from datetime import datetime, timedelta, timezone
import jwt
from flask import jsonify, request
from functools import wraps

# Secret key used for JWT encoding/decoding
SECRET_KEY = "super_secret_secrets"

def encode_token(user_id, role):
    """
    Generate a JWT token for a given user_id and role.
    
    Args:
        user_id (str): Unique identifier for the user.
        role (str): Role of the user (e.g., "Admin", "User").
    
    Returns:
        str: Encoded JWT token.
    """
    # Define the token payload with expiration time (1 hour) and issue time
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),  # Expires in 1 hour
        'iat': datetime.now(timezone.utc),  # Issued at the current time
        'sub': user_id,  # Subject - user identifier
        'role': role  # User's role
    }

    # Generate and return the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(func):
    """
    Decorator to ensure that the request contains a valid JWT token.
    
    This function extracts the token from the Authorization header,
    verifies it, and allows access to the protected route if the token is valid.
    
    Args:
        func (function): The original route handler that is being wrapped by this decorator.
    
    Returns:
        function: The wrapper function that checks token validity before calling the original route handler.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        # Check if the Authorization header is present
        if 'Authorization' in request.headers:
            try:
                # Extract the token from the header
                token = request.headers['Authorization'].split()[1]
                # Decode the token and validate it
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("Payload:", payload)  # Optionally log the payload for debugging purposes
            except jwt.ExpiredSignatureError:
                # Handle token expiration error
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                # Handle invalid token error
                return jsonify({"message": "Invalid Token"}), 401
            # If token is valid, proceed with the original function
            return func(*args, **kwargs)
        else:
            # If no token is found in the headers, return a 401 Unauthorized response
            return jsonify({"message": "Token Authorization Required"}), 401
    return wrapper

def user_token_wrapper(func):
    """
    Decorator to ensure the request contains a valid JWT token and passes the user ID to the route handler.
    
    This function extracts the token from the Authorization header, verifies it,
    and allows access to the protected route if the token is valid. It also provides 
    the decoded user ID to the route handler.
    
    Args:
        func (function): The original route handler that is being wrapped by this decorator.
    
    Returns:
        function: The wrapper function that checks token validity and provides the user ID to the handler.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        # Check if the Authorization header is present
        if 'Authorization' in request.headers:
            try:
                # Extract the token from the header
                token = request.headers['Authorization'].split()[1]
                # Decode the token and validate it
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("Payload:", payload)  # Optionally log the payload for debugging purposes
            except jwt.ExpiredSignatureError:
                # Handle token expiration error
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                # Handle invalid token error
                return jsonify({"message": "Invalid Token"}), 401
            # If token is valid, pass the user ID to the wrapped function
            return func(token_id=payload['sub'], *args, **kwargs)
        else:
            # If no token is found in the headers, return a 401 Unauthorized response
            return jsonify({"message": "Token Authorization Required"}), 401
    return wrapper

def admin_required(func):
    """
    Decorator to ensure that the request contains a valid JWT token and that the user has the 'Admin' role.
    
    This function checks the role of the user in the decoded JWT token and allows access 
    only if the user has the 'Admin' role.
    
    Args:
        func (function): The original route handler that is being wrapped by this decorator.
    
    Returns:
        function: The wrapper function that checks token validity and role before calling the handler.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        # Check if the Authorization header is present
        if 'Authorization' in request.headers:
            try:
                # Extract the token from the header
                token = request.headers['Authorization'].split()[1]
                # Decode the token and validate it
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("Payload:", payload)  # Optionally log the payload for debugging purposes
            except jwt.ExpiredSignatureError:
                # Handle token expiration error
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                # Handle invalid token error
                return jsonify({"message": "Invalid Token"}), 401
            
            # Check if the user has the 'Admin' role
            if payload['role'] == 'Admin':
                # If valid, proceed with the original function
                return func(*args, **kwargs)
            else:
                # If the user doesn't have the 'Admin' role, return a 401 Unauthorized response
                return jsonify({"message": "Admin role required"}), 401
        else:
            # If no token is found in the headers, return a 401 Unauthorized response
            return jsonify({"message": "Token Authorization Required"}), 401
    return wrapper
