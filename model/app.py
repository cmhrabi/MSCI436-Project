import json
import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sklearn.model_selection import train_test_split
from flask_cors import CORS
import numpy as np
from marshmallow import ValidationError

from model import predict_heart_risk
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
                return jsonify(err.messages)

            data = request.get_json()
            predict = predict_heart_risk(data)
            return {'predict':predict.tolist()}

        except Exception as error:
            return {'error': error}

        
api.add_resource(Test,'/')
api.add_resource(Predict, '/predict')    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)