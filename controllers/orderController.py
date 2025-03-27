from flask import jsonify, request
from models.schemas.orderSchema import order_schema, orders_schema
from marshmallow import ValidationError
from services import orderService
from utils.util import token_required, admin_required
from caching import cache
import logging

# Setup logging for better debugging in production
logging.basicConfig(level=logging.INFO)

# ======================================================================================================
@token_required
@admin_required
def save():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        logging.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400
    
    try:
        new_order = orderService.save(order_data)
        return order_schema.jsonify(new_order), 201
    except Exception as e:
        logging.error(f"Error while saving order: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
    try:
        all_orders = orderService.find_all()
        return orders_schema.jsonify(all_orders), 200
    except Exception as e:
        logging.error(f"Error while fetching all orders: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_by_id(id):
    try:
        orders = orderService.find_by_id(id)
        return orders_schema.jsonify(orders), 200
    except Exception as e:
        logging.error(f"Error while fetching order with ID {id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_by_customer_id(id, token_id):
    try:
        if id == token_id:
            orders = orderService.find_by_customer_id(id)
            return orders_schema.jsonify(orders), 200
        else:
            return jsonify({"message": "You can't view other people's orders."}), 403
    except Exception as e:
        logging.error(f"Error while fetching orders for customer {id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_by_customer_email():
    try:
        email = request.json['email']
        orders = orderService.find_by_customer_email(email)
        return orders_schema.jsonify(orders), 200
    except KeyError:
        return jsonify({"message": "Email is required."}), 400
    except Exception as e:
        logging.error(f"Error while fetching orders for email {email}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@admin_required
def place_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        logging.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400
    
    try:
        new_order = orderService.place_order(order_data)
        return order_schema.jsonify(new_order), 201
    except Exception as e:
        logging.error(f"Error while placing order: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def retrieve_order():
    try:
        order_id = request.json['order_id']
    except KeyError:
        return jsonify({"message": "Order ID is required."}), 400
    
    try:
        order = orderService.retrieve_order(order_id)
        return order_schema.jsonify(order), 200
    except Exception as e:
        logging.error(f"Error while retrieving order with ID {order_id}: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
