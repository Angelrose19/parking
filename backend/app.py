import json
from flask import Flask, session, render_template, request, redirect
import pyrebase

app = Flask(__name__)

config = {
    'apiKey': "AIzaSyBTWJrKmp_gNr7YYv46nJUvKqgsriF1iUo",
    'authDomain': "main-9c0bf.firebaseapp.com",
    'projectId': "main-9c0bf",
    'storageBucket': "main-9c0bf.appspot.com",
    'messagingSenderId': "620928909019",
    'appId': "1:620928909019:web:583d8676a515ae0003d6fe",
    'measurementId': "G-6S6CM0KGP0",
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app.secret_key = "secret"

@app.route('/', methods=['GET'])
def index():
    return render_template('base.html',)

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if('user' in session):
        return render_template('welcome.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
        except Exception as e:
            error = str(e)
    return render_template('home.html', error=error)

@app.route("/register", methods=["POST", "GET"])
def register():
    error = None
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            return render_template('welcome.html')
        except Exception as e:
            error = str(e)
    return render_template('signup.html', error=error)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/history')
def history():
    return "This is the history page"

def fetch_nearby_parking_slots(driver_lat, driver_lng):
    # For example, you could fetch nearby parking slots from a database
    # Here, we use dummy data for demonstration
    nearby_slots = [
        {"id": 1, "latitude": driver_lat + 0.01, "longitude": driver_lng - 0.01, "available_slots": 3, "rate": 5},
        {"id": 2, "latitude": driver_lat - 0.01, "longitude": driver_lng + 0.01, "available_slots": 1, "rate": 8},
        {"id": 3, "latitude": driver_lat + 0.02, "longitude": driver_lng + 0.02, "available_slots": 2, "rate": 6}
    ]
    return nearby_slots

@app.route('/book_slot')
def book_slot():
    # Dummy values for driver's location (for demonstration)
    driver_lat = 37.7749
    driver_lng = -122.4194
    
    # Fetch nearby parking slots based on driver's location
    nearby_slots = fetch_nearby_parking_slots(driver_lat, driver_lng)
    
    # Convert nearby_slots to JSON format
    nearby_slots_json = json.dumps(nearby_slots)
    
    # Pass the nearby parking slot data to the template
    return render_template('book_slot.html', nearby_slots_json=nearby_slots_json)


@app.route('/profile')
def profile():
    return "This is the profile page"   

@app.route('/book_slot_form', methods=['GET'])
def book_slot_form():
    # Retrieve the slot ID from the URL query parameters
    slot_id = request.args.get('id')

    # Assuming you have a function to retrieve slot details from the database based on the slot ID
    slot_details = get_slot_details_from_database(slot_id)

    # Pass the slot details to the template
    return render_template('book_slot_form.html', slot_details=slot_details)

# Function to retrieve slot details from the database (replace with actual implementation)
def get_slot_details_from_database(slot_id):
    # Dummy slot details for demonstration
    return {
        "id": slot_id,
        "location": "Example Location",
        "rate": 5,
        "available_slots": 3
    }


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

if __name__ == '__main__':
    app.run()

