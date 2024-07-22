# MSCI436-Project
Project for MSCI436 predicting being at risk of heart disease

## Deployment Steps
Contact chrabi@uwaterloo.ca if you are having any trouble

### Backend server
Windows
```
python -m venv env
env\Scripts\activate
python -m pip install -r model/requirements.txt

python model/Api/app.py
```

Mac/Linux
```
python -m venv env
source env/bin/activate
python -m pip install -r model/requirements.txt

python model/Api/app.py
```

### Frontend
```
cd frontend
npm install
npm start
```
