import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle
import keras
from keras import layers
from keras import ops

def combine_similar_columns(risk_df, heart_2020_df, heart_2022_df):
    # Map columns with similar meanings
    risk_df = risk_df.rename(columns={
        'sex': 'Sex',
        'is_smoking': 'Smoking',
        'prevalentStroke': 'Stroke',
        'diabetes': 'Diabetic',
        'age': 'AgeCategory',
        'TenYearCHD': 'HeartDisease'
    })
    
    heart_2020_df = heart_2020_df.rename(columns={
        'Diabetic': 'Diabetes'
    })
    
    heart_2022_df = heart_2022_df.rename(columns={
        'HadHeartAttack': 'HeartDisease',
        'HadStroke': 'Stroke',
        'HadDiabetes': 'Diabetes',
        'SmokerStatus': 'Smoking'
    })
    
    # Combine the dataframes
    combined_df = pd.concat([risk_df, heart_2020_df, heart_2022_df], ignore_index=True)
    
    return combined_df

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


    # Key Indicators of Heart Disease 2020
    heart_2020_data = pd.read_csv("model/data/2020/heart_2020_cleaned.csv")
    heart_2020_df = pd.DataFrame(heart_2020_data)
    heart_2020_df.drop(['AlcoholDrinking', 'PhysicalHealth', 'MentalHealth', 'DiffWalking', 'Race', 
                        'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease', 'SkinCancer'], 
                    axis=1, inplace=True)
    
    # Replacing categorical values
    heart_2020_df['Sex'] = heart_2020_df['Sex'].map({'Male': 0, 'Female': 1})
    heart_2020_df['Diabetic'] = heart_2020_df['Diabetic'].map({'No': 0, 'Yes': 1, 
                                         'No, borderline diabetes': 2, 'Yes (during pregnancy)':3})
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
    
    # Key Indicators of Heart Disease 2022
    heart_2022_df['Sex'] = heart_2022_df['Sex'].map({'Male': 0, 'Female': 1})
    heart_2022_df['HadHeartAttack'] = heart_2022_df['HadHeartAttack'].map({'No': 0, 'Yes': 1})
    heart_2022_df['HadStroke'] = heart_2022_df['HadStroke'].map({'No': 0, 'Yes': 1})
    heart_2022_df['HadDiabetes'] = heart_2022_df['HadDiabetes'].map({'No': 0, 'Yes': 1, 
                                                 'No, pre-diabetes or borderline diabetes': 2, 'Yes, but only during pregnancy (female)':3})
    heart_2022_df['SmokerStatus'] = heart_2022_df['SmokerStatus'].map({'Former smoker': 0, 'Never smoked': 1,
                                                  'Current smoker - now smokes every day': 2,
                                                  'Current smoker - now smokes some days':3})
    heart_2022_df['AgeCategory'] = heart_2022_df['AgeCategory'].map({'Age 80 or older': 80,
                                                'Age 75 to 79': 76,
                                                'Age 70 to 74': 72,
                                                'Age 65 to 69': 66, 
                                                'Age 60 to 64': 62,
                                                'Age 55 to 59': 54,
                                                'Age 50 to 54': 52,
                                                'Age 45 to 49': 46,
                                                'Age 40 to 44': 42,
                                                'Age 35 to 39': 36,
                                                'Age 30 to 34': 32,
                                                'Age 25 to 29': 26,
                                                'Age 18 to 24': 21})

    combined_df = combine_similar_columns(risk_df, heart_2020_df, heart_2022_df)

    return combined_df

def trainNN(input):

    x=input.drop('HeartDisease',axis=1)
    y=input['HeartDisease']

    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.2 , random_state = 0)
    model = keras.Sequential()
    model.add(keras.Input(shape=(7,)))
    model.add(keras.layers.Dense(7, activation="tanh"))
    model.add(keras.layers.Dense(7, activation="tanh"))
    model.add(keras.layers.Dense(7, activation="tanh"))
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
    model = trainNN(clean_data_sets())
    model_pkl_file = "heart_classifier_model.pkl"  

    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)

if __name__ == "__main__":
    main()