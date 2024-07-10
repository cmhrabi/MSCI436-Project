import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle
import keras
from keras import layers
from keras import ops

def clean_data_set():
    data = pd.read_csv("model/data/2020/heart_2020_cleaned.csv")
    df = pd.DataFrame(data)

    # Replacing categorical values
    df['Sex'] = df['Sex'].map({'Male': 0, 'Female': 1})
    df['Diabetic'] = df['Diabetic'].map({'No': 0, 'Yes': 1, 
                                         'No, borderline diabetes': 2, 'Yes (during pregnancy)':3})
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
    df['Stroke'] = df['Stroke'].map({'No': 0, 'Yes': 1})
    df['Smoking'] = df['Smoking'].map({'No': 0, 'Yes': 1})
    df['HeartDisease'] = df['HeartDisease'].map({'No': 0, 'Yes': 1})
    df['AlcoholDrinking'] = df['AlcoholDrinking'].map({'No': 0, 'Yes': 1})
    df['DiffWalking'] = df['DiffWalking'].map({'No': 0, 'Yes': 1})
    df['Asthma'] = df['Asthma'].map({'No': 0, 'Yes': 1})
    df['Race'] = df['Race'].map({'White': 0, 'Black': 1, 'Asian': 2, 
                                 'American Indian/Alaskan Native': 3, 'Other': 4, 'Hispanic': 5})
    df['PhysicalActivity'] = df['PhysicalActivity'].map({'No': 0, 'Yes': 1})
    df['GenHealth'] = df['GenHealth'].map({'Very good': 0, 'Fair': 1, 'Good': 2, 
                                 'Poor': 3, 'Excellent': 4})
    df['KidneyDisease'] = df['KidneyDisease'].map({'No': 0, 'Yes': 1})
    df['SkinCancer'] = df['SkinCancer'].map({'No': 0, 'Yes': 1})
    
    # check the col names and data types
    # column_names = df.columns
    # print(column_names)
    # types = df.dtypes
    # print(types)

    return df

def trainNN(input):
    x=input.drop('HeartDisease',axis=1)
    y=input['HeartDisease']

    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.2 , random_state = 0)
    model = keras.Sequential()
    model.add(keras.Input(shape=(17,)))
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
    # clean_data_set()
    model = trainNN(clean_data_set())
    model_pkl_file = "indicator_2020_nn.pkl"  

    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)

if __name__ == "__main__":
    main()