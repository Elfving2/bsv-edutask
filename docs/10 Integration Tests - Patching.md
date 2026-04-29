# PA1417 — Integration Tests: Mocking an Injected Dependency

This tutorial shows how to write an integration test when one dependency in the chain would require a live external connection. You will keep two real components running together and mock only the one that is genuinely out of scope.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## The spectrum from unit to end-to-end

Mocking is not only a unit test technique. It exists on a spectrum:

| Test type | What runs real | What is mocked |
| --- | --- | --- |
| Unit test | One class | All its dependencies |
| Integration test | Two or more classes | External dependencies only |
| End-to-end test | The entire system | Nothing (or near nothing) |

The tests in this tutorial sit in the middle: two classes run with real logic, and one external dependency is mocked because it would require a live network connection.

## Test Example 1: `DiscountEngine` and `OrderPricer`

### Step 1: Read the Components

Open [src/integration/mocking_injected/loyalty_service.py](../src/integration/mocking_injected/loyalty_service.py). `LoyaltyService` would call a remote system to fetch a customer's loyalty points. In tests, calling it for real is not an option.

Open [src/integration/mocking_injected/discount_engine.py](../src/integration/mocking_injected/discount_engine.py). `DiscountEngine` accepts a `LoyaltyService` via its constructor and uses it to decide whether a customer earns a discount (10 % off when they have 100 or more points).

Open [src/integration/mocking_injected/order_pricer.py](../src/integration/mocking_injected/order_pricer.py). `OrderPricer` accepts a `DiscountEngine` via its constructor and uses it to compute the final price.

The chain is: `OrderPricer` → `DiscountEngine` → `LoyaltyService`.

### Step 2: Identify What to Mock

You want to test that `OrderPricer` and `DiscountEngine` work correctly together. `LoyaltyService` is the only thing you cannot use for real — it requires a live connection.

Mock `LoyaltyService`. Keep `DiscountEngine` and `OrderPricer` real.

✋ **Before writing any code, think through this question:**

> What happens if you mock `DiscountEngine` entirely — passing a `MagicMock()` to `OrderPricer` instead of a real `DiscountEngine`?

<details>
<summary>Answer</summary>

If you replace the real `DiscountEngine` with a `MagicMock()`, you are no longer testing the collaboration between `OrderPricer` and `DiscountEngine`. The mock just returns whatever you tell it to return — it exercises none of `DiscountEngine`'s real logic (the threshold, the rate, the subtraction).

That is a **unit test of `OrderPricer`**, not an integration test. The moment `DiscountEngine` becomes a mock, the integration between A and B disappears.

</details><br>

### Step 3: Write the Integration Tests

Open the stub at `test/student/integration/mocking_injected/test_order_pricer_integration.py`.

✋ **Write at least three tests. Inject a `MagicMock` for `LoyaltyService`, create real `DiscountEngine` and `OrderPricer` instances, and assert the final price.**

> **`MagicMock(spec=LoyaltyService)`:** Passing `spec=` enforces the real class's interface on the mock. If your code accidentally calls a method that does not exist on `LoyaltyService` — for example, a typo like `get_point` instead of `get_points` — the mock raises `AttributeError` immediately. Without `spec=`, a plain `MagicMock()` silently accepts any attribute name and returns another `MagicMock`, hiding the mistake. Use `spec=` whenever you know which class you are replacing.

<details>
<summary>Hint: test structure</summary>

```python
from unittest.mock import MagicMock
from src.integration.mocking_injected.loyalty_service import LoyaltyService
from src.integration.mocking_injected.discount_engine import DiscountEngine
from src.integration.mocking_injected.order_pricer import OrderPricer

def test_loyal_customer_receives_discount():
    # Arrange
    mock_loyalty = MagicMock(spec=LoyaltyService)
    mock_loyalty.get_points.return_value = 150   # above threshold
    engine = DiscountEngine(mock_loyalty)         # real
    pricer = OrderPricer(engine)                  # real
    # Act
    result = pricer.price("cust-1", 200.0)
    # Assert: 10 % off 200 = 20 discount → 180 final
    assert result == 180.0
```

</details><br>

Suggested test cases:

- A customer with points above the threshold (100) — should receive a 10 % discount
- A customer with points below the threshold — should pay the full price
- A customer with exactly 100 points — threshold is inclusive, so they should receive the discount

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/mocking_injected/test_order_pricer_integration.py](../test/_solutions/integration/mocking_injected/test_order_pricer_integration.py)

## Test Example 2: `ReviewAnalyzer` and `RatingEngine`

Open [src/integration/mocking_injected/sentiment_api.py](../src/integration/mocking_injected/sentiment_api.py). `SentimentApi` would call a remote service to score the sentiment of text, returning a float from −1.0 (most negative) to +1.0 (most positive). It raises `NotImplementedError` when called directly.

