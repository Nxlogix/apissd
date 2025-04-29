from flask import Blueprint, jsonify, request
from controllers.Users_Controller import (
    get_all_users, create_user, update_user, delete_user, login_user,
    get_all_products, create_product, update_product, delete_product,
    create_category, search_products_by_category, search_products_by_name
)

app_bp = Blueprint('users', __name__)

@app_bp.route('/', methods=['GET'])
def index():
    """
    Obtener todos los usuarios
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios obtenida correctamente
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
      500:
        description: Error del servidor
    """
    users = get_all_users()
    return jsonify(users), 200

@app_bp.route('/post', methods=['POST'])
def user_store():
    """
    Crear un usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: usuario
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
              example: "Juan"
            email:
              type: string
              example: "juan@ejemplo.com"
            password:
              type: string
              example: "secreto123"
    responses:
      201:
        description: Usuario creado exitosamente
        schema:
          $ref: '#/definitions/User'
      400:
        description: Datos faltantes o inválidos
      500:
        description: Error del servidor
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    new_user = create_user(name, email, password)
    return jsonify(new_user), 201

@app_bp.route('/update/<int:user_id>', methods=['PUT'])
def user_update(user_id):
    """
    Actualizar un usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID del usuario
      - in: body
        name: usuario
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      200:
        description: Usuario actualizado correctamente
        schema:
          $ref: '#/definitions/User'
      400:
        description: Datos faltantes o inválidos
      500:
        description: Error del servidor
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    name = data.get('name')
    email = data.get('email')
    updated_user = update_user(user_id, name, email)
    return jsonify(updated_user), 200

@app_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def user_delete(user_id):
    """
    Eliminar un usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID del usuario
    responses:
      200:
        description: Usuario eliminado correctamente
      500:
        description: Error del servidor
    """
    result = delete_user(user_id)
    status = result[1] if isinstance(result, tuple) else 200
    return jsonify(result), status

@app_bp.route('/login', methods=['POST'])
def login():
    """
    Login de usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: credenciales
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login exitoso, retorna token
      401:
        description: Credenciales inválidas
      500:
        description: Error del servidor
    """
    data = request.get_json()
    return login_user(data.get('email'), data.get('password'))

@app_bp.route('/products', methods=['GET'])
def list_products():
    """
    Listar productos
    ---
    tags:
      - Productos
    responses:
      200:
        description: Lista de productos obtenida correctamente
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
      500:
        description: Error del servidor
    """
    products = get_all_products()
    return jsonify(products), 200

@app_bp.route('/products', methods=['POST'])
def product_store():
    """
    Crear un producto
    ---
    tags:
      - Productos
    parameters:
      - in: body
        name: producto
        required: true
        schema:
          type: object
          required:
            - name
            - price
            - stock
            - category_id
          properties:
            name:
              type: string
            price:
              type: number
            stock:
              type: integer
            category_id:
              type: integer
    responses:
      201:
        description: Producto creado correctamente
        schema:
          $ref: '#/definitions/Product'
      400:
        description: Datos faltantes o inválidos
      500:
        description: Error del servidor
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    required = ['name', 'price', 'stock', 'category_id']
    if not all(data.get(k) for k in required):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    new_product = create_product(
        data['name'], data['price'], data['stock'], data['category_id']
    )
    return jsonify(new_product), 201

@app_bp.route('/products/<int:product_id>', methods=['PUT'])
def product_update(product_id):
    """
    Actualizar un producto
    ---
    tags:
      - Productos
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: ID del producto
      - in: body
        name: producto
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            price:
              type: number
            stock:
              type: integer
            category_id:
              type: integer
    responses:
      200:
        description: Producto actualizado correctamente
        schema:
          $ref: '#/definitions/Product'
      400:
        description: Datos faltantes o inválidos
      500:
        description: Error del servidor
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    updated = update_product(
        product_id,
        data.get('name'),
        data.get('price'),
        data.get('stock'),
        data.get('category_id')
    )
    return jsonify(updated), 200

@app_bp.route('/products/<int:product_id>', methods=['DELETE'])
def product_delete(product_id):
    """
    Eliminar un producto
    ---
    tags:
      - Productos
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: ID del producto
    responses:
      200:
        description: Producto eliminado correctamente
      500:
        description: Error del servidor
    """
    result = delete_product(product_id)
    status = result[1] if isinstance(result, tuple) else 200
    return jsonify(result), status

@app_bp.route('/categories', methods=['POST'])
def category_store():
    """
    Crear una categoría
    ---
    tags:
      - Categorías
    parameters:
      - in: body
        name: categoría
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      201:
        description: Categoría creada correctamente
        schema:
          $ref: '#/definitions/Category'
      400:
        description: Datos faltantes o inválidos
      500:
        description: Error del servidor
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    if not data.get('name'):
        return jsonify({"error": "El nombre de la categoría es obligatorio"}), 400
    new_cat = create_category(data['name'], data.get('description'))
    return jsonify(new_cat), 201

@app_bp.route('/products/search/name', methods=['GET'])
def search_by_name():
    """
    Buscar productos por nombre
    ---
    tags:
      - Productos
    parameters:
      - in: query
        name: name
        type: string
        required: true
        description: Nombre a buscar
    responses:
      200:
        description: Lista de productos encontrados
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
      400:
        description: Parámetro faltante
      500:
        description: Error del servidor
    """
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Debe proporcionar un nombre para buscar"}), 400
    results = search_products_by_name(name)
    return jsonify(results), 200

@app_bp.route('/products/search/category', methods=['GET'])
def search_by_category():
    """
    Buscar productos por categoría
    ---
    tags:
      - Productos
    parameters:
      - in: query
        name: category_name
        type: string
        required: true
        description: Nombre de la categoría
    responses:
      200:
        description: Lista de productos encontrados
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
      400:
        description: Parámetro faltante
      500:
        description: Error del servidor
    """
    category_name = request.args.get('category_name')
    if not category_name:
        return jsonify({"error": "Debe proporcionar el nombre de una categoría para buscar"}), 400
    results = search_products_by_category(category_name)
    return jsonify(results), 200
