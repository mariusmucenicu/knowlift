# Setup

### 🔧 Step 1: Prerequisites
+ Make sure you have any Python 3.11+ version installed.
+ Clone or download this repository.
+ Change directory into the project root.

### 📦 Step 2: Install dependencies
```
pip install -r requirements.txt
```

### ✅ Step 3: Run the test suite
```
python -m unittest discover
```
This command should show absolutely no errors.

### 🚀 Step 4: Run the application
Pick the runtime environment by setting the env var `KNOWLIFT_ENV`.

#### Windows (Command Prompt)
```
set KNOWLIFT_ENV=development
flask run
```

#### Windows (PowerShell)
```
$env:KNOWLIFT_ENV = "development"
flask run
```

#### Unix
```
export KNOWLIFT_ENV=development
flask run
```

Open your favourite browser at http://127.0.0.1:5000/ and give it a try 🎉
