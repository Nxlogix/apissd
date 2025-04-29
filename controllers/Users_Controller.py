from models.User import User, Category, Product
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token  

def get_all_users():
    try:
        return [user.to_dict() for user in User.query.all()]    
    except Exception as error:
        print(f"ERROR {error}")

def create_user(name, email,password):
    try:
        new_user = User(name,email,password)
    
        db.session.add(new_user)
        db.session.commit()
        
        return new_user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg' : 'Error al crear usuario'}),500

def update_user(user_id, name, email):
    try:
        user = User.query.get(user_id)
        if not user:
            return {"error": "Usuario no encontrado"}, 404

        user.name = name if name else user.name
        user.email = email if email else user.email
        
        db.session.commit()
        return user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
        return {"error": str(e)}, 500

def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return {"error": "Usuario no encontrado"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente"}, 200
    except Exception as e:
        print(f"ERROR {e}")
        return {"error": str(e)}, 500

def login_user(email, password):
    user = User.query.filter_by(email=email).first();
    if user and user.check_password(password):
            access_token = create_access_token(identity=user.id);
            return jsonify ( {
                'access_token': access_token,
                'user': {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
        })
    return jsonify({"msg":"Credenciales invalidas"}),401

def get_all_products():
    try:
        return [product.to_dict() for product in Product.query.all()]
    except Exception as error:
        print(f"ERROR {error}")
        return {"error": "Error al listar productos"}, 500

def create_product(name, price, stock, category_id):
    try:
        new_product = Product(name, price, stock, category_id)
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict()
    except Exception as error:
        print(f"ERROR {error}")
        return {"error": "Error al crear producto"}, 500

def update_product(product_id, name=None, price=None, stock=None, category_id=None):
    try:
        product = Product.query.get(product_id)
        if not product:
            return {"error": "Producto no encontrado"}, 404

        product.name = name if name else product.name
        product.price = price if price else product.price
        product.stock = stock if stock else product.stock
        product.category_id = category_id if category_id else product.category_id

        db.session.commit()
        return product.to_dict()
    except Exception as error:
        print(f"ERROR {error}")
        return {"error": str(error)}, 500

def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return {"error": "Producto no encontrado"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Producto eliminado exitosamente"}, 200
    except Exception as error:
        print(f"ERROR {error}")
        return {"error": str(error)}, 500

def create_category(name, description=None):
    try:
        new_category = Category(name, description)
        db.session.add(new_category)
        db.session.commit()
        return new_category.to_dict()
    except Exception as error:
        print(f"ERROR {error}")
        return {"error": "Error al crear categoría"}, 500
    
def search_products_by_name(name):
    try:
        products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
        if not products:
            return {"message": "No se encontraron productos con ese nombre"}, 404
        return [product.to_dict() for product in products], 200
    except Exception as error:
        print(f"ERROR {error}")
        return {"error": "Error al buscar productos por nombre"}, 500

def search_products_by_category(category_name):
    try:
        category = Category.query.filter(Category.name.ilike(f"%{category_name}%")).first()
        if not category:
            return {"message": "Categoría no encontrada"}, 404
        products = Product.query.filter_by(category_id=category.id).all()
        if not products:
            return {"message": "No se encontraron productos en esta categoría"}, 404
        return [product.to_dict() for product in products], 200
    except Exception as error:
        print(f"ERROR {error}")
        return {"error": "Error al buscar productos por categoría"}, 500