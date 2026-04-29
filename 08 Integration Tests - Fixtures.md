# PA1417 — Integration Tests: Basics

This tutorial introduces integration testing by showing its simplest form: two classes in different source files, both running for real, tested together with no mocking and no external resources.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## What makes something an integration test?

A **unit test** isolates one class completely — every dependency is replaced with a mock. An **integration test** lets two or more real components run together. The test verifies that they collaborate correctly, not just that each works in isolation.

The line between integration and unit is not complexity — it is the number of real components involved. The tests in this tutorial are short and contain no mocking. They are integration tests purely because both `TipCalculator` and `BillSplitter` run with their real implementations.

## Test Example 1: `TipCalculator` and `BillSplitter`

### Step 1: Read the Components

Open [src/integration/basics/tip_calculator.py](../src/integration/basics/tip_calculator.py) and read the class. `TipCalculator` has one method: `calculate(amount, tip_percent)`, which returns the tip as a rounded monetary amount.

Open [src/integration/basics/bill_splitter.py](../src/integration/basics/bill_splitter.py) and read the class. `BillSplitter` accepts a `TipCalculator` in its constructor and uses it inside `split(bill, tip_percent, num_people)` to compute the share each person owes.

Notice that neither class reads or writes any external resource — no file, no network, no database. This means there is nothing to clean up after each test, so no `yield`-based teardown fixture is needed.

### Step 2: Write the Integration Tests

Open `test/student/integration/basics/test_bill_splitter_integration.py`.

✋ **Write at least three tests. In each test, create a real `TipCalculator` and pass it to a real `BillSplitter`, then call `split()` and assert the result.**

<details>
<summary>Hint: test structure</summary>

```python
from src.integration.basics.tip_calculator import TipCalculator
from src.integration.basics.bill_splitter import BillSplitter

def test_split_ten_percent_tip_among_two():
    # Arrange — both components are real
    calculator = TipCalculator()
    splitter = BillSplitter(calculator)
    # Act
    result = splitter.split(bill=100.0, tip_percent=10.0, num_people=2)
    # Assert: bill=100, tip=10, total=110, each person owes 55
    assert result == 55.0
```

</details><br>

Suggested test cases:

- A standard tip (e.g. 10 %) split between two people
- A zero-tip case (no tip, just the bill divided evenly)
- A case that involves rounding (e.g. 15 % tip split among three people)

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/basics/test_bill_splitter_integration.py](../test/_solutions/integration/basics/test_bill_splitter_integration.py)

## Test Example 2: `ScoreNormalizer` and `GradeAssigner`

Open [src/integration/basics/score_normalizer.py](../src/integration/basics/score_normalizer.py). `ScoreNormalizer` has one method: `percentage(score, max_score)`, which returns the score as a percentage rounded to one decimal place.

Open [src/integration/basics/grade_assigner.py](../src/integration/basics/grade_assigner.py). `GradeAssigner` accepts a `ScoreNormalizer` in its constructor and uses it inside `assign(score, max_score)` to return a letter grade.

The grade boundaries are: A (90 %+), B (75–89 %), C (60–74 %), D (50–59 %), F (below 50 %).

✋ **Create `test/student/integration/basics/test_grade_assigner_integration.py`. Write at least five tests — one for each grade level (A through F). In each test, create a real `ScoreNormalizer` and pass it to a real `GradeAssigner`.**

<details>
<summary>Hint: test structure</summary>

```python
from src.integration.basics.score_normalizer import ScoreNormalizer
from src.integration.basics.grade_assigner import GradeAssigner

def test_perfect_score_is_grade_a():
    normalizer = ScoreNormalizer()
    assigner = GradeAssigner(normalizer)
    assert assigner.assign(100, 100) == "A"
```

</details><br>

> **Why is this still an integration test?** `GradeAssigner.assign` calls `normalizer.percentage` to get the percentage, then applies its own threshold logic. A unit test of `GradeAssigner` would mock the normalizer and pass in percentages directly — the collaboration between the two classes would never run. The integration test exercises both.

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/basics/test_grade_assigner_integration.py](../test/_solutions/integration/basics/test_grade_assigner_integration.py)

## Test Example 3: A Component That Calls Its Dependency Multiple Times — `PriceFormatter` and `ReceiptPrinter`

Open [src/integration/basics/price_formatter.py](../src/integration/basics/price_formatter.py). `PriceFormatter` has one method: `format(amount)`, which returns a price string like `"12.50 SEK"`.

Open [src/integration/basics/receipt_printer.py](../src/integration/basics/receipt_printer.py). `ReceiptPrinter` accepts a `PriceFormatter` in its constructor and uses it inside `print_receipt(items)`, which takes a list of `(name, price)` tuples and returns a list of formatted strings — one per item. The formatter is called once for every item in the list.

This differs from the previous examples: the second component calls the first component's method in a loop rather than once. The integration test therefore verifies not just that the two components connect correctly, but that the loop produces the right output for every element.

✋ **Create `test/student/integration/basics/test_receipt_printer_integration.py`. Write at least four tests: an empty list, a single item, multiple items (check count and content), and items appearing in the correct order.**

<details>
<summary>Hint: test structure</summary>

```python
from src.integration.basics.price_formatter import PriceFormatter
from src.integration.basics.receipt_printer import ReceiptPrinter

def test_empty_items_returns_empty_list():
    formatter = PriceFormatter()
    printer = ReceiptPrinter(formatter)
    assert printer.print_receipt([]) == []

def test_single_item_receipt():
    formatter = PriceFormatter()
    printer = ReceiptPrinter(formatter)
    result = printer.print_receipt([("Apple", 1.5)])
    assert result == ["  Apple: 1.50 SEK"]
```

</details><br>

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/basics/test_receipt_printer_integration.py](../test/_solutions/integration/basics/test_receipt_printer_integration.py)

## Summary

| Source files | Tests | Concepts practised |
| --- | --- | --- |
| `tip_calculator.py`, `bill_splitter.py` | 3 | Integration testing, two real components, no mocking, no teardown |
| `score_normalizer.py`, `grade_assigner.py` | 6 | Two components, result of A feeds into conditional logic of B |
| `price_formatter.py`, `receipt_printer.py` | 4 | Two components, B calls A's method once per item in a loop |

> **Key idea:** An integration test can be as simple as this — no mocking, no fixtures, no setup. The distinguishing feature is that two real classes collaborate. If you replaced either dependency with a `MagicMock()`, you would be writing a unit test instead, because the real collaboration logic would no longer run.
