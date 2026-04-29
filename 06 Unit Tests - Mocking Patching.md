# PA1417 — Unit Tests: Mocking Basics

This tutorial introduces mocking — replacing a real dependency with a controlled stand-in so your tests are not blocked by external systems. You will apply `MagicMock` to classes that receive their dependencies via the constructor, learning how to set fixed return values and how to share mock setup across multiple tests using a fixture.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## What is a mock, and why do we use one?

A class that depends on an external service — a weather API, a pricing database, a bank rate feed — cannot be tested reliably without the real service available. Mocks solve this: instead of passing the real service, you pass a `MagicMock()`. You configure it to return a fixed value, and the class under test never knows the difference.

**Key terms:**

- **Injected dependency** — a dependency passed in via the constructor (or method argument). This is the simplest kind to mock.
- `MagicMock()` — creates a mock object. Any attribute you access on it returns another `MagicMock` automatically — you never need to declare what methods exist.
- `.return_value` — controls what a mocked method returns when called. The key mental model:
    - `mock.some_method` (no parentheses) — attribute access; gives you the mock object representing that method
    - `mock.some_method()` (with parentheses) — calling the mock; returns `mock.some_method.return_value`
    - `mock.some_method.return_value = 42` — configure this so that any call to `some_method(...)` returns `42`

    This is why there are no parentheses when setting `return_value`: you are configuring the method mock itself, not calling it.

## Test Example 1: A Single Injected Dependency — `WeatherReporter`

Open `src/unit/mocking_basics/weather_reporter.py` and read the class. `WeatherReporter` accepts a `weather_service` in its constructor and calls `weather_service.get_temperature(city)` inside `get_report`.

Because the dependency is injected, you can pass a `MagicMock()` directly in place of the real service.

✋ **Open `test/student/unit/mocking_basics/test_weather_reporter.py`. Write a test that:**

1. Creates a `MagicMock()` for the weather service.
2. Sets `mock.get_temperature.return_value` to a fixed temperature.
3. Passes the mock to `WeatherReporter(mock)`.
4. Calls `get_report("Karlskrona")` and asserts the returned string matches.

<details>
<summary>Hint: basic MagicMock setup</summary>

```python
from unittest.mock import MagicMock
from src.unit.mocking_basics.weather_reporter import WeatherReporter

def test_get_report_formats_string():
    # Arrange
    mock_service = MagicMock()
    mock_service.get_temperature.return_value = 22
    reporter = WeatherReporter(mock_service)
    # Act
    result = reporter.get_report("Karlskrona")
    # Assert
    assert result == "The temperature in Karlskrona is 22°C."
```

</details><br>

✋ **Add a second test that uses a different city and a negative temperature.**

Once you're ready to compare, open the solution: [test/\_solutions/unit/mocking_basics/test_weather_reporter.py](../test/_solutions/unit/mocking_basics/test_weather_reporter.py)

Run `pytest test/student/unit/mocking_basics/test_weather_reporter.py -v` and confirm all tests pass.

## Test Example 2: A Mock Inside a Fixture — `CartPricer`

Open `src/unit/mocking_basics/cart_pricer.py`. `CartPricer` accepts a `price_service` and uses it in `total(item, quantity)`.

You will write three tests, each calling `total()` with different quantities. All three need the same mock with the same `return_value`. Repeating that setup in every test body is tedious — this is exactly the problem `@pytest.fixture` solves.

✋ **Create `test/student/unit/mocking_basics/test_cart_pricer.py`. Write a `@pytest.fixture` that creates a `MagicMock`, sets `mock.get_price.return_value = 5.0`, and returns the mock. Write three tests:**

- `test_total_single_item`: `total("apple", 1)` returns `5.0`
- `test_total_multiple_items`: `total("apple", 3)` returns `15.0`
- `test_total_zero_quantity`: `total("apple", 0)` returns `0.0`

<details>
<summary>Hint: fixture containing a mock</summary>

```python
import pytest
from unittest.mock import MagicMock
from src.unit.mocking_basics.cart_pricer import CartPricer

@pytest.fixture
def price_service():
    mock = MagicMock()
    mock.get_price.return_value = 5.0
    return mock

# The fixture is named price_service for readability, but the name is
# your choice — it only needs to match the test function parameter name,
# not the constructor parameter of CartPricer.

def test_total_single_item(price_service):
    # Arrange
    pricer = CartPricer(price_service)
    # Act
    result = pricer.total("apple", 1)
    # Assert
    assert result == 5.0
```

A mock placed inside a `@pytest.fixture` works the same way as a real object inside a fixture — pytest calls the fixture function again for each test, so each test receives a new `MagicMock` instance with a clean state.

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/unit/mocking_basics/test_cart_pricer.py](../test/_solutions/unit/mocking_basics/test_cart_pricer.py)

Run `pytest test/student/unit/mocking_basics/test_cart_pricer.py -v` and confirm all tests pass.

## Test Example 3: Two Injected Dependencies — `LoanCalculator`

Open `src/unit/mocking_basics/loan_calculator.py`. `LoanCalculator` takes two services — a `rate_service` and a `fee_service` — and uses both in `total_repayment(amount)`.

When a class has more than one dependency, each gets its own `MagicMock`. They are configured independently.

Because each test in this step needs different return values for the rate and fee, a shared fixture would not reduce repetition — it would just move the configuration somewhere harder to read. Create the mocks directly inside each test body instead.

✋ **Create `test/student/unit/mocking_basics/test_loan_calculator.py`. Write three tests, each creating separate mocks for both services with different return values.**

Use this arithmetic to verify your first test: `total_repayment(1000.0)` with `rate=0.1` (10%) and `fee=50.0` should return `1150.0`.

<details>
<summary>Hint: two independent mocks</summary>

```python
from unittest.mock import MagicMock
from src.unit.mocking_basics.loan_calculator import LoanCalculator

def test_total_repayment_includes_interest_and_fee():
    # Arrange
    mock_rate_service = MagicMock()
    mock_rate_service.get_rate.return_value = 0.1
    mock_fee_service = MagicMock()
    mock_fee_service.get_fee.return_value = 50.0
    calculator = LoanCalculator(mock_rate_service, mock_fee_service)
    # Act
    result = calculator.total_repayment(1000.0)
    # Assert
    assert result == 1150.0  # 1000 + 100 interest + 50 fee
```

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/unit/mocking_basics/test_loan_calculator.py](../test/_solutions/unit/mocking_basics/test_loan_calculator.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass.

## Summary

| Source file           | Tests | Concepts practised                                          |
| --------------------- | ----- | ----------------------------------------------------------- |
| `weather_reporter.py` | 2     | `MagicMock()`, injected dependency, `.return_value`         |
| `cart_pricer.py`      | 3     | Mock inside a `@pytest.fixture`, reusing setup across tests |
| `loan_calculator.py`  | 3     | Two independent mocks, one per service                      |

> **Key idea:** A `MagicMock` is a stand-in for any injected dependency. Pass it in the same place you would pass the real thing. Set `.return_value` on the methods your class calls to control what the mock returns. When multiple tests share the same mock configuration, put the mock inside a `@pytest.fixture` rather than repeating the setup in every test body.
