# unbabel-translator (Python 2.7)
Unbabel Translator (English --> Spanish)

Installation:
  - Clone this repositary
  - Install dependencies from requirements.txt file (pip install -r requirements.txt)

Run Flask Server (python app.py)
  - cd to cloned directory
  - create postgres database with following credential , apply migrations from models.py
    - {
      'user': 'flask',
      'pw': 'flask',
      'db': 'flask',
      'host': 'localhost',
      'port': '5432',
    }
  - apply migrations on DB
    - select * from base_term;
  - run server with command
    - python app.py
  - Access server on http://127.0.0.1:5000/
  
  
