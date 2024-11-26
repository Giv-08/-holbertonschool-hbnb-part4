from app import create_app
from flask import Flask, render_template
from flask_restx import Api
from flask_jwt_extended import JWTManager, create_access_token
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
from flask_cors import CORS
from flask import Flask, request, jsonify
from app.services.facade import HBnBFacade
import requests
from flask import session, redirect, url_for
import os

# app = create_app()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
facade = HBnBFacade()
app.config['JWT_SECRET_KEY'] = 'malimirin1234'
jwt = JWTManager(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')  # Get user_id from the session
    place_id = session.get('place_id')

    places = None

    if place_id:
        places = facade.get_place_owner(user_id)
    if user_id:
        user = facade.get_user(user_id)
        if user:
            return render_template('dashboard.html', user=user, places=places)
    return redirect(url_for('login'))


@app.route('/sign_up')
def sign_up():
    # POST user
    return render_template('sign_up.html')

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

@app.route('/update_place')
def update_place():
    return render_template('update_place.html')

@app.route('/update_user')
def update_user():
    return render_template('update_user.html')

@app.route('/add_review/<place_id>')
def add_review(place_id):
    try:
        # need to specify id for specific place
        response = requests.get(f'http://0.0.0.0:5000/api/v1/places/{place_id}')
        if response.status_code == 200:
            place = response.json()
            print("Fetched data:", place)
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
api.add_namespace(auth_ns, path='/api/v1/auth')
api.add_namespace(protected_ns, path='/api/v1/protected')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
