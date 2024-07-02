from marshmallow import Schema, fields

class PredictSchema(Schema):
    age = fields.Integer(required=True)
    education = fields.Integer(required=True)
    sex = fields.Integer(required=True)
    is_smoking = fields.Integer(required=True)
    cigs_per_day = fields.Integer(required=True)
    BP_meds = fields.Integer(required=True)
    prevalent_stroke = fields.Integer(required=True)
    diabetes = fields.Integer(required=True)
    tot_chol = fields.Integer(required=True)
    prevalent_hyp = fields.Integer(required=True)
    sys_BP = fields.Float(required=True)
    dia_BP = fields.Float(required=True)
    bmi = fields.Float(required=True)
    heart_rate = fields.Integer(required=True)
    glucose = fields.Integer(required=True)

