import json
import os
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from sklearn.model_selection import train_test_split
from flask_cors import CORS
import numpy as np
from marshmallow import ValidationError
from model import predict_heart_risk, predict_heart_disease, total_chol_loop, bmi_loop, smoking_loop
from schema import PredictSchema
from model_training import clean_data_set

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class Test(Resource):
    def get(self):
        return 'Welcome to, Test App API!'

    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201

            return {"error":"Invalid format."}

        except Exception as error:
            return {'error': error}
        
class Predict(Resource):
    def get(self):
        try:
            input = clean_data_set()

            x=input.drop('TenYearCHD',axis=1)
            y=input['TenYearCHD']

            x_train, X_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.2 , random_state = 0)            

            return {'Predicted Test set': predict_heart_risk(X_test).tolist()}
        
        except Exception as error:
            print(error)
            return {'error': error}
    
    def post(self):
        try:
            # Get Request body from JSON
            request_data = request.json
            schema = PredictSchema()
            try:
                result = schema.load(request_data)
            except ValidationError as err:
                return make_response(jsonify(err.messages), 400)

            data = request.get_json()
            predict2 = predict_heart_risk(data["model2"])
            predict1 = predict_heart_disease(data["model1"])

            if predict1[0] <= 0.5 and predict2[0] >= 0.5:

                return {'predict2':predict2.tolist(), 'predict1': predict1.tolist(), 'recommendations': {'totChol': total_chol_loop(data["model2"]), 'BMI': bmi_loop(data["model2"]), "smoking": smoking_loop(data["model2"])}}
            if predict1[0] >= 0.5:
                return {'predict2': [0], 'predict1': predict1.tolist(), 'recommendations': 'NA'}
            else:
                return {'predict2':predict2.tolist(), 'predict1': predict1.tolist(), 'recommendations': 'NA'}

            

        except Exception as error:
            return make_response({'error': error}, 400)

        
api.add_resource(Test,'/')
api.add_resource(Predict, '/predict')    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)