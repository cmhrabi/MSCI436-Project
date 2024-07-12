import pickle
import pandas as pd
import json

def clean_data_risk(input):
    if input['sex'] == 'M':
        input['sex'] = 0
    else:
        input['sex'] = 1
    
    for k in input:
        if type(input[k]) == bool:
            if input[k]:
                input[k] = 1
            else:
                input[k] = 0
        elif k == "BMI":
            input[k] = float(input[k])
        else:
            input[k] = int(input[k])

    return input

def predict_heart_risk(config):
    ##loading the model from the saved file
    pkl_filename = "heart_classifier_model.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        config = clean_data_risk(config)
        input = pd.DataFrame([config])
        print(input)
    else:
        input = config

    prediction = model.predict(input)
    return prediction

def clean_data_disease(input):
    if input['sex'] == 'M':
        input['sex'] = 0
    else:
        input['sex'] = 1
    
    for k in input:
        if type(input[k]) == bool:
            if input[k]:
                input[k] = 1
            else:
                input[k] = 0
        elif k == "BMI":
            input[k] = float(input[k])
        else:
            input[k] = int(input[k])

    return input

def predict_heart_disease(config):
    pkl_filename = "indicator_2020_nn.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        config = clean_data_disease(config)
        input = pd.DataFrame([config])
        print(input)
    else:
        input = config


    prediction = model.predict(input)
    return prediction

def total_chol_loop(config):
    pkl_filename = "heart_classifier_model.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        config = clean_data_risk(config)
        count = 0
        for i in range(config["totChol"]):
            config['totChol']-=1
            input = pd.DataFrame([config])
            print(input)
            prediction = model.predict(input)
            if prediction[0] == 0:
                return count
            count+=1
            if count >= 40:
                break

    return 0

def bmi_loop(config):
    pkl_filename = "heart_classifier_model.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        config = clean_data_risk(config)
        count = 0
        for i in range(int(config["BMI"])):
            config['BMI']-=1
            input = pd.DataFrame([config])
            print(input)
            prediction = model.predict(input)
            if prediction[0] == 0:
                return count
            count+=1
        
        return 0
    return 0

def smoking_loop(config):
    pkl_filename = "heart_classifier_model.pkl"
    with open(pkl_filename, 'rb') as f_in:
        model = pickle.load(f_in)

    if type(config) == dict:
        config = clean_data_risk(config)
        for i in range(int(config["smoking"])):
            config['smoking']-=1
            input = pd.DataFrame([config])
            print(input)
            prediction = model.predict(input)
            if prediction[0] == 0:
                return True
        
        return False
    return False