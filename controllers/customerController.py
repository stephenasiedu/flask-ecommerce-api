from flask import Flask, request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerService
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, admin_required
from mysql.connector import Error
from contextlib import closing
import logging

# Setup logging for better debugging in production
logging.basicConfig(level=logging.INFO)

# ======================================================================================================
def login():
    try:
        credentials = request.json
        token = customerService.login(credentials['username'], credentials['password'])
        if token:
            return jsonify(token), 200
        return jsonify({'message': 'Invalid username or password'}), 401
    except KeyError:
        return jsonify({'message': 'Invalid payload, expecting username and password'}), 400
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# ======================================================================================================
@token_required
@admin_required
def save():
    try:
        customer_data = customer_schema.load(request.json)
        customer_saved = customerService.save(customer_data)
        return customer_schema.jsonify(customer_saved), 201
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        logging.error(f"Error while saving customer: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
    try:
        all_customers = customerService.find_all()
        return customers_schema.jsonify(all_customers), 200
    except Exception as e:
        logging.error(f"Error while fetching all customers: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# ======================================================================================================
@cache.cached(timeout=60)
@admin_required
def find_all_paginate():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        customers = customerService.find_all_paginate(page, per_page)
        return customers_schema.jsonify(customers), 200
    except Exception as e:
        logging.error(f"Error while fetching paginated customers: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# ======================================================================================================
@token_required
@admin_required
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
        logging.info(f"Customer data received: {customer_data}")

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        with closing(conn.cursor()) as cursor:
            query = "INSERT INTO Customers(name, email, phone) VALUES(%s, %s, %s)"
            cursor.execute(query, (customer_data['name'], customer_data['email'], customer_data['phone']))
            conn.commit()

        return jsonify({"message": "New customer added successfully"}), 201
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify(e.messages), 400
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as e:
        logging.error(f"Error adding customer: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# ======================================================================================================
@token_required
@admin_required
def read_customer():
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"message": "Database connection failed"}), 500

        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute("SELECT * FROM Customers")
            customers = cursor.fetchall()

        return customers_schema.jsonify(customers), 200
    except Error as e:
        logging.error(f"Error while fetching customers: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# ======================================================================================================
@token_required
@admin_required
def update_customer(id):
    try:
        customer_data = customer_schema.load(request.json)
        logging.info(f"Customer data to update: {customer_data}")

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        with closing(conn.cursor()) as cursor:
            query = "UPDATE Customers SET name = %s, email = %s, phone = %s WHERE customer_id = %s"
            cursor.execute(query, (customer_data['name'], customer_data['email'], customer_data['phone'], id))
            conn.commit()

        return jsonify({"message": "Customer details updated successfully"}), 200
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify(e.messages), 400
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as e:
        logging.error(f"Error updating customer: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# ======================================================================================================
@token_required
@admin_required
def delete_customer(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"message": "Database connection failed"}), 500

        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (id,))
            customer = cursor.fetchone()

            if not customer:
                return jsonify({"message": "Customer not found"}), 404

            cursor.execute("SELECT * FROM Orders WHERE customer_id = %s", (id,))
            customer_orders = cursor.fetchall()

            if customer_orders:
                return jsonify({"message": "Cannot delete customer with associated orders."}), 403

            cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (id,))
            conn.commit()

        return jsonify({"message": "Customer removed successfully"}), 200
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as e:
        logging.error(f"Error deleting customer: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
