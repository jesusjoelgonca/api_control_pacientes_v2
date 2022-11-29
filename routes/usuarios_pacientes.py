from datetime import timedelta, timezone
from models.model import *
from utils.schema_usuarios_pacientes import *
from flask import  jsonify, request, Blueprint
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required, create_access_token, set_access_cookies
from flask_mail import Message
from mail import mail

usuarios_pacientes_blueprint = Blueprint('usuarios_pacientes',__name__)


@usuarios_pacientes_blueprint.route('/usuarios_pacientes', methods=['POST'])
@jwt_required()
def crear_usuarios_pacientes():
    try:
        
        identifacion = request.json['identificacion']
        password = request.json['password']
        correo = request.json['correo']
        paciente_id = request.json['paciente_id']

        nuevo_usuario = UsuariosPacientes(identificacion=identifacion,password=password,tipo_usuario="Paciente",estado=True,paciente_id=paciente_id)
        db.session.add(nuevo_usuario)
        db.session.commit()
        msg = Message(
            subject=("Mensaje generado: su cuenta de Usuario para ingresar a la app"),
            sender=("jesusjoelgonzalezcastro@gmail.com"),
            recipients = [str(correo)],
            body=("Su usuario es: "+str(identifacion)+"\n"+"Su contraseña es: "+str(password))
        )
        mail.send(msg)
        return usuarios_pacientes_schema.jsonify(nuevo_usuario)
    except Exception as e:
        return jsonify({"Error": e})

@usuarios_pacientes_blueprint.route('/usuarios_pacientes', methods=['GET'])
@jwt_required()
def obtener_pacientes():
    usuarios = UsuariosPacientes.query.filter_by(tipo_usuario="Paciente")
    resultados = usuarios_pacientes_schemas.dump(usuarios)
    return jsonify(resultados)

@usuarios_pacientes_blueprint.route('/usuarios_pacientes/<int:id>', methods=['GET'])
@jwt_required()
def obtener_paciente(id):
    usuario = UsuariosPacientes.query.get_or_404(int(id))
    if usuario.estado != False:
        return usuarios_pacientes_schema.jsonify(usuario)
    else:
        return '<h1>no se encuentra este usuario medico </h1>'

@usuarios_pacientes_blueprint.route('/usuarios_pacientes/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_paciente(id):
    usuario = UsuariosPacientes.query.get_or_404(int(id))
    identifacion = request.json['identificacion']
    password = request.json['password']

    usuario.identificacion = identifacion
    usuario.password = password

    db.session.commit()
    return usuarios_pacientes_schema.jsonify(usuario)
    
@usuarios_pacientes_blueprint.route('/usuarios_pacientes/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_paciente(id):
    usuario = UsuariosPacientes.query.get_or_404(int(id))
    estado = False

    usuario.estado = estado
    db.session.commit()
    return jsonify({"Mensaje":"se ha eliminado con exito!"})

@usuarios_pacientes_blueprint.after_request
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

@usuarios_pacientes_blueprint.route('/usuarios_pacientes/login', methods=['POST'])
def login_paciente():
    if request.is_json:
        identificacion = request.json['identificacion']
        password = request.json['password']
    else:
        identificacion = request.form['identificacion']
        password = request.form['password']

    test = UsuariosPacientes.query.filter_by(identificacion=identificacion, password=password).first()
    if test:
            
        access_token = create_access_token(identity=identificacion)
        response = jsonify({"msg": "login successful","success":True,"access_token":access_token, "paciente_id":test.paciente_id})
        set_access_cookies(response, access_token)
        return response
    else:
        return jsonify({"message":"Identificacion o Contraseña incorrectos!",
            "success":False})