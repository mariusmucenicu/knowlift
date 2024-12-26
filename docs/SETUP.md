### Step 1: Prerequisites
+ Make sure you have any version of **Python 3.6.X**, **3.7.X** installed.
    + If you **haven't got** any of the supported **Python** versions (mentioned above), you can download one from [here](https://www.python.org/).
+ Clone or download this repository locally.
+ [OPTIONAL]: Create a **Python** virtual environment (to isolate the game's package dependencies) and **activate** it.

### Step 2: Change directory into the project root (everything you do will be done from here)

### Step 3: Install package dependencies
```pip install -r requirements.txt```

### Step 4: Running the tests
```python -m unittest discover``` (This command should show absolutely no errors)

### Step 5: Running the game
#### On Windows:
+ Command Prompt:
    + ```set FLASK_APP=wsgi.py```
    + ```set FLASK_ENV=development``` (this activates the debugger and automatic reloader)
    + ```flask run```

+ PowerShell:
    + ```$env:FLASK_APP = "wsgi.py"```
    + ```$env:FLASK_ENV = "development"``` (this activates the debugger and automatic reloader)
    + ```flask run```

#### On Unix:
+ ```export FLASK_APP=wsgi.py```
+ ```export FLASK_ENV=development``` (this activates the debugger and automatic reloader)
+ ```flask run```

Now open your favourite browser and punch in: http://localhost:5000/ or http://127.0.0.1:5000/
