from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from app.models.user import User
from flask import session, redirect, url_for
from flask import request

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# @api.route('/login')
# class Login(Resource):
#     @api.expect(login_model)
#     def post(self):
#         """Authenticate user and return a JWT token"""
#          # curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{ "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "cowabunga"}'
#         # curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "Content-Type: application/json" -d '{ "email": "john.doe@example.com", "password": "cowabunga" }'
#         print(request.headers)
#         if not request.is_json:
#             return {'error': "Request content-type must be 'application/json'"}, 400
#         credentials = api.payload  # Get the email and password from the request payload

#         # Step 1: Retrieve the user based on the provided email
#         user = facade.get_user_by_email(credentials['email'])

#         # Step 2: Check if the user exists and the password is correct
#         if not user or not user.verify_password(credentials['password']):
#             return {'error': 'Invalid credentials'}, 401

#         # Step 3: Create a JWT token with the user's id and is_admin flag
#         access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

#         # Step 4: Return the JWT token to the client
#         return {'access_token': access_token}, 200

@api.route('/login')
class Login(Resource):
    def post(self):
        """Authenticate user and return a JWT token"""
        # Retrieve the email and password from the form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(email)

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        # Step 4: Store the JWT token in session (or cookies) for future requests
        session['jwt_token'] = access_token
        session['user_id'] = user.id  # Store the user_id in the session

        # Step 5: Redirect to the dashboard route after successful login
        print("YOU'VE LOGGED IN!!")
        print(f"your_token:{access_token}")
        return redirect(url_for('dashboard', user=user.id))
