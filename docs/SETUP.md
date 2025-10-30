# Setup

### 📁 Step 1: Get the source code
+ Get the repository via HTTPS or SSH.
+ Change directory into the project root.

### 🔧 Step 2: Install uv
Install the **uv package manager** by following the steps [here][uv-install].

### 📦 Step 3: Install dependencies
```
uv sync --locked
```

### ✅ Step 4: Run the test suite
```
uv run python -m unittest discover
```

### 🚀 Step 5: Run the application
```
uv run flask run
```

Open your favourite browser at http://127.0.0.1:5000/ and give it a try 🎉

[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
