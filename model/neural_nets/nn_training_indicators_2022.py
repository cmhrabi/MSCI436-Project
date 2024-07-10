import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle
import keras
from keras import layers
from keras import ops

def clean_data_set():
    data = pd.read_csv("model/data/2022/heart_2022_no_nans.csv")
    df = pd.DataFrame(data)
    
    # Replacing categorical values
    df['State'] = df['State'].map({'Alabama': 0, 'Alaska': 1, 'Arizona': 2, 'Arkansas': 3, 'California': 4, 'Colorado': 5,
                                    'Connecticut': 6, 'Delaware': 7, 'District of Columbia': 8, 'Florida': 9,  'Georgia': 10,
                                    'Hawaii': 11, 'Idaho': 12, 'Illinois': 13, 'Indiana': 14, 'Iowa': 15, 'Kansas': 16, 'Kentucky': 17,
                                    'Louisiana': 18, 'Maine': 19, 'Maryland': 20, 'Massachusetts': 21, 'Michigan': 22, 'Minnesota': 23,
                                    'Mississippi': 24, 'Missouri': 25, 'Montana': 26, 'Nebraska': 27, 'Nevada': 28, 'New Hampshire': 29,
                                    'New Jersey': 30, 'New Mexico': 31, 'New York': 32, 'North Carolina': 33, 'North Dakota': 34,
                                    'Ohio': 35, 'Oklahoma': 36, 'Oregon': 37, 'Pennsylvania': 38, 'Rhode Island': 39, 'South Carolina': 40,
                                    'South Dakota': 41, 'Tennessee': 42, 'Texas': 43, 'Utah': 44, 'Vermont': 45, 'Virginia': 46,
                                    'Washington': 47, 'West Virginia': 48, 'Wisconsin': 49, 'Wyoming': 50, 'Guam': 51, 'Puerto Rico': 52,
                                    'Virgin Islands': 53})
    df['Sex'] = df['Sex'].map({'Male': 0, 'Female': 1})
    df['LastCheckupTime'] = df['LastCheckupTime'].map({'Within past year (anytime less than 12 months ago)': 0,
                                                    'Within past 2 years (1 year but less than 2 years ago)': 1, 
                                                    'Within past 5 years (2 years but less than 5 years ago)': 2,
                                                    '5 or more years ago': 3})
    df['GeneralHealth'] = df['GeneralHealth'].map({'Very good': 0, 'Fair': 1, 'Good': 2, 
                                                    'Poor': 3, 'Excellent': 4})
    df['RemovedTeeth'] = df['RemovedTeeth'].map({'No': 0, 'Yes': 1})
    df['PhysicalActivities'] = df['PhysicalActivities'].map({'No': 0, 'Yes': 1})
    df['HadHeartAttack'] = df['HadHeartAttack'].map({'No': 0, 'Yes': 1})
    df['HadAngina'] = df['HadAngina'].map({'No': 0, 'Yes': 1})
    df['HadStroke'] = df['HadStroke'].map({'No': 0, 'Yes': 1})
    df['HadAsthma'] = df['HadAsthma'].map({'No': 0, 'Yes': 1})
    df['HadSkinCancer'] = df['HadSkinCancer'].map({'No': 0, 'Yes': 1})
    df['HadCOPD'] = df['HadCOPD'].map({'No': 0, 'Yes': 1})
    df['HadDepressiveDisorder'] = df['HadDepressiveDisorder'].map({'No': 0, 'Yes': 1})
    df['HadKidneyDisease'] = df['HadKidneyDisease'].map({'No': 0, 'Yes': 1})
    df['HadArthritis'] = df['HadArthritis'].map({'No': 0, 'Yes': 1})
    df['HadDiabetes'] = df['HadDiabetes'].map({'No': 0, 'Yes': 1, 
                                         'No, pre-diabetes or borderline diabetes': 2, 'Yes, but only during pregnancy (female)':3})
    df['DeafOrHardOfHearing'] = df['DeafOrHardOfHearing'].map({'No': 0, 'Yes': 1})
    df['BlindOrVisionDifficulty'] = df['BlindOrVisionDifficulty'].map({'No': 0, 'Yes': 1})
    df['DifficultyConcentrating'] = df['DifficultyConcentrating'].map({'No': 0, 'Yes': 1})
    df['DifficultyWalking'] = df['DifficultyWalking'].map({'No': 0, 'Yes': 1})
    df['DifficultyDressingBathing'] = df['DifficultyDressingBathing'].map({'No': 0, 'Yes': 1})
    df['DifficultyErrands'] = df['DifficultyErrands'].map({'No': 0, 'Yes': 1})
    df['SmokerStatus'] = df['SmokerStatus'].map({'Former smoker': 0, 'Never smoked': 1,
                                                  'Current smoker - now smokes every day': 2,
                                                  'Current smoker - now smokes some days':3})
    df['ECigaretteUsage'] = df['ECigaretteUsage'].map({'Never used e-cigarettes in my entire life': 0, 'Use them some days': 1,
                                                  'Not at all (right now)': 2, 'Use them every day':3})
    df['ChestScan'] = df['ChestScan'].map({'No': 0, 'Yes': 1})
    df['RaceEthnicityCategory'] = df['RaceEthnicityCategory'].map({'White only, Non-Hispanic': 0, 'Black only, Non-Hispanic': 1,
                                                                    'Other race only, Non-Hispanic': 2, 'Multiracial, Non-Hispanic': 3, 
                                                                    'Hispanic': 4})
    df['AgeCategory'] = df['AgeCategory'].map({'80 or older': 80,
                                                                     '75-79': 76,
                                                                     '70-74': 72,
                                                                     '65-69': 66, 
                                                                     '60-64': 62,
                                                                     '55-59': 54,
                                                                     '50-54': 52,
                                                                     '45-49': 46,
                                                                     '40-44': 42,
                                                                     '35-39': 36,
                                                                     '30-34': 32,
                                                                     '25-29': 26,
                                                                     '18-24': 21,})
    df['AlcoholDrinkers'] = df['AlcoholDrinkers'].map({'No': 0, 'Yes': 1})
    df['HIVTesting'] = df['HIVTesting'].map({'No': 0, 'Yes': 1})
    df['FluVaxLast12'] = df['FluVaxLast12'].map({'No': 0, 'Yes': 1})
    df['PneumoVaxEver'] = df['PneumoVaxEver'].map({'No': 0, 'Yes': 1})
    df['TetanusLast10Tdap'] = df['TetanusLast10Tdap'].map({'Yes, received Tdap': 0, 
                                                           'Yes, received tetanus shot but not sure what type': 1,
                                                           'No, did not receive any tetanus shot in the past 10 years': 2,
                                                           'Yes, received tetanus shot, but not Tdap': 3})
    df['HighRiskLastYear'] = df['HighRiskLastYear'].map({'No': 0, 'Yes': 1})
    df['CovidPos'] = df['CovidPos'].map({'No': 0, 'Yes': 1, 
                                         'Tested positive using home test without a health professional':2})

    # check the col names and data types
    column_names = df.columns
    print(column_names)
    types = df.dtypes
    print(types)

    return df

def trainNN(input):
    x=input.drop('HadHeartAttack',axis=1)
    y=input['HadHeartAttack']

    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.2 , random_state = 0)
    model = keras.Sequential()
    model.add(keras.Input(shape=(39,)))
    model.add(keras.layers.Dense(39, activation="tanh"))
    model.add(keras.layers.Dense(39, activation="tanh"))
    model.add(keras.layers.Dense(39, activation="tanh"))
    model.add(keras.layers.Dense(1, activation="sigmoid"))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss=keras.losses.BinaryCrossentropy(),
    )
    
    model.fit(x=x_train, y=y_train)
    
    y_pred = model.predict(x=x_test)

    y_pred = (y_pred > 0.5).astype(int) # convert to binary predictions

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    return model

def main():
    model = trainNN(clean_data_set())
    model_pkl_file = "indicator_2022_nn.pkl"  

    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)

if __name__ == "__main__":
    main()