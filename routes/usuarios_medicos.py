
from datetime import timedelta, timezone
from models.model import *
from utils.schema_usuarios_medicos import *
from utils.schema_medicos import *
from flask import  jsonify, request, Blueprint
from flask_jwt_extended import get_jwt, jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity

usuarios_medicos_blueprint = Blueprint('usuarios_medicos',__name__)


@usuarios_medicos_blueprint.route('/usuarios_medicos', methods=['POST'])
@jwt_required()
def crear_usuarios_medicos():
    try:
        identifacion = request.json['identificacion']
        password = request.json['password']
        medico_id = request.json['medico_id']

        nuevo_usuario = UsuariosMedicos(identificacion=identifacion,password=password,tipo_usuario="Medico",estado=True,medico_id=medico_id)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuarios_medicos_schema.jsonify(nuevo_usuario)
    except Exception as e:
        return jsonify({"Error": e})

@usuarios_medicos_blueprint.route('/usuarios_medicos', methods=['GET'])
@jwt_required()
def obtener_medicos():
    current_user = get_jwt_identity()
    usuarios = UsuariosMedicos.query.filter_by(tipo_usuario="Medico")
    resultados = usuarios_medicos_schemas.dump(usuarios)
   
    return jsonify(resultados)

@usuarios_medicos_blueprint.route('/usuarios_medicos/<int:id>', methods=['GET'])
@jwt_required()
def obtener_medico(id):
    usuario = UsuariosMedicos.query.get_or_404(int(id))
   
    if usuario.estado == False and usuario.tipo_usuario!="Medico":
    
        return "<h1>No existe el medico</h1>"
    else:
        return usuarios_medicos_schema.jsonify(usuario)

    

@usuarios_medicos_blueprint.route('/usuarios_medicos/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_medico(id):
    usuario = UsuariosMedicos.query.get_or_404(int(id))
    identifacion = request.json['identificacion']
    password = request.json['password']

    usuario.identificacion = identifacion
    usuario.password = password

    db.session.commit()
    return usuarios_medicos_schema.jsonify(usuario)
    
    
@usuarios_medicos_blueprint.route('/usuarios_medicos/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_medico(id):
    usuario = UsuariosMedicos.query.get_or_404(int(id))
    estado = False

    usuario.estado = estado
    db.session.commit()
    return jsonify({"Mensaje":"se ha eliminado con exito!"})

@usuarios_medicos_blueprint.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

@usuarios_medicos_blueprint.route('/usuarios_medicos/login', methods=['POST'])
def login():
    if request.is_json:
        identificacion = request.json['identificacion']
        password = request.json['password']
    else:
        identificacion = request.form['identificacion']
        password = request.form['password']
  
    test = UsuariosMedicos.query.filter_by(identificacion=identificacion, password=password).first()
    
    if test:
        
        access_token = create_access_token(identity=identificacion)
        response = jsonify({"msg": "login successful","success":True,"access_token":access_token, "medico_id":test.medico_id})
        set_access_cookies(response, access_token)
        return response
    else:
        return jsonify({"message":"Identificacion o Contraseña incorrectos!",
        "success":False})





