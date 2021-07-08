```
    .
    ├── api
    │   ├── __init__.py
    │   ├── database.db                  # database file
    │   ├── database.py                  # database creation
    │   ├── main.py                      # routes definition
    │   ├── models.py 
    │   ├── schemas.py
    │   └── services.py                  # function for requesting api
    ├── models
    │   └── LogisticRegression.joblib
    ├── scripts
    │   ├── __init__.py
    │   ├── CONST.py
    │   └── functions.py                 # utils functions
    ├── app_components.py                # components for streamlit
    ├── app.py                           # streamlit application
    ├── README.md
    └── requirements.txt
```
## Setup
--------------------------------
- run database.py
- 1st terminal :
    streamlit run app.py

- 2nd terminal :
    cd api
     uvicorn main:app.py