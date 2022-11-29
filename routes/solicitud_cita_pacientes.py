from models.model import *
from utils.schema_solicitud_cita_pacientes import *
from utils.schema_union_paciente_solicitud import *
from flask import  jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

s_c_p_blueprint = Blueprint('s_c_p',__name__)

@s_c_p_blueprint.route('/s_c_p', methods=['POST'])
@jwt_required()
def crear_s_c_p():
    try:
        if request.is_json:
            tipo_solicitud = request.json['tipo_solicitud']
            paciente_id = request.json['paciente_id']
        else:
            tipo_solicitud = request.form['tipo_solicitud']
            paciente_id = request.form['paciente_id']
        nuevo_s_c_p = Solicitud_Cita_Pacientes(tipo_solicitud,estado=True,paciente_id=paciente_id)
        db.session.add(nuevo_s_c_p)
        db.session.commit()
        return s_c_p_schema.jsonify(nuevo_s_c_p)
    except Exception as e:
        return jsonify({"error":e})
    
@s_c_p_blueprint.route('/s_c_p', methods=['GET'])
@jwt_required()
def obtener_s_c_p():
    s_c_p = Solicitud_Cita_Pacientes.query.filter_by(estado=True)
    
    resultado = s_c_p_schemas.dump(s_c_p)
    return jsonify(resultado)
@s_c_p_blueprint.route('/s_c_p/<int:id>', methods=['GET'])
@jwt_required()
def obtener_s_c_ps(id):
    s_c_p = Solicitud_Cita_Pacientes.query.get_or_404(int(id))
    if s_c_p.estado != False:
        return s_c_p_schema.jsonify(s_c_p)
    else:
        return '<h1> no existe esta solicitud </h1>'
@s_c_p_blueprint.route('/s_c_p/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_solicitud(id):
    s_c_p = Solicitud_Cita_Pacientes.query.get_or_404(int(id))

    db.session.delete(s_c_p)
    db.session.commit()
    return jsonify({"Mensaje":"se ha elimanado con exito!"})