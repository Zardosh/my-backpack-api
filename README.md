# MyBackpack API
An API for the My Backpack application made with Flask

# Requirements

- Python 3
- A MySQL instance

# How to run

1. Create a database named "mybackpack" in the MySQL instance

2. Clone the repository

`git clone https://github.com/Zardosh/my-backpack-api.git`

3. Access the repository

`cd my-backpack-api`

4. Create a venv

`python -m venv venv`

5. Activate the venv

`venv\scripts\activate`

6. Install the required dependencies

`pip install -r requirements.txt`

7. Configure the `config_example.py` file accordingly and rename it to `config.py`

8. Create the tables in the database (type in the console)

```
python
from app import db
db.create_all()
exit()
```

9. Run the API

`python run.py`
