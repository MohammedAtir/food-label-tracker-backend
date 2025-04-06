from flask import Flask
from src.routes.food_routes import food_bp

app = Flask(__name__)
app.register_blueprint(food_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
