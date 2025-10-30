# Setup

## 📁 Step 1: Get the source code
Get the repository via HTTPS or SSH and change directory into the project root.

## 🔧 Step 2: Install uv
Install the **uv package manager** by following the steps [here][uv-install].

## 📦 Step 3: Install dependencies
```zsh
uv sync --locked
```

## ✅ Step 4: Run the test suite
```zsh
uv run python -m unittest discover
```

## 🚀 Step 5: Run the application
```zsh
uv run flask run
```

Open a new tab at [http://127.0.0.1:5000/](flask-app) and give it a try 🎉.

[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
[flask-app]: http://127.0.0.1:5000/
