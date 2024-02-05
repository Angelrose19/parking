# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, auth, db  # Import the 'db' module

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'a@123'  # Change this to a secure key

# Initialize Firebase Admin SDK
cred = credentials.Certificate('./cred.json')  # Replace with the path to your JSON file
firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-firebase-url.firebaseio.com/'})

# Routes for driver
@app.route('/driver_signup', methods=['GET', 'POST'])
def driver_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user(email=email, password=password)
            session['user_id'] = user.uid
            return redirect(url_for('driver_dashboard'))
        except auth.AuthError as e:
            return render_template('driver_signup.html', error=str(e))

    return render_template('driver_signup.html')

@app.route('/driver_login', methods=['GET', 'POST'])
def driver_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user_id'] = user['localId']
            return redirect(url_for('driver_dashboard'))
        except auth.AuthError as e:
            return render_template('driver_login.html', error=str(e))

    return render_template('driver_login.html')


@app.route('/driver_dashboard')
def driver_dashboard():
    # Check if the user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('driver_login'))

    # Get the user's data from Firebase
    user_id = session['user_id']
    user_data = db.reference(f'/drivers/{user_id}').get()

    return render_template('driver_dashboard.html', user_data=user_data)

# Routes for parking space owner (similar to driver routes)

if __name__ == '__main__':
    app.run(debug=True)