Open [src/integration/mocking_injected/review_analyzer.py](../src/integration/mocking_injected/review_analyzer.py). `ReviewAnalyzer` accepts a `SentimentApi` in its constructor and classifies text as `"positive"`, `"neutral"`, or `"negative"`.

Open [src/integration/mocking_injected/rating_engine.py](../src/integration/mocking_injected/rating_engine.py). `RatingEngine` accepts a `ReviewAnalyzer` in its constructor and maps the classification to a 1–5 star rating.

The chain is: `RatingEngine` → `ReviewAnalyzer` → `SentimentApi`.

✋ **Create `test/student/integration/mocking_injected/test_rating_engine_integration.py`. Write three tests — one per sentiment outcome. Mock only `SentimentApi`; keep `ReviewAnalyzer` and `RatingEngine` real.**

<details>
<summary>Hint: test structure</summary>

```python
from unittest.mock import MagicMock
from src.integration.mocking_injected.sentiment_api import SentimentApi
from src.integration.mocking_injected.review_analyzer import ReviewAnalyzer
from src.integration.mocking_injected.rating_engine import RatingEngine

def test_positive_review_gets_five_stars():
    mock_api = MagicMock(spec=SentimentApi)
    mock_api.analyze.return_value = 0.8
    analyzer = ReviewAnalyzer(mock_api)     # real
    engine = RatingEngine(analyzer)          # real
    assert engine.star_rating("Great!") == 5
```

</details><br>

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/mocking_injected/test_rating_engine_integration.py](../test/_solutions/integration/mocking_injected/test_rating_engine_integration.py)

## Test Example 3: A Component With Two Real Methods — `FraudDetector` and `PaymentProcessor`

Open [src/integration/mocking_injected/risk_database.py](../src/integration/mocking_injected/risk_database.py). `RiskDatabase` would query a remote fraud-risk service, returning an integer score from 0 to 100. It raises `NotImplementedError` when called directly.

Open [src/integration/mocking_injected/fraud_detector.py](../src/integration/mocking_injected/fraud_detector.py). `FraudDetector` accepts a `RiskDatabase` in its constructor and exposes **two** methods: `is_blocked` (score > 90) and `is_flagged` (score > 70).

Open [src/integration/mocking_injected/payment_processor.py](../src/integration/mocking_injected/payment_processor.py). `PaymentProcessor` accepts a `FraudDetector` in its constructor and calls *both* `is_blocked` and `is_flagged` inside `process`. The outcome is `"blocked"`, `"flagged"`, or `"approved: <amount> SEK"`.

The chain is: `PaymentProcessor` → `FraudDetector` → `RiskDatabase`.

This example is more demanding than Example 2 because `FraudDetector` has two real methods and `PaymentProcessor` exercises both of them. A unit test of `PaymentProcessor` would mock `FraudDetector` entirely and never run its threshold logic — the integration test is the only test that exercises the interaction between both methods and the real processor.

✋ **Create `test/student/integration/mocking_injected/test_payment_processor_integration.py`. Write four tests: a blocked customer (score > 90), a flagged customer (score 71–90), an approved customer (score ≤ 70), and the boundary case where score is exactly 70 (not flagged). Mock only `RiskDatabase`.**

<details>
<summary>Hint: test structure</summary>

```python
from unittest.mock import MagicMock
from src.integration.mocking_injected.risk_database import RiskDatabase
from src.integration.mocking_injected.fraud_detector import FraudDetector
from src.integration.mocking_injected.payment_processor import PaymentProcessor

def test_high_risk_customer_is_blocked():
    mock_db = MagicMock(spec=RiskDatabase)
    mock_db.get_score.return_value = 95
    detector = FraudDetector(mock_db)       # real — both methods run
    processor = PaymentProcessor(detector)   # real
    assert processor.process("cust-1", 500.0) == "blocked"
```

</details><br>

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/mocking_injected/test_payment_processor_integration.py](../test/_solutions/integration/mocking_injected/test_payment_processor_integration.py)

## Summary

| Source files | Tests | Concepts practised |
| --- | --- | --- |
| `discount_engine.py`, `order_pricer.py` | 3 | Integration test with one injected mock, `MagicMock(spec=...)` |
| `review_analyzer.py`, `rating_engine.py` | 3 | Second injected-mock chain, different domain |
| `fraud_detector.py`, `payment_processor.py` | 4 | B exposes two real methods; integration exercises both |

> **Key idea:** In an integration test, mock only what is genuinely external — the dependency that would break the test by requiring a live connection or a non-deterministic result. Keep every other component real. The more you mock, the closer you move towards a unit test; the less you mock, the closer you move towards an end-to-end test.
