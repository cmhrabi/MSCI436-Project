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

    column_names = df.columns
    print(column_names)
    types = df.dtypes
    print(types)

    # Replacing missing values

    # Replacing categorical values
    # risk_df['sex'] = risk_df['sex'].map({'M': 0, 'F': 1})
    # risk_df['is_smoking'] = risk_df['is_smoking'].map({'YES': 0, 'NO': 1})

    # Dropping the 'id' column

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