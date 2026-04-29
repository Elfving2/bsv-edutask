# PA1417 — Unit Tests: Parameterization

This tutorial introduces `@pytest.mark.parametrize` for eliminating repetition across test cases that share the same logic but differ only in their data.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## Test Example 1: Eliminating Repetition — `day_type`

Open `src/unit/parameterization/day_type.py` and read the function and its docstring.

✋ **Open `test/student/unit/parameterization/test_day_type.py`. How many test cases does this function need? Write them out without using `@pytest.mark.parametrize` first. What do you notice about the test functions?**

<details>
<summary>What did you observe?</summary>

Every test function is structurally identical — only the day name and expected output differ. Seven functions that share the same logic are seven places to update if anything changes.

`@pytest.mark.parametrize` solves this by letting you write the logic once and supply the data as a list. pytest runs the function once per row and reports each run as a separate test.

</details><br>

✋ **Rewrite your tests using `@pytest.mark.parametrize`. The decorator takes a string naming the parameters and a list of tuples — one tuple per test case.**

<details>
<summary>Hint: parametrize syntax</summary>

```python
import pytest
from src.unit.parameterization.day_type import day_type

@pytest.mark.parametrize("day, expected", [
    ("Monday",   "weekday"),
    ("Saturday", "weekend"),
    # ... remaining cases
])
def test_day_type(day, expected):
    # Arrange
    # (handled by parametrize)
    # Act
    result = day_type(day)
    # Assert
    assert result == expected
```

</details><br>

✋ **The invalid-day case tests different behaviour — an exception rather than a return value. Should it go in the parametrize table or stay as its own function?**

<details>
<summary>Answer</summary>

Keep it as its own function. `@pytest.mark.parametrize` is for cases where the test logic is identical and only the data changes. An exception test has different logic (`pytest.raises`), so it does not belong in the table.

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/unit/parameterization/test_day_type.py](../test/_solutions/unit/parameterization/test_day_type.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass.

## Test Example 2: Parametrize with an Infinite Domain — `is_palindrome`

Open `src/unit/parameterization/palindrome.py` and read the function and its docstring.

Unlike `day_type`, which had exactly seven possible inputs, `is_palindrome` accepts any string — the input domain is infinite. You cannot write a test for every possible input. What you can do is choose a representative sample that covers the cases that matter.

✋ **Before writing any tests, think about which cases are worth testing. What kinds of strings should you cover?**

<details>
<summary>Hint: Representative Cases</summary>

| Case                       | Example     | Expected |
| -------------------------- | ----------- | -------- |
| empty string               | `""`        | `True`   |
| single character           | `"a"`       | `True`   |
| odd-length palindrome      | `"racecar"` | `True`   |
| even-length palindrome     | `"noon"`    | `True`   |
| not a palindrome           | `"hello"`   | `False`  |
| another non-palindrome     | `"world"`   | `False`  |
| case-sensitivity edge case | `"Racecar"` | `False`  |

This is equivalence partitioning applied to an infinite domain — you cannot test everything, so you identify the distinct kinds of input and pick one example from each.

</details><br>

✋ **Create `test/student/unit/parameterization/test_palindrome.py` and write the tests using `@pytest.mark.parametrize`.**

Once you're ready to compare, open the solution: [test/\_solutions/unit/parameterization/test_palindrome.py](../test/_solutions/unit/parameterization/test_palindrome.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass.

## Test Example 3: Multiple Input Parameters and Readable IDs — `triangle_type`

Open `src/unit/parameterization/triangle_type.py` and read the function and its docstring. It takes three arguments rather than one.

When a function takes multiple inputs, the parametrize string lists all of them separated by commas, and each tuple in the data list must contain a value for every parameter plus the expected output.

With numeric inputs like `(3, 3, 3)`, pytest generates test names like `test_triangle_type[3-3-3]`. This is not very readable. `pytest.param` lets you attach an explicit `id` to each case so the output reads like `test_triangle_type[all-sides-equal]` instead.

✋ **Create `test/student/unit/parameterization/test_triangle_type.py`. Write a parametrized test covering equilateral, isosceles (all three orientations), and scalene (two different representatives, to show the same logic works for different proportions). Use `pytest.param(..., id="...")` for each case so the test names are human-readable.**

<details>
<summary>Hint: multi-argument tuples and pytest.param IDs</summary>

```python
import pytest
from src.unit.parameterization.triangle_type import triangle_type

@pytest.mark.parametrize("a, b, c, expected", [
    pytest.param(3, 3, 3, "equilateral", id="all-sides-equal"),
    pytest.param(3, 3, 5, "isosceles",   id="isosceles-first-two-match"),
    pytest.param(3, 4, 5, "scalene",     id="scalene"),
    # ... remaining cases
])
def test_triangle_type(a, b, c, expected):
    result = triangle_type(a, b, c)
    assert result == expected
```

> **When to use IDs:** Use `pytest.param(..., id="...")` whenever the raw input values do not clearly communicate what case is being tested. Numeric tuples like `(1, 2, 10)` give no hint that this is an "invalid triangle" case — an explicit `id` fixes that.

</details><br>

✋ **The two error cases (non-positive side, violated triangle inequality) raise exceptions. Should they go in the table or stay as separate functions?**

<details>
<summary>Answer</summary>

Keep them as separate functions. They use `pytest.raises`, which is different logic from the main assertion. The data table is for cases where the test logic is identical — only the data differs. Exception tests have a structurally different body.

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/unit/parameterization/test_triangle_type.py](../test/_solutions/unit/parameterization/test_triangle_type.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass. Observe the readable test names in the output.

## Summary

| Source file       | Tests | Concepts practised                                                          |
| ----------------- | ----- | --------------------------------------------------------------------------- |
| `day_type.py`     | 8     | `@pytest.mark.parametrize`, finite domain, when to use vs not              |
| `palindrome.py`   | 7     | `@pytest.mark.parametrize`, infinite domain, representative set             |
| `triangle_type.py`| 8     | Multi-argument tuples, `pytest.param` IDs, exception tests kept separate   |

> **Key idea:** Use `@pytest.mark.parametrize` when multiple test cases share identical logic and differ only in their inputs and expected outputs. Keep exception tests as separate functions — they have different logic and do not belong in the data table. When test IDs generated from raw values are unreadable, use `pytest.param(..., id="...")` to name each case explicitly.
