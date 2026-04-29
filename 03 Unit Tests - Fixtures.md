# PA1417 — Unit Tests: Assert

This tutorial introduces unit testing in Python using pytest. You will write tests for three simple functions, progressively building confidence with the AAA pattern and equivalence partitioning.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## Test Example 1: `sign`

### Step 1: Designing Test Cases

Open `src/unit/asserts/sign.py` and read the function and its docstring. Before writing any code, derive the test cases from the _documentation_, not the code.

✋ **Use equivalence partitioning to decide which tests you need. How many distinct cases exist? What is one representative input for each?**

<details>
<summary>Hint: Test Case Table</summary>

```
sign(n: int) -> str
  "negative" — if n < 0
  "zero"     — if n == 0
  "positive" — if n > 0
```

| #   | `n`  | Expected   |
| --- | ---- | ---------- |
| 1   | < 0  | "negative" |
| 2   | == 0 | "zero"     |
| 3   | > 0  | "positive" |

Three mutually exclusive, exhaustive cases — three tests gives full coverage.

> **Principle:** Derive test cases from the documentation or specification, not from the code. Code is not ground truth.

</details><br>

### Step 2: Writing the First Tests — `test_sign.py`

Open `test/student/unit/asserts/test_sign.py`. The file already has the import and a TODO comment.

✋ **Stop here. Let's write the first test together.**

Every test follows the **AAA pattern**:

1. **Arrange** — set up any data or preconditions the test needs
2. **Act** — call the function under test and capture the result
3. **Assert** — verify the result matches what you expect

```python
def test_negative():
    # Arrange
    # (nothing to set up)
    # Act
    result = sign(-1)
    # Assert
    assert result == "negative"
```

> **Principle:** One `assert` per test. If the first assert fails, you still want to know whether the others pass or fail — multiple asserts in one test hides that information.

✋ **Stop here. Write the remaining two test functions for `sign` before moving on.**

<details>
<summary>Solution</summary>

```python
def test_zero():
    # Arrange
    # (nothing to set up)
    # Act
    result = sign(0)
    # Assert
    assert result == "zero"

def test_positive():
    # Arrange
    # (nothing to set up)
    # Act
    result = sign(1)
    # Assert
    assert result == "positive"
```

</details><br>

### Step 3: Running pytest and Reading the Output

✋ **Run `pytest test/student/unit/asserts/test_sign.py -v` from the repository root and read the output before continuing.**

Pytest prints one character per test:

- `.` — passed
- `F` — failed
- `E` — error during setup or teardown

When all three pass you will see a coverage table. Because `pytest.ini` sets `--cov-report term-missing --cov=src`, coverage is measured automatically. The **Missing** column shows which lines were never executed. Confirm that `sign.py` shows 100% coverage.

## Test Example 2: `fizzbuzz`

### Step 1: Designing Test Cases

Open `src/unit/asserts/fizzbuzz.py` and read the function and its docstring.

✋ **Use equivalence partitioning to derive the test cases. How many distinct cases exist?**

<details>
<summary>Hint: Test Case Table</summary>

```
fizzbuzz(n: int) -> str
  "FizzBuzz" — divisible by both 3 and 5
  "Fizz"     — divisible by 3 only
  "Buzz"     — divisible by 5 only
  str(n)     — not divisible by 3 or 5
```

| #   | Condition            | Example input | Expected   |
| --- | -------------------- | ------------- | ---------- |
| 1   | divisible by 3 and 5 | 15            | "FizzBuzz" |
| 2   | divisible by 3 only  | 9             | "Fizz"     |
| 3   | divisible by 5 only  | 10            | "Buzz"     |
| 4   | divisible by neither | 7             | "7"        |

</details><br>

### Step 2: Writing the Tests — Create `test_fizzbuzz.py` Yourself

✋ **There is no starter file this time. Create `test/student/unit/asserts/test_fizzbuzz.py` and write all four test functions following the same AAA pattern as `test_sign.py`.**

Once you're ready to compare, open the solution: [test/\_solutions/unit/asserts/test_fizzbuzz.py](../test/_solutions/unit/asserts/test_fizzbuzz.py)

Run `pytest test/student/unit/ -v` and confirm all seven tests pass (three from `test_sign.py`, four from `test_fizzbuzz.py`).

## Test Example 3: `age_classifier`

Open `src/unit/asserts/age_classifier.py` and read the function and its docstring.

✋ **Use equivalence partitioning to derive the test cases. This function has more partitions than the previous two — and one of them requires a different kind of assert.**

<details>
<summary>Hint: Test Case Table</summary>

```
classify_age(age: int) -> str
  "infant"   — 0 to 2
  "child"    — 3 to 12
  "teenager" — 13 to 17
  "adult"    — 18 to 64
  "senior"   — 65 and above

  raises ValueError — if age is negative
```

| #   | `age` | Expected          |
| --- | ----- | ----------------- |
| 1   | 1     | "infant"          |
| 2   | 8     | "child"           |
| 3   | 15    | "teenager"        |
| 4   | 30    | "adult"           |
| 5   | 70    | "senior"          |
| 6   | -1    | raises ValueError |

For case 6, use `pytest.raises` as a context manager:

```python
import pytest

def test_negative_age_raises():
    # Arrange
    # (nothing to set up)
    # Act / Assert
    with pytest.raises(ValueError):
        classify_age(-1)
```

</details><br>

✋ **There is no starter file this time. Create `test/student/unit/asserts/test_age_classifier.py` yourself and write all six tests.**

Once you're ready to compare, open the solution: [test/\_solutions/unit/asserts/test_age_classifier.py](../test/_solutions/unit/asserts/test_age_classifier.py)

> **Principle:** In real projects you always create the test file yourself. The file name must start with `test_` and each function name must start with `test_` for pytest to discover them automatically.

Run `pytest test/student/unit/ -v` and confirm all thirteen tests pass with 100% coverage across all three source files.

## Summary

| Source file         | Tests | Concepts practised                              |
| ------------------- | ----- | ----------------------------------------------- |
| `sign.py`           | 3     | AAA pattern, first `assert`, 3 partitions       |
| `fizzbuzz.py`       | 4     | Multiple conditions, equivalence partitions     |
| `age_classifier.py` | 6     | More partitions, `pytest.raises`, own file      |

> **Key idea:** Equivalence partitioning lets you identify the minimum number of tests needed for full logical coverage. More tests are not always better — redundant tests add maintenance cost without adding confidence.
