from flask import Flask, request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from services import productService  
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, admin_required
from mysql.connector import Error
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# ======================================================================================================
def login():
    try:
        credentials = request.json
        token = productService.login(credentials['username'], credentials['password'])
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 401
    
    if token:
        return jsonify(token), 200
    else:
        return jsonify({'messages': 'Invalid username or password'}), 401

# ======================================================================================================
@token_required
@admin_required
def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        logging.error(f"Validation error: {e.messages}")
        return jsonify(e.messages), 400
    
    try:
        product_saved = productService.save(product_data)
        return product_schema.jsonify(product_saved), 201
    except Exception as e:
        logging.error(f"Error while saving product: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
    try:
        all_products = productService.find_all()
        return products_schema.jsonify(all_products), 200
    except Exception as e:
        logging.error(f"Error fetching all products: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@cache.cached(timeout=60)
@admin_required
def find_all_paginate():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        products = productService.find_all_paginate(page, per_page)
        return products_schema.jsonify(products), 200
    except Exception as e:
        logging.error(f"Error with pagination: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@admin_required
def add_product():
    try:
        product_data = product_schema.load(request.json)
        logging.info(f"Received product data: {product_data}")
    except ValidationError as e:
        logging.error(f"Validation error: {e.messages}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed."}), 500
        
        cursor = conn.cursor()
        name = product_data['name']
        price = product_data['price']
        stock = product_data['stock']

        new_product = (name, price, stock)
        query = "INSERT INTO Products(name, price, stock) VALUES(%s, %s, %s)"
        cursor.execute(query, new_product)
        conn.commit()
        logging.info(f"Product {name} added successfully.")
        
        return jsonify({"message": "New product added successfully"}), 201 
    
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def list_products():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True) 
        query = "SELECT * FROM Products"
        cursor.execute(query)
        products = cursor.fetchall()
        logging.info(f"Fetched {len(products)} products.")
        
        cursor.close()    
        conn.close()

        return products_schema.jsonify(products) 
    
    except Error as e:
        logging.error(f"Error fetching products from DB: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

# ======================================================================================================
@token_required
@admin_required
def update_product(id):
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        logging.error(f"Validation error: {e.messages}")
        return jsonify(e.messages), 400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed."}), 500
        
        cursor = conn.cursor()
        name = product_data['name']
        price = product_data['price']
        stock = product_data['stock']
        updated_product = (name, price, stock, id)

        query = "UPDATE Products SET name = %s, price = %s, stock = %s WHERE product_id = %s"
        cursor.execute(query, updated_product)
        conn.commit()
        logging.info(f"Product {id} updated successfully.")

        return jsonify({"message": "Product details updated successfully"}), 200
    
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ======================================================================================================
@token_required
@admin_required
def delete_product(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"message": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        product_to_remove = (id,)

        query = "SELECT * FROM Products WHERE product_id = %s"
        cursor.execute(query, product_to_remove)
        product = cursor.fetchone()

        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        query = "SELECT * FROM Orders WHERE product_id = %s"
        cursor.execute(query, product_to_remove)
        product_orders = cursor.fetchall()

        if product_orders:
            return jsonify({"message": "Cannot delete product with associated orders."}), 403  # FORBID the user from deleting a product with orders
        
        query = "DELETE FROM Products WHERE product_id = %s"
        cursor.execute(query, product_to_remove)
        conn.commit()

        logging.info(f"Product {id} deleted successfully.")
        return jsonify({"message": "Product removed successfully"}), 200

    except Error as e:
        logging.error(f"Error deleting product: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
