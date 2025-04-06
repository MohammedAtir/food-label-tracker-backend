from flask import Blueprint, request, jsonify

food_bp = Blueprint('food', __name__)

# In-memory store (in a real app, replace with a database)
food_items = []

@food_bp.route('/foods', methods=['GET'])
def get_foods():
    return jsonify(food_items), 200

@food_bp.route('/foods', methods=['POST'])
def add_food():
    data = request.get_json()
    required_fields = ['name', 'sugar', 'carbs', 'protein']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields in request"}), 400

    new_item = {
        "name": data['name'],
        "sugar": float(data['sugar']),
        "carbs": float(data['carbs']),
        "protein": float(data['protein'])
    }
    food_items.append(new_item)
    return jsonify(new_item), 201
