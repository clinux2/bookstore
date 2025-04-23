from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
import bcrypt
import jwt
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB configuration
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client.bookstore

# JWT Secret Key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

# Authentication middleware
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.users.find_one({'_id': ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# Admin registration endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if db.users.find_one({'email': data['email']}):
        return jsonify({'message': 'User already exists'}), 400
    
    # Hash password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user = {
        'email': data['email'],
        'password': hashed_password,
        'is_admin': True,
        'created_at': datetime.utcnow()
    }
    
    db.users.insert_one(user)
    return jsonify({'message': 'Admin registered successfully'}), 201

# Admin login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.users.find_one({'email': data['email']})
    
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.utcnow() + timedelta(days=1)
    }, app.config['SECRET_KEY'])
    
    return jsonify({'token': token})

# Book management endpoints
@app.route('/api/books', methods=['GET'])
def get_books():
    books = list(db.books.find())
    return jsonify([serialize_doc(book) for book in books])

@app.route('/api/books', methods=['POST'])
@token_required
def add_book(current_user):
    if not current_user['is_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    book = {
        'title': data['title'],
        'author': data['author'],
        'price': data['price'],
        'description': data['description'],
        'stock': data['stock'],
        'created_at': datetime.utcnow()
    }
    
    db.books.insert_one(book)
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/api/books/<book_id>', methods=['PUT'])
@token_required
def update_book(current_user, book_id):
    if not current_user['is_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    db.books.update_one(
        {'_id': ObjectId(book_id)},
        {'$set': {
            'title': data['title'],
            'author': data['author'],
            'price': data['price'],
            'description': data['description'],
            'stock': data['stock'],
            'updated_at': datetime.utcnow()
        }}
    )
    return jsonify({'message': 'Book updated successfully'})

@app.route('/api/books/<book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, book_id):
    if not current_user['is_admin']:
        return jsonify({'message': 'Unauthorized'}), 403
        
    db.books.delete_one({'_id': ObjectId(book_id)})
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True) 