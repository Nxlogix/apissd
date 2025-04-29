from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), nullable= False)
    email = db.Column(db.String(50), unique= True, nullable= False)
    password = db.Column(db.String(200), nullable= False)
    
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password,password);
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    
    def __init__(self, name, price, stock, category_id):
        self.name = name
        self.price = price
        self.stock = stock
        self.category_id = category_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category_id": self.category_id,
            "category": self.category.to_dict() if self.category else None,
        }