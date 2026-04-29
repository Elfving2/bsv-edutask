# PA1417 — Tutorial Prep and Introduction

## Part 1: Pre-Tutorial Setup

Complete the following setup steps before attending the tutorial.

### 1. Clone/Download the Repository

Clone/download the testing repository to your local machine using your preferred git client or the command line.

### 2. Install and open VSCode

You can use any code editor you prefer. We will use **Visual Studio Code (VSCode)** as our example during the course, so if you don't have a strong preference, download and install it from [https://code.visualstudio.com](https://code.visualstudio.com). Once installed, open the repository folder in VSCode.

The remaining steps can all be performed using VSCode's integrated terminal (`Terminal → New Terminal`) or any terminal on your local machine of your choosing.

### 3. Confirm Python 3 is installed

Open a terminal and confirm you have Python 3 installed:

```shell
python --version
```

> On some systems (macOS, Linux) Python 3 is accessed via `python3`. Either works. Version 3.10 or newer is recommended.

### 4. Install the dependencies

First, update your local Python Package Installer (pip):

```shell
pip install --upgrade pip
```

Create a virtual environment at the root of the project:

```shell
python -m venv venv
```

Activate the virtual environment before installing anything or running any commands. You must do this every time you open a new terminal for this project.

**macOS / Linux:**

```shell
source venv/bin/activate
```

**Windows:**

```shell
venv\Scripts\activate
```

Once inside the virtual environment, you may want to update the pip inside the environment as well:

```shell
pip install --upgrade pip
```

Your terminal prompt should change to show `(venv)` when the environment is active. Then install the dependencies:

```shell
pip install -r requirements.txt
```

Your setup is correct when this command runs without errors:

```shell
pytest --version
```

### 5. Run the test suite

Confirm pytest can discover and run the existing tests:

```shell
pytest test/_solutions
```

All tests should pass. If you see failures, something is wrong with your setup — re-read the steps above before continuing.

### 6. Configure VSCode

**Select the correct Python interpreter:** Press `Cmd+Shift+P`, type "Python: Select Interpreter", and choose the one pointing to `./venv/bin/python` (macOS/Linux) or `.\venv\Scripts\python.exe` (Windows). If it doesn't appear, select "Enter interpreter path…" and paste the full path.

### 7. Additional Notes

When you are finished with the virtual environment and want to leave, you can either quit your terminal or run the following command from inside your virtual environment:

```shell
deactivate
```

---

## Part 2: Introduction

Complete this section at the start of the tutorial, before beginning any of the topic tutorials. Each topic tutorial focuses on a single concept, but the recommended order reflects genuine dependencies: Mocking Basics assumes fixtures knowledge, and integration tutorials build on unit test skills.

> Throughout the tutorials, the ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

### Orient Yourself

Open the repository in your editor. The structure we care about:

```
pa1417-tutorials/
├── pytest.ini                  ← pytest configuration
├── .pylintrc                   ← pylint configuration (only affects those using pylint)
├── requirements.txt            ← Python dependencies
├── src/                        ← source files you will be testing
└── test/
    ├── student/                ← where you write your tests
    │   ├── unit/
    │   └── integration/
    └── _solutions/             ← reference solutions (try not to peek!)
        ├── unit/
        └── integration/
```

Open `pytest.ini` and read through it. Note the `testpaths` and `addopts` settings — coverage is measured automatically on every run.
