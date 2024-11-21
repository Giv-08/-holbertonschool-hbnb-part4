# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
from app import create_app
from flask import Flask, render_template
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from flask_cors import CORS
import requests

# app = create_app()

app = Flask(__name__)

@app.route('/') # url = http://0.0.0.0:5000/
def index():
    try:
        response = requests.get('http://0.0.0.0:5000/api/v1/places/')
        if response.status_code == 200:
            places = response.json()
            print("Fetched data:", places)
        else:
            places = []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        places = []

    return render_template('index.html', places=places)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/place/<place_id>')
def place_page(place_id):
    try:
        # Fetch the place data
        place_response = requests.get(f'http://0.0.0.0:5000/api/v1/places/{place_id}')
        if place_response.status_code == 200:
            place = place_response.json()
            print("Fetched place data:", place)
        else:
            place = {}  # Handle error case for place

        # Fetch reviews data
        reviews_response = requests.get(f'http://0.0.0.0:5000/api/v1/reviews/{place_id}')
        if reviews_response.status_code == 200:
            reviews = reviews_response.json()
        else:
            reviews = []  # Handle error case for reviews
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        place = {}
        reviews = []

    return render_template('place.html', place=place, reviews=reviews)


@app.route('/add_review/<place_id>')
def add_review(place_id):
    try:
        # need to specify id for specific place
        response = requests.get(f'http://0.0.0.0:5000/api/v1/places/{place_id}')
        if response.status_code == 200:
            place = response.json()
            print("Fetched data:", place)
            print("Fetched amenities:", place.amenities)
        else:
            place = {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        place = {}

    return render_template('add_review.html', place=place)

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Need to add CORS so that we can do API calls in Part 4
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/swagger')

# Register the namespaces
api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(amenities_ns, path='/api/v1/amenities')
api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(reviews_ns, path='/api/v1/reviews')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
