import pickle
import pandas as pd
import json

def predict_heart_risk(config):
    ##loading the model from the saved file
    pkl_filename = "model/heart_classifier_model.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        input = [list(config.values())]
    else:
        input = config

    prediction = model.predict(input)
    return prediction