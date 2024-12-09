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
from flask import session, redirect, url_for, flash
import os

# app = create_app()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
facade = HBnBFacade()
app.config['JWT_SECRET_KEY'] = 'malimirin1234'
jwt = JWTManager(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['login'] = True # set a key flag to True
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear() # clear storage in server-side
    session['logout'] = True
    print("logged out!")
    return redirect("/")

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')  # Get user_id from the session
    try:
        response = requests.get(f'http://localhost:5000/api/v1/users/{user_id}/places/')
        if response.status_code == 200:
            places = response.json()
            print("Fetched data:", places)
        else:
            places = []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        places = []
    if user_id:
        user = facade.get_user(user_id)
        if user:
            return render_template('dashboard.html', user=user, places=places)
    return redirect(url_for('login'))


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    # POST user
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not (first_name and last_name and email and password):
            return render_template("register.html", message="All fields are required.")

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password
        }

        new_user = facade.create_user(user_data)
        print("new user has been created successfully!")
        session['user_id'] = new_user.id
        return redirect(f"/dashboard")
    return render_template('sign_up.html')

@app.route('/') # url = http://0.0.0.0:5000/
def index():
    print("Session data:", session)
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
        user_id = session.get('user_id')
        # Fetch the place data
        place_response = requests.get(f'http://0.0.0.0:5000/api/v1/places/{place_id}')
        if place_response.status_code == 200:
            place = place_response.json()
            print("Fetched place data:", place)
        else:
            place = {}

        owner_response = requests.get(f'http://localhost:5000/api/v1/places/{place_id}/owner/')
        if owner_response.status_code == 200:
            owner = owner_response.json()
            print("owner details:", owner)
        else:
            owner = {}

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
        owner = {}
    return render_template('place.html', place=place, reviews=reviews, owner=owner, user_id=user_id)

@app.route('/add_place', methods=["GET", "POST"])
def add_place():
    user_id = session.get('user_id')  # Get user_id from the session
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if not (title and description and price and latitude and longitude):
            return render_template("register.html", message="All fields are required.")

        place_data = {
            'title': title,
            'description': description,
            'price': float(price),
            'latitude': float(latitude),
            'longitude': float(longitude),
            'owner_id': user_id
        }

        new_place = facade.create_place(place_data)
        print("new place has been created successfully!")
        session['place_id'] = new_place.id
        return redirect(f"/dashboard")

    return render_template('add_place.html')

@app.route('/update_place/<place_id>', methods=["GET", "PUT", "DELETE"])
def update_place(place_id):
    user_id = session.get('user_id')
    if request.method == "GET":
        place = facade.get_place(place_id)
        if place:
            return render_template('update_place.html', place=place)
        else:
            return render_template('update_place.html', message="Place not found.")

    elif request.method == "PUT":
        place_data = request.get_json()
        print(f"Received data: {place_data}")

        title = place_data.get("title")
        description = place_data.get("description")
        price = float(place_data.get("price"))

        if not (title and description and price):
            return {"message": "All fields are required."}, 400

        try:
            price = float(price)
        except ValueError:
            return {"message": "Invalid value specified for price"}, 400

        updated_place = facade.update_place(place_id, place_data)

        if updated_place:
            return {"message": "Place updated successfully!"}, 200
    elif request.method == "DELETE":
        deleted_place = facade.delete_place(place_id)
        if deleted_place:
            print(f"Successfully deleted place with ID {place_id}")
            return redirect("/dashboard")

    return render_template("update_place.html", message="Invalid request.", place=None)


@app.route('/update_user/<user_id>', methods=["GET", "PUT"])
def update_user(user_id):
    if request.method == "GET":
        user = facade.get_user(user_id)
        if user:
            return render_template('update_user.html', user=user)
        else:
            return render_template('update_place.html', message="user not found.", user=None)
    elif request.method == "PUT":
        user_data = request.get_json()
        print(f"Received data: {user_data}")

        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")

        if not (first_name and last_name and email):
            return {"message": "All fields are required."}, 400

        updated_user = facade.update_user(user_id, user_data)

        if updated_user:
            return {"message": "user updated successfully!"}, 200

    return render_template("update_user.html", message="Invalid request.", user=None)

@app.route('/reviews/<place_id>', methods=["GET", "POST"])
def add_review(place_id):
    user_id = session.get('user_id') # get current user id
    # Fetch the place details using place_id
    if request.method == "GET":
        response = requests.get(f'http://0.0.0.0:5000/api/v1/places/{place_id}')
        if response.status_code == 200:
            place = response.json()
        else:
            place = {}

    return render_template('add_review.html', place=place, place_id=place_id, user_id=user_id)

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
