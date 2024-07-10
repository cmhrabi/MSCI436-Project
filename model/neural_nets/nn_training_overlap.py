import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle
import keras
from keras import layers
from keras import ops

def clean_data_sets():
    # risk of coronary heart disease CHD
    risk_data = pd.read_csv("model/data/data_cardiovascular_risk.csv")
    risk_df = pd.DataFrame(risk_data)

    # Dropping the non overlapping cols
    risk_df.drop(['id', 'education', 'cigsPerDay', 'BPMeds', 'totChol', 'heartRate', 'prevalentHyp', 
                  'diaBP', 'glucose', 'sysBP'], axis=1, inplace=True)

    # Replacing missing values
    risk_df['BMI'] = risk_df['BMI'].fillna(risk_df['BMI'].median())

    # Replacing categorical values
    risk_df['sex'] = risk_df['sex'].map({'M': 0, 'F': 1})
    risk_df['is_smoking'] = risk_df['is_smoking'].map({'YES': 0, 'NO': 1})

    column_names = risk_df.columns
    print(column_names)
    types = risk_df.dtypes
    print(types)
    # print(risk_df.head())

    # Key Indicators of Heart Disease 2020
    heart_2020_data = pd.read_csv("model/data/2020/heart_2020_cleaned.csv")
    heart_2020_df = pd.DataFrame(heart_2020_data)
    heart_2020_df.drop(['AlcoholDrinking', 'PhysicalHealth', 'MentalHealth', 'DiffWalking', 'Race', 
                        'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease', 'SkinCancer'], 
                    axis=1, inplace=True)
    
    unique_entries = heart_2020_df['Diabetic'].unique()
    print("Diabetic values: \n", unique_entries)

    # Replacing missing values for 'Diabetic'
    heart_2020_df['Diabetic'] = heart_2020_df['Diabetic'].fillna('No')
    unique_entries = heart_2020_df['Diabetic'].unique()
    print("Diabetic values: \n", unique_entries)
    

    # Replacing categorical values
    heart_2020_df['Sex'] = heart_2020_df['Sex'].map({'Male': 0, 'Female': 1})
    heart_2020_df['Diabetic'] = heart_2020_df['Diabetic'].map({'No': 0, 'Yes': 1})
    heart_2020_df['AgeCategory'] = heart_2020_df['AgeCategory'].map({'80 or older': 80,
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
    heart_2020_df['Stroke'] = heart_2020_df['Stroke'].map({'No': 0, 'Yes': 1})
    heart_2020_df['Smoking'] = heart_2020_df['Smoking'].map({'No': 0, 'Yes': 1})
    heart_2020_df['HeartDisease'] = heart_2020_df['HeartDisease'].map({'No': 0, 'Yes': 1})
    
    column_names = heart_2020_df.columns
    print(column_names)
    types = heart_2020_df.dtypes
    print(types)
    # print(heart_2020_df.head())


    # Key Indicators of Heart Disease 2022
    heart_2022_data = pd.read_csv("model/data/2022/heart_2022_no_nans.csv")
    heart_2022_df = pd.DataFrame(heart_2022_data)
    heart_2022_df.drop(['State', 'GeneralHealth', 'PhysicalHealthDays', 'MentalHealthDays', 'LastCheckupTime', 
                        'PhysicalActivities', 'SleepHours', 'RemovedTeeth', 'HadAngina', 'HadAsthma', 
                        'HadSkinCancer', 'HadCOPD', 'HadDepressiveDisorder', 'HadKidneyDisease', 'HadArthritis', 
                        'DeafOrHardOfHearing', 'BlindOrVisionDifficulty', 'DifficultyConcentrating', 'DifficultyWalking',
                        'DifficultyDressingBathing', 'DifficultyErrands', 'ECigaretteUsage', 'ChestScan', 'RaceEthnicityCategory',
                        'HeightInMeters', 'WeightInKilograms', 'AlcoholDrinkers', 'HIVTesting', 'FluVaxLast12', 'PneumoVaxEver', 
                        'TetanusLast10Tdap', 'HighRiskLastYear', 'CovidPos'], 
                    axis=1, inplace=True)
    # unique_entries = heart_2022_df['AgeCategory'].unique()
    # print("UNIQUE AGE CATEGORIES: \n", unique_entries)
    # column_names = heart_2022_df.columns
    # print(column_names)
    # types = heart_2022_df.dtypes
    # print(types)
    # print(heart_2022_df.head())

    return risk_df, heart_2020_df, heart_2022_data

def trainNN(risk_df, heart_2020_df, heart_2022_data):

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
        # metrics=[keras.metrics.BinaryAccuracy(), keras.metrics.FalseNegatives(),],
    )
    
    model.fit(x=x_train, y=y_train)
    
    y_pred = model.predict(x=x_test)

    y_pred = (y_pred > 0.5).astype(int) # convert to binary predictions

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    return model

def main():
    clean_data_sets()
    # model = trainNN(clean_data_sets())
    # model_pkl_file = "heart_classifier_model.pkl"  

    # with open(model_pkl_file, 'wb') as file:  
    #     pickle.dump(model, file)

if __name__ == "__main__":
    main()