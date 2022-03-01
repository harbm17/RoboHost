import firebase_admin
from firebase_admin import credentials, firestore;

from flask import Flask, jsonify, request, render_template
import json

# Initialize Flask
app = Flask(__name__, template_folder="robohost/Main/")

# Initialize Firebase / Firestore
cred = credentials.Certificate("firebase_private_key.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
objData = {} # This is the object to send back to JS.

@app.route('/auth_login', methods=['POST'])
def auth_login():

    if request.method == 'POST':

        # Extract deserialized payload data from JavaScript.
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Get CollectionReference instance for users table.
        colUsers = firestore_db.collection("users")

        # Get DocumentReference instance from collection.
        # Database is setup such that usernames are the primary key
        # for each document.
        docRef = colUsers.document(username)

        # Obtain DocumentSnapshot instance; this is needed to access
        # individual fields for a document.
        docSnapShot = docRef.get()

        # Is their a document in our database for the provided username or
        # does the document exist, but the password is invalid?
        if docSnapShot == None or docSnapShot.get("password") != password:

            objData['msg'] = "Invalid username/password entered!"
            objData['success'] = 0

        # Second case would be that this is a valid login request. For both cases,
        # we will need to send something back to JavaScript to notify the user
        # about what has happened.
        else:

            objData['msg'] = "Login successful!"
            objData['success'] = 1

        return jsonify(objData)

@app.route('/employeeLogin')
def render_login():
    return render_template('employeeLogin.html')