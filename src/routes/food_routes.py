import requests
import sqlite3
from flask import Blueprint, request, jsonify

food_bp = Blueprint('food', __name__)

HUGGING_FACE_API_KEY = 'YOUR_HUGGING_FACE_API_KEY'  # Replace with your Hugging Face API key

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('foods.db')
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn

# Route to get all foods
@food_bp.route('/foods', methods=['GET'])
def get_foods():
    conn = get_db_connection()
    foods = conn.execute('SELECT * FROM food').fetchall()
    conn.close()
    return jsonify([dict(row) for row in foods]), 200

# Route to add a new food item
@food_bp.route('/foods', methods=['POST'])
def add_food():
    data = request.get_json()
    required_fields = ['name', 'sugar', 'carbs', 'protein']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields in request"}), 400

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO food (name, sugar, carbs, protein)
        VALUES (?, ?, ?, ?)
    ''', (data['name'], data['sugar'], data['carbs'], data['protein']))
    conn.commit()
    conn.close()

    return jsonify(data), 201

# Route to get similar foods using Hugging Face API
@food_bp.route('/foods/similar', methods=['POST'])
def get_similar_foods():
    data = request.get_json()
    if not all(field in data for field in ['sugar', 'carbs', 'protein']):
        return jsonify({"error": "Missing nutrient fields"}), 400

    prompt = (
        f"Suggest foods similar to a food with Sugar: {data['sugar']}g, "
        f"Carbs: {data['carbs']}g, Protein: {data['protein']}g."
    )

    # Call Hugging Face API
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/distilgpt2",  # You can choose other models too
        headers=headers,
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        return jsonify({"error": "Error fetching suggestions from Hugging Face"}), 500

    result = response.json()
    suggestions = result.get('generated_text', '').split('\n')

    return jsonify({"suggestions": suggestions}), 200
