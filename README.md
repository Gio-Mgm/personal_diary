```
    .
    ├── models
    │   └── LogisticRegression.joblib
    ├── src
    |   └── api
    |   │   ├── database.db             # database file
    |   │   ├── database.py             # database creation
    |   │   ├── main.py                 # routes definition
    |   │   ├── models.py               # define database structure
    |   │   ├── schemas.py              # classes declaration for pydantic
    |   │   └── services.py             # services for API requests
    |   └── utils
    |       ├── CONST.py                # constants
    |       └── functions.py            # utils functions
    ├── app_components.py               # components for streamlit
    ├── app.py                          # streamlit application
    ├── README.md
    └── requirements.txt
```

## Setup
--------------------------------
- run database.py
- 1st terminal :
    streamlit run app.py

- 2nd terminal :
    cd src/api
     uvicorn main:app.py