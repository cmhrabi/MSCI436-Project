import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle
import keras
from keras import layers
from keras import ops
from imblearn.over_sampling import SMOTE

def clean_data_set():
    data=pd.read_csv("model/data/data_cardiovascular_risk.csv")
    risk_df=pd.DataFrame(data)

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
    risk_df['is_smoking'] = risk_df['is_smoking'].map({'NO': 0, 'YES': 1})

    # Dropping the 'id' column
    risk_df = risk_df.drop(['id'], axis=1)

    return risk_df

def trainNN(input):
    x=input.drop('TenYearCHD',axis=1)
    y=input['TenYearCHD']

    smote = SMOTE()
    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.2 , random_state = 0)
    x_train, y_train = smote.fit_resample(x_train, y_train)
    model = keras.Sequential()
    model.add(keras.Input(shape=(15,)))
    model.add(keras.layers.Dense(128, activation="relu"))
    model.add(keras.layers.Dropout(.1))
    model.add(keras.layers.Dense(128, activation="relu"))
    model.add(keras.layers.Dropout(.1))
    model.add(keras.layers.Dense(1, activation="sigmoid"))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-5),
        loss=keras.losses.BinaryCrossentropy(),
    )
    
    model.fit(x=x_train, y=y_train, epochs=40)
    
    print(x_test)
    y_pred = model.predict(x=x_test)

    y_pred = (y_pred > 0.5).astype(int) # convert to binary predictions

    count = 0
    for i in y_pred:
        if i == 1:
            count+=1

    count1 = 0
    for i in y_test:
        if i == 1:
            count1+=1

    print(count1)      
    print(count)
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))
    print(metrics.confusion_matrix(y_test, y_pred))
    return model

def main():
    model = trainNN(clean_data_set())
    model_pkl_file = "heart_classifier_model.pkl"  

    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)

if __name__ == "__main__":
    main()