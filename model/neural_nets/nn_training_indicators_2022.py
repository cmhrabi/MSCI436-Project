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

    unique_entries = df['RemovedTeeth'].unique()
    print("UNIQUE RemovedTeeth CATEGORIES: \n", unique_entries)
    unique_entries = df['HadHeartAttack'].unique()
    print("UNIQUE HadHeartAttack CATEGORIES: \n", unique_entries)
    unique_entries = df['HadAngina'].unique()
    print("UNIQUE HadAngina CATEGORIES: \n", unique_entries)
    unique_entries = df['HadStroke'].unique()
    print("UNIQUE HadStroke CATEGORIES: \n", unique_entries)
    unique_entries = df['HadAsthma'].unique()
    print("UNIQUE HadAsthma CATEGORIES: \n", unique_entries)
    unique_entries = df['HadSkinCancer'].unique()
    print("UNIQUE HadSkinCancer CATEGORIES: \n", unique_entries)
    unique_entries = df['HadCOPD'].unique()
    print("UNIQUE HadCOPD CATEGORIES: \n", unique_entries)
    unique_entries = df['HadDepressiveDisorder'].unique()
    print("UNIQUE HadDepressiveDisorder CATEGORIES: \n", unique_entries)
    unique_entries = df['HadKidneyDisease'].unique()
    print("UNIQUE HadKidneyDisease CATEGORIES: \n", unique_entries)
    unique_entries = df['HadArthritis'].unique()
    print("UNIQUE HadArthritis CATEGORIES: \n", unique_entries)
    unique_entries = df['HadDiabetes'].unique()
    print("UNIQUE HadDiabetes CATEGORIES: \n", unique_entries)
    unique_entries = df['DeafOrHardOfHearing'].unique()
    print("UNIQUE DeafOrHardOfHearing CATEGORIES: \n", unique_entries)
    unique_entries = df['BlindOrVisionDifficulty'].unique()
    print("UNIQUE BlindOrVisionDifficulty CATEGORIES: \n", unique_entries)
    unique_entries = df['DifficultyConcentrating'].unique()
    print("UNIQUE DifficultyConcentrating CATEGORIES: \n", unique_entries)
    unique_entries = df['DifficultyWalking'].unique()
    print("UNIQUE DifficultyWalking CATEGORIES: \n", unique_entries)
    unique_entries = df['DifficultyDressingBathing'].unique()
    print("UNIQUE DifficultyDressingBathing CATEGORIES: \n", unique_entries)
    unique_entries = df['DifficultyErrands'].unique()
    print("UNIQUE DifficultyErrands CATEGORIES: \n", unique_entries)
    unique_entries = df['SmokerStatus'].unique()
    print("UNIQUE SmokerStatus CATEGORIES: \n", unique_entries)
    unique_entries = df['ECigaretteUsage'].unique()
    print("UNIQUE ECigaretteUsage CATEGORIES: \n", unique_entries)
    unique_entries = df['ChestScan'].unique()
    print("UNIQUE ChestScan CATEGORIES: \n", unique_entries)
    unique_entries = df['RaceEthnicityCategory'].unique()
    print("UNIQUE RaceEthnicityCategory CATEGORIES: \n", unique_entries)
    unique_entries = df['AgeCategory'].unique()
    print("UNIQUE AgeCategory CATEGORIES: \n", unique_entries)
    unique_entries = df['AlcoholDrinkers'].unique()
    print("UNIQUE AlcoholDrinkers CATEGORIES: \n", unique_entries)
    unique_entries = df['HIVTesting'].unique()
    print("UNIQUE HIVTesting CATEGORIES: \n", unique_entries)
    unique_entries = df['FluVaxLast12'].unique()
    print("UNIQUE FluVaxLast12 CATEGORIES: \n", unique_entries)
    unique_entries = df['PneumoVaxEver'].unique()
    print("UNIQUE PneumoVaxEver CATEGORIES: \n", unique_entries)
    unique_entries = df['TetanusLast10Tdap'].unique()
    print("UNIQUE TetanusLast10Tdap CATEGORIES: \n", unique_entries)
    unique_entries = df['HighRiskLastYear'].unique()
    print("UNIQUE HighRiskLastYear CATEGORIES: \n", unique_entries)
    unique_entries = df['HighRiskLastYear'].unique()
    print("UNIQUE HighRiskLastYear CATEGORIES: \n", unique_entries)
    unique_entries = df['CovidPos'].unique()
    
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
    df['PhysicalActivities'] = df['PhysicalActivities'].map({'No': 0, 'Yes': 1})
    # df['Diabetic'] = df['Diabetic'].map({'No': 0, 'Yes': 1})
    # df['AgeCategory'] = df['AgeCategory'].map({'80 or older': 80,
    #                                                                  '75-79': 76,
    #                                                                  '70-74': 72,
    #                                                                  '65-69': 66, 
    #                                                                  '60-64': 62,
    #                                                                  '55-59': 54,
    #                                                                  '50-54': 52,
    #                                                                  '45-49': 46,
    #                                                                  '40-44': 42,
    #                                                                  '35-39': 36,
    #                                                                  '30-34': 32,
    #                                                                  '25-29': 26,
    #                                                                  '18-24': 21,})
    # df['Stroke'] = df['Stroke'].map({'No': 0, 'Yes': 1})
    # df['Smoking'] = df['Smoking'].map({'No': 0, 'Yes': 1})
    # df['HeartDisease'] = df['HeartDisease'].map({'No': 0, 'Yes': 1})
    # Dropping the 'id' column

    # check the col names and data types
    column_names = df.columns
    print(column_names)
    types = df.dtypes
    print(types)

    return df

def trainNN(input):
    x=input.drop('TenYearCHD',axis=1)
    y=input['TenYearCHD']

    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.2 , random_state = 0)
    model = keras.Sequential()
    model.add(keras.Input(shape=(15,)))
    model.add(keras.layers.Dense(15, activation="tanh"))
    model.add(keras.layers.Dense(15, activation="tanh"))
    model.add(keras.layers.Dense(15, activation="tanh"))
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
    clean_data_set()
    # model = trainNN(clean_data_set())
    # model_pkl_file = "heart_classifier_model.pkl"  

    # with open(model_pkl_file, 'wb') as file:  
    #     pickle.dump(model, file)

if __name__ == "__main__":
    main()