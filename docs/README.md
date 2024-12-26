# Knowlift

Encapsulates o series of interactive games with the purpose of increasing one's mood. **:iphone: :computer: friendly**

<table>
  <tr>
    <th rowspan="2">State</th>
    <th>Branch</th>
    <th>Status</th>
  </tr>
  <tr>
    <td>Master</td>
    <td>
      <a href="https://github.com/mariusmucenicu/knowlift/actions/workflows/ci.yml?query=branch%3Amaster">
        <img src="https://github.com/mariusmucenicu/knowlift/actions/workflows/ci.yml/badge.svg"></a>
    </td>
  </tr>
  <tr>
    <th>Measurements</th>
    <td colspan="2" align="center">
      <a href="https://codecov.io/gh/mariusmucenicu/knowlift">
        <img src="https://codecov.io/gh/mariusmucenicu/knowlift/branch/master/graph/badge.svg"></a>
    </td>
  </tr>
  <tr>
    <th>To do</th>
    <td colspan="2" align="center">
      <a href="https://github.com/mariusmucenicu/knowlift/issues">
        <img src="https://img.shields.io/github/issues/mariusmucenicu/knowlift.svg"></a>
    </td>
  </tr>
  <tr>
    <th>Progress</th>
    <td colspan="2" align="center">
      <a href="https://github.com/mariusmucenicu/knowlift/compare/1.0.0...master">
        <img src="https://img.shields.io/github/commits-since/mariusmucenicu/knowlift/1.0.0.svg"></a>
    </td>
  </tr>
  <tr>
    <th>Code of Conduct</th>
    <td colspan="2" align="center">
      <a href="https://www.contributor-covenant.org/version/2/1/code_of_conduct/">
        <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg"></a>
    </td>
  </tr>
  <tr>
    <th>License</th>
    <td colspan="2" align="center">
      <a href="https://www.gnu.org/licenses/gpl-3.0">
        <img src="https://img.shields.io/badge/License-GPLv3-blue.svg"></a>
    </td>
  </tr>
</table>

## Contents
+ [Development](https://github.com/mariusmucenicu/knowlift#development)
+ [Versioning](https://github.com/mariusmucenicu/knowlift#versioning)
+ [Code of conduct](https://github.com/mariusmucenicu/knowlift#code-of-conduct)
+ [How can I contribute?](https://github.com/mariusmucenicu/knowlift#how-can-i-contribute)

## Development
In order to get the project started locally, you need to go through these simple steps:

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

## Versioning
This project adheres to [SemVer](http://semver.org/) for versioning.
For the versions available, see the [tags on this repository](https://github.com/mariusmucenicu/knowlift/tags).

- New **major** versions are exceptional and are planned very long in advance.
- New **minor** versions are feature releases; they get released more frequently.
- New **patch** versions are bug fix releases; they get released as needed.

## Code of conduct
This project adheres to the Contributor Covenant [code of conduct](https://github.com/mariusmucenicu/knowlift/blob/master/docs/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How can I contribute?
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.  

- Before filing an **issue** or submitting a **pull request** please make sure you read the [project's contribution guidelines](https://github.com/mariusmucenicu/knowlift/blob/master/docs/CONTRIBUTING.md).
- **Performance-wise**:
    - This is just a fun project, however, one shouldn't wait like seconds between requests and responses.  
