# Todo App

This is a simple Todo application built using Python and SQLite. The application allows users to add, view, update and delete tasks. The data is stored in a SQLite database and the front-end is rendered using the Jinja2 template engine.

## Requirements
- Python 3.x
- Flask
- SQLite3

## Installation
1. Clone the repository git clone 

    `https://github.com/nguynnga23/PROJECT_Quality-assurance-and-software-testing.git`

2. Install the required packages
    
    `pip install -r requirements.txt`

3. Create the database
    
    `python db_create.py`

## Usage
1. Start the development server
    `python app.py`

2. Open `http://localhost:5000` in your web browser
3. Run tests
- Run Unit Tests (unittest)
    `python -m unittest -v tests/test_app.py`
- Run Integration Tests (pytest)
    `python -m pytest -v tests/test_integration.py`
- Run Functional Tests (selenium)
   ....
- Run Acceptance Tests (behave)
    `cd .\tests\features\`
    `behave`
"# PROJECT_Quality-assurance-and-software-testing" 
