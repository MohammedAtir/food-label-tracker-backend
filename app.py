from flask import Flask
from food_routes import food_bp  # Adjust this import based on your actual file structure

app = Flask(__name__)
app.register_blueprint(food_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
