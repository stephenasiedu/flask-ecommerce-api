from flask import Flask, request, jsonify
from models.schemas.accountSchema import account_schema, accounts_schema
from services import accountService
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
        token = accountService.login(credentials['username'], credentials['password'])
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
        account_data = account_schema.load(request.json)
        account_saved = accountService.save(account_data)
        return account_schema.jsonify(account_saved), 201
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        logging.error(f"Error while saving account: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_all():
    try:
        all_accounts = accountService.find_all()
        return accounts_schema.jsonify(all_accounts), 200
    except Exception as e:
        logging.error(f"Error while fetching all accounts: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def find_all_paginate():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        accounts = accountService.find_all_paginate(page, per_page)
        return accounts_schema.jsonify(accounts), 200
    except Exception as e:
        logging.error(f"Error while fetching paginated accounts: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# ======================================================================================================
@token_required
@admin_required
def add_account():
    try:
        account_data = account_schema.load(request.json)
        logging.info(f"Account data received: {account_data}")

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        with closing(conn.cursor()) as cursor:
            query = "INSERT INTO Accounts(name, email, phone) VALUES(%s, %s, %s)"
            cursor.execute(query, (account_data['name'], account_data['email'], account_data['phone']))
            conn.commit()

        return jsonify({"message": "New account added successfully"}), 201
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify(e.messages), 400
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as e:
        logging.error(f"Error adding account: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def read_accounts():
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"message": "Database connection failed"}), 500

        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute("SELECT * FROM Accounts")
            accounts = cursor.fetchall()

        return accounts_schema.jsonify(accounts), 200
    except Error as e:
        logging.error(f"Error while fetching accounts: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# ======================================================================================================
@token_required
@admin_required
def update_account(id):
    try:
        account_data = account_schema.load(request.json)
        logging.info(f"Account data to update: {account_data}")

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        with closing(conn.cursor()) as cursor:
            query = "UPDATE Accounts SET name = %s, email = %s, phone = %s WHERE account_id = %s"
            cursor.execute(query, (account_data['name'], account_data['email'], account_data['phone'], id))
            conn.commit()

        return jsonify({"message": "Account details updated successfully"}), 200
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return jsonify(e.messages), 400
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as e:
        logging.error(f"Error updating account: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

# ======================================================================================================
@token_required
@cache.cached(timeout=60)
@admin_required
def delete_account(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"message": "Database connection failed"}), 500

        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT * FROM Accounts WHERE account_id = %s", (id,))
            account = cursor.fetchone()

            if not account:
                return jsonify({"message": "Account not found"}), 404

            cursor.execute("SELECT * FROM Orders WHERE account_id = %s", (id,))
            account_orders = cursor.fetchall()

            if account_orders:
                return jsonify({"message": "Cannot delete account with associated orders."}), 403

            cursor.execute("DELETE FROM Accounts WHERE account_id = %s", (id,))
            conn.commit()

        return jsonify({"message": "Account removed successfully"}), 200
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as e:
        logging.error(f"Error deleting account: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
