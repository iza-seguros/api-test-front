from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
import re
from datetime import datetime
import os
from email_validator import validate_email, EmailNotValidError

# Initialize Flask app
app = Flask(__name__)

# Ensure data directory exists
os.makedirs('/app/data', exist_ok=True)

# Configure SQLite database with absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/data/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-RESTX
api = Api(app, version='1.0', title='User Registration API',
          description='A simple API for user registration with data validation')

# Create namespace
ns = api.namespace('users', description='User operations')

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    zip_code = db.Column(db.String(9), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    terms_accepted = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'zip_code': self.zip_code,
            'address': self.address,
            'number': self.number,
            'city': self.city,
            'state': self.state,
            'terms_accepted': self.terms_accepted,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create API models for Swagger documentation
user_model = api.model('User', {
    'full_name': fields.String(required=True, description='User full name'),
    'email': fields.String(required=True, description='User email address'),
    'phone': fields.String(required=True, description='Brazilian phone number'),
    'zip_code': fields.String(required=True, description='Brazilian CEP'),
    'address': fields.String(required=True, description='Street address'),
    'number': fields.String(required=True, description='Address number'),
    'city': fields.String(required=True, description='City name'),
    'state': fields.String(required=True, description='State abbreviation (2 letters)'),
    'terms_accepted': fields.Boolean(required=True, description='Terms acceptance status')
})

# Validation functions
def validate_phone(phone):
    # Brazilian phone format: (XX) XXXXX-XXXX or (XX) XXXX-XXXX
    pattern = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    return bool(re.match(pattern, phone))

def validate_zip_code(zip_code):
    # Brazilian CEP format: XXXXX-XXX
    pattern = r'^\d{5}-\d{3}$'
    return bool(re.match(pattern, zip_code))

def validate_state(state):
    # Brazilian state abbreviations (2 letters)
    valid_states = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    return state.upper() in valid_states

def validate_user_data(data, check_email_uniqueness=True, exclude_user_id=None):
    # Validate required fields
    required_fields = ['full_name', 'email', 'phone', 'zip_code', 'address', 
                      'number', 'city', 'state', 'terms_accepted']
    for field in required_fields:
        if field not in data or data[field] is None:
            return {'message': f'Missing required field: {field}'}, 400

    # Validate email format
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return {'message': 'Invalid email format'}, 400

    # Validate phone format
    if not validate_phone(data['phone']):
        return {'message': 'Invalid phone format. Use (XX) XXXXX-XXXX or (XX) XXXX-XXXX'}, 400

    # Validate zip code format
    if not validate_zip_code(data['zip_code']):
        return {'message': 'Invalid zip code format. Use XXXXX-XXX'}, 400

    # Validate state
    if not validate_state(data['state']):
        return {'message': 'Invalid state abbreviation'}, 400

    # Validate terms acceptance
    if not data['terms_accepted']:
        return {'message': 'Terms must be accepted'}, 400

    # Check if email already exists (only for new users or when email is changed)
    if check_email_uniqueness:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and (exclude_user_id is None or existing_user.id != exclude_user_id):
            return {'message': 'Email already registered'}, 409

    return None, None

@ns.route('')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = User.query.all()
        return [user.to_dict() for user in users]

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.response(201, 'User successfully created')
    @ns.response(400, 'Validation Error')
    @ns.response(409, 'Email already exists')
    def post(self):
        """Create a new user"""
        data = request.json
        
        # Validate user data
        error, status_code = validate_user_data(data)
        if error:
            return error, status_code

        # Create new user
        try:
            new_user = User(
                full_name=data['full_name'],
                email=data['email'],
                phone=data['phone'],
                zip_code=data['zip_code'],
                address=data['address'],
                number=data['number'],
                city=data['city'],
                state=data['state'].upper(),
                terms_accepted=data['terms_accepted']
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Internal server error'}, 500

@ns.route('/<int:id>')
@ns.param('id', 'The user identifier')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.response(200, 'Success')
    @ns.response(404, 'User not found')
    def get(self, id):
        """Get a user by ID"""
        user = User.query.get(id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.to_dict()

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.response(200, 'User successfully updated')
    @ns.response(400, 'Validation Error')
    @ns.response(404, 'User not found')
    @ns.response(409, 'Email already exists')
    def put(self, id):
        """Update a user"""
        user = User.query.get(id)
        if not user:
            return {'message': 'User not found'}, 404

        data = request.json
        
        # Validate user data
        error, status_code = validate_user_data(data, exclude_user_id=id)
        if error:
            return error, status_code

        try:
            user.full_name = data['full_name']
            user.email = data['email']
            user.phone = data['phone']
            user.zip_code = data['zip_code']
            user.address = data['address']
            user.number = data['number']
            user.city = data['city']
            user.state = data['state'].upper()
            user.terms_accepted = data['terms_accepted']
            
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            return {'message': 'Internal server error'}, 500

    @ns.doc('delete_user')
    @ns.response(204, 'User successfully deleted')
    @ns.response(404, 'User not found')
    def delete(self, id):
        """Delete a user"""
        user = User.query.get(id)
        if not user:
            return {'message': 'User not found'}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return {'message': 'Internal server error'}, 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True) 