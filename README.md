# 📋 Backend part of Name of the Project


---


## 📚 Table of Contents

- [🛠 Prerequisites](#prerequisites)
- [🚀 Project Quick Start](#project-quick-start)
- [⚙️ Local Run](#local-run)
- [✨ Code Style and Linting](#code-style-and-linting)
  - [Ruff Usage](#ruff-usage)
  - [MyPy Usage](#mypy-usage)
- [🔧 Pre-commit Hooks](#pre-commit-hooks)
- [🧪 Running Tests](#running-tests)


---


<a id="prerequisites"></a>
## 🛠 Prerequisites
- Poetry == 2.1.3


---


<a id="project-quick-start"></a>
## 🚀 Project quick start
1. Clone the repo

Bash

    git clone {link of the project}
    cd {name of the project}

2. Set up environment
   - Copy .env.template to .env and fill in required variables.
   - Ask someone from development team about environment variables.
3. Install Python dependencies for local development

Bash

     poetry install --with dev


     Then install git hooks:


Bash

     poetry run pre-commit install

4. Run the application

Bash

    python entrypoint_api.py

    OR\
    Setup run via PyCharm or VSCode with entrypoint_api.py as the main module and don't forget to set the .env file.

---


<a id="local-run"></a>
## ⚙️ Local Runner (Standalone Rules Evaluation)
1. Set up environment variables for local run in `.env` file

   | Variable | Description |
   |----------|-------------|
   | LOCAL_RUN_DIAL_API_KEY    | Your API key used to authenticate to DIAL Core. |
   | LOCAL_RUN_CONTRACT_NAME   | Name of the file inside eval/documents/ to evaluate. |
   | LOCAL_RUN_CONFIG_PATH     | Path to config JSON. |
   | LOCAL_RUN_DOCUMENT_TYPE_ID| Filters configuration rules by document type. |
   | LOCAL_RUN_ROUNDS          | Number of repeated evaluations |

2. Preparing Input Files
   - Put your document DOCX inside eval/documents/
3. Running Local Evaluation

Bash

    python local_run_entrypoint.py


---

<a id="code-style-and-linting"></a>
## ✨ Code Style and Linting
This project uses Ruff as the primary tool for linting, import sorting, and formatting validation.

<a id="ruff-usage"></a>
### 🧹 Ruff Usage:

1. Run linting checks:
Bash

  poetry run ruff check .

2. Run linting check and fix:
Bash

  poetry run ruff check . --fix

3. Run code formatting:
Bash

  poetry run ruff format .

<a id="mypy-usage"></a>
### 🔍 MyPY Usage:
1. Run type checking:
Bash

  poetry run mypy --show-error-codes src tests


---

<a id="pre-commit-hooks"></a>
## 🔧 Pre-commit Hooks
1. 🔌 Install the pre-commit hook:
Bash

  poetry run pre-commit install

2. ♻️ Update the pre-commit hooks:
Bash

    pre-commit install
Bash

    pre-commit autoupdate
Bash

    pre-commit install
Bash

    pre-commit run --all-files

3. ▶️ Run all pre-commit checks manually:
Bash

  pre-commit run --all-files


---


<a id="running-tests"></a>
## 🧪 Running Tests
1. ▶️ Run all tests:

Bash

   poetry run pytest

2. 📊 Run tests with coverage report:

Bash

   poetry run pytest --cov=src

3. 🎯 Run specific test file:xw

Bash

   poetry run pytest tests/test_your_test_file.py

4. 🔎 Run specific test function:

Bash

   poetry run pytest tests/test_your_test_file.py::test_your_function

5. 📈 Generate coverage report in HTML:

Bash

   poetry run pytest --cov=src --cov-report=html

   - Open htmlcov/index.html in your browser to view the report.

---
