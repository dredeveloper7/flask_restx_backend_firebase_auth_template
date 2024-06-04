import firebase_admin
from firebase_admin.auth import verify_id_token as _verify_id_token
import requests
import os
from .firebase_config import config
"""
firebase_user_auth = FirebaseUserAuthentication(email='drewallace00@gmail.com', password="password123")
id_token = firebase_user_auth.login_with_email_and_password()
decoded_uid = firebase_user_auth.verify_id_token(id_token)

"""

class FirebaseUserAuthentication:        
    # Initialize Firebase Admin SDK
    dirpath = os.path.dirname(__file__)
    cred = firebase_admin.credentials.Certificate(config)
    firebase_admin.initialize_app(cred)
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

    # Function to log in user with email and password
    def login_with_email_and_password(self):
        api_key = 'AIzaSyAWqk4aXLHazKa6cOn0jbdXiURByDvEsQs'  # Replace with your Firebase project's web API key
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        
        payload = {
            'email': self.email,
            'password': self.password,
            'returnSecureToken': True
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if 'idToken' in data:
            print("User logged in successfully.")
            print("ID Token:", data['idToken'])
            return data['idToken']
        else:
            print("Failed to log in:", data.get('error', {}).get('message', 'Unknown error'))
            return None

    # Function to verify ID token
    def verify_id_token(self, id_token):
        try:
            decoded_token = _verify_id_token(id_token)
            print("Token verified successfully.")
            print("User ID:", decoded_token['uid'])
            return decoded_token['uid']
        except Exception as e:
            print("Failed to verify token:", str(e))
            return None


# def create_user_with_custom_uid(uid, email, password):
#     try:
#         user = auth.create_user(
#             uid=uid,
#             email=email,
#             password=password
#         )
#         print('Successfully created new user:', user.uid)
#         return user
#     except Exception as e:
#         print('Error creating new user:', str(e))
