import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle
import keras
from keras import layers
from keras import ops

def clean_data_set():
    data=pd.read_csv("model/data/data_cardiovascular_risk.csv")
    df=pd.DataFrame(data)

    df['education'].fillna(df['education'].value_counts().idxmax(), inplace=True)
    df['cigsPerDay'].fillna(df['cigsPerDay'].median(), inplace=True)
    df['BPMeds'].fillna(df['BPMeds'].value_counts().idxmax(), inplace=True)
    df['totChol'].fillna(df['totChol'].median(), inplace=True)
    df['BMI'].fillna(df['BMI'].median(), inplace=True)
    df['heartRate'].fillna(df['heartRate'].median(), inplace=True)
    df['glucose'].fillna(df['glucose'].median(), inplace=True)

    df['sex'] = df.sex.replace(['M', 'F'], [0, 1])
    df['is_smoking'] = df.is_smoking.replace(['YES', 'NO'], [0, 1])
    df.drop(['id'],axis=1,inplace=True)

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
        # metrics=[keras.metrics.BinaryAccuracy(), keras.metrics.FalseNegatives(),],
    )
    
    model.fit(x=x_train, y=y_train)
    
    y_pred = model.predict(x=x_test)

    y_pred = (y_pred > 0.5).astype(int) # convert to binary predictions

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    return model

def main():
    model = trainNN(clean_data_set())
    model_pkl_file = "heart_classifier_model.pkl"  

    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)

if __name__ == "__main__":
    main()