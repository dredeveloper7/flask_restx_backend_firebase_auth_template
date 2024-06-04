# auth.py
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User
from ..extensions import db
from .helpers.firebase_auth import FirebaseUserAuthentication

auth_ns = Namespace('auth', description='Authentication operations')
header_parser = reqparse.RequestParser()
header_parser.add_argument('Authorization', location='headers', required=True, help='Bearer token: Bearer <JWT>')

signup_model = auth_ns.model('Signup', {
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password'),
})

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        if User.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 400

        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='The user email adress'),
    'password': fields.String(required=True, description='The user password'),
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        firebase_user_auth = FirebaseUserAuthentication(email=email, password=password)
        id_token = firebase_user_auth.login_with_email_and_password()
        user_id = firebase_user_auth.verify_id_token(id_token)

        if user_id:
            access_token = create_access_token(identity=user_id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401

@auth_ns.route('/protected')
class Protected(Resource):
    # @auth_ns.expect(header_parser)
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        import pdb;pdb.set_trace()
        return {'message': f'Logged in as user {current_user_id}'}, 200
