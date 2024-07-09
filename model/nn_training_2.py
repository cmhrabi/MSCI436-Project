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

    # Replacing missing values
    risk_df['education'] = risk_df['education'].fillna(risk_df['education'].value_counts().idxmax())
    risk_df['cigsPerDay'] = risk_df['cigsPerDay'].fillna(risk_df['cigsPerDay'].median())
    risk_df['BPMeds'] = risk_df['BPMeds'].fillna(risk_df['BPMeds'].value_counts().idxmax())
    risk_df['totChol'] = risk_df['totChol'].fillna(risk_df['totChol'].median())
    risk_df['BMI'] = risk_df['BMI'].fillna(risk_df['BMI'].median())
    risk_df['heartRate'] = risk_df['heartRate'].fillna(risk_df['heartRate'].median())
    risk_df['glucose'] = risk_df['glucose'].fillna(risk_df['glucose'].median())

    # Replacing categorical values
    risk_df['sex'] = risk_df['sex'].map({'M': 0, 'F': 1})
    risk_df['is_smoking'] = risk_df['is_smoking'].map({'YES': 0, 'NO': 1})

    # Dropping the 'id' column
    risk_df = risk_df.drop(['id'], axis=1)

    column_names = risk_df.columns
    print(column_names)

    # Key Indicators of Heart Disease 2020
    heart_2020_data = pd.read_csv("model/data/2020/heart_2020_cleaned.csv")
    heart_2020_df = pd.DataFrame(heart_2020_data)
    heart_2020_df.drop(['HeartDisease', 'AlcoholDrinking', 'PhysicalHealth', 'MentalHealth', 'DiffWalking', 'Race', 
                        'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease', 'SkinCancer'], 
                    axis=1, inplace=True)
    column_names = heart_2020_df.columns
    print(column_names)

    # Key Indicators of Heart Disease 2022
    heart_2022_data = pd.read_csv("model/data/2022/heart_2022_no_nans.csv")
    heart_2022_df = pd.DataFrame(heart_2022_data)
    heart_2022_df.drop(['State', 'GeneralHealth', 'PhysicalHealthDays', 'MentalHealthDays', 'LastCheckupTime', 
                        'PhysicalActivities', 'SleepHours', 'RemovedTeeth', 'HadHeartAttack', 'HadAngina', 'HadAsthma', 
                        'HadSkinCancer', 'HadCOPD', 'HadDepressiveDisorder', 'HadKidneyDisease', 'HadArthritis', 
                        'DeafOrHardOfHearing', 'BlindOrVisionDifficulty', 'DifficultyConcentrating', 'DifficultyWalking',
                        'DifficultyDressingBathing', 'DifficultyErrands', 'ECigaretteUsage', 'ChestScan', 'RaceEthnicityCategory',
                        'HeightInMeters', 'WeightInKilograms', 'AlcoholDrinkers', 'HIVTesting', 'FluVaxLast12', 'PneumoVaxEver', 
                        'TetanusLast10Tdap', 'HighRiskLastYear', 'CovidPos'], 
                    axis=1, inplace=True)
    column_names = heart_2022_df.columns
    print(column_names)

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