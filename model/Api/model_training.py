import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle

def clean_data_set():
    data=pd.read_csv("model/data_cardiovascular_risk.csv")
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

def train(input):
    x=input.drop('TenYearCHD',axis=1)
    y=input['TenYearCHD']

    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size = 0.2 , random_state = 0)
    RF=RandomForestClassifier(n_estimators=200)
    RF.fit(x_train, y_train)
    y_pred = RF.predict(x_test)
    print("Accuracy:",metrics.accuracy_score(y_test,y_pred))
    return RF

def main():
    model = train(clean_data_set())
    model_pkl_file = "heart_classifier_model.pkl"  

    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)

if __name__ == "__main__":
    main()