from flask_marshmallow import Marshmallow

ma = Marshmallow()

class PacienteSolicitudSchema(ma.Schema):
    class Meta:
        fileds=("primer_nombre","segundo_apellido","paciente_id","id")

pacienteSolicitudSchema = PacienteSolicitudSchema(many=False)
pacienteSolicitudSchemas = PacienteSolicitudSchema(many=True)