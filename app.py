# from flask import Flask, render_template
# import requests
# # import jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def index():
#     try:
#         response = requests.get('http://localhost:5000/api/v1/places/')
#         if response.status_code == 200:
#             places = response.json()
#             # jsonify?
#             print("Fetched data:", places)
#         else:
#             places = []
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data: {e}")
#         places = []

#     return render_template('index.html', places=places)

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5000)
