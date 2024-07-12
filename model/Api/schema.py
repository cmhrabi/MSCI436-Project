from marshmallow import Schema, fields

class Predict1Schema(Schema):
    BMI = fields.Float(required=True)
    smoking = fields.Boolean(required=True)
    alcohol = fields.Boolean(required=True)
    stroke = fields.Boolean(required=True)
    diffWalking = fields.Boolean(required=True)
    sex = fields.String(required=True)
    age = fields.String(required=True)
    race = fields.String(required=True)
    diabetes = fields.Boolean(required=True)
    geneticHealth = fields.String(required=True)
    asthma = fields.Boolean(required=True)
    kidney = fields.Boolean(required=True)
    skinCancer = fields.Boolean(required=True)

class Predict2Schema(Schema):
    age = fields.String(required=True)
    education = fields.String(required=True)
    sex = fields.String(required=True)
    smoking = fields.Boolean(required=True)
    cigarettesPerDay = fields.String(required=True)
    bpMeds = fields.Boolean(required=True)
    stroke = fields.Boolean(required=True)
    diabetes = fields.Boolean(required=True)
    totChol = fields.Integer(required=True)
    hypertensive = fields.Boolean(required=True)
    sysBP = fields.Float(required=True)
    diaBP = fields.Float(required=True)
    BMI = fields.Float(required=True)
    glucose = fields.String(required=True)
    heartRate = fields.String(required=True)

class PredictSchema(Schema):
    model1 = fields.Nested(Predict1Schema)
    model2 = fields.Nested(Predict2Schema)

