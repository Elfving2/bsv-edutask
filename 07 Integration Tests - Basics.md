# PA1417 — Unit Tests: Mocking Patching

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## When `MagicMock` alone is not enough

In [Mocking Basics](05%20Unit%20Tests%20-%20Mocking%20Basics.md) every dependency was *injected* — you passed a mock straight to the constructor. That works only when the class is designed to receive its dependency from outside.

Open `src/unit/mocking_patching/invoice_mailer.py` and look at line 22:

```python
client = EmailClient()
```

That line is inside the method body. The constructor takes no arguments — there is nowhere to pass in a mock. The class creates its own dependency, so injection is not an option.

The tool for this situation is `patch`. It temporarily replaces a name in a module with a mock for the duration of the test, then restores the original automatically.

## Test Example 1: Patching a Hard-Coded Class — `InvoiceMailer`

✋ **Open `test/student/unit/mocking_patching/test_invoice_mailer.py` and add this test:**

```python
def test_send_invoice_returns_true_on_success():
    # Arrange - TODO
    mailer = InvoiceMailer()
    # Act
    result = mailer.send_invoice("customer@example.com", 499.0)
    # Assert
    assert result is True
```

**Run it and read the output.**

```
pytest test/student/unit/mocking_patching/test_invoice_mailer.py -v
```

The test fails — the real `EmailClient` runs and `send` does not return `True`. The Act and Assert are correct; the problem is the missing Arrange. You have no way to control what `send` returns because `InvoiceMailer` creates its own `EmailClient` internally.

### Introducing `patch`

`patch` solves this. It temporarily replaces a name in a module with a mock for the duration of the test. You use it in the Arrange section, like this:

```python
from unittest.mock import patch

def test_send_invoice_returns_true_on_success():
    # Arrange
    with patch("src.unit.mocking_patching.invoice_mailer.EmailClient") as MockEmailClient:
        mock_client = MockEmailClient.return_value
        mock_client.send.return_value = True
        mailer = InvoiceMailer()
        # Act
        result = mailer.send_invoice("customer@example.com", 499.0)
        # Assert
        assert result is True
```

The `with` block replaces `EmailClient` with a mock for as long as the block runs. `MockEmailClient` is that mock. Now when `send_invoice` calls `EmailClient()`, it calls the mock instead, and `send` returns whatever you told it to.

✋ **Update the test with this Arrange block and run it again. Confirm it passes.**

### What is `.return_value`?

Look at this line in the Arrange:

```python
mock_client = MockEmailClient.return_value
mock_client.send.return_value = True
```

`patch` replaces the *class* `EmailClient` with `MockEmailClient`. Inside `send_invoice`, the source code calls `EmailClient()` to create an instance. When it calls `MockEmailClient()`, the result is `MockEmailClient.return_value` — that is a mock itself, representing the instance the rest of the method uses. You store it in `mock_client`, and then configure `send` on that mock.

In Mocking Basics you set up a mock instance directly. Here there is one extra step: go through `.return_value` to reach the instance the code actually works with.

✋ **Add a second test: `test_send_invoice_returns_false_on_failure`. Configure `send` to return `False` and assert the result is `False`.**

<details>
<summary>Hint</summary>

```python
def test_send_invoice_returns_false_on_failure():
    # Arrange
    with patch("src.unit.mocking_patching.invoice_mailer.EmailClient") as MockEmailClient:
        mock_client = MockEmailClient.return_value
        mock_client.send.return_value = False
        mailer = InvoiceMailer()
        # Act
        result = mailer.send_invoice("customer@example.com", 499.0)
        # Assert
        assert result is False
```

</details><br>

Run the tests again and confirm both pass. Then compare with the solution: [test/\_solutions/unit/mocking_patching/test_invoice_mailer.py](../test/_solutions/unit/mocking_patching/test_invoice_mailer.py)

### The Namespace Rule

Look at the patch string you used:

```
"src.unit.mocking_patching.invoice_mailer.EmailClient"
```

It points to `invoice_mailer`, not to `email_client` where `EmailClient` is defined. Why?

When `invoice_mailer.py` runs `from ... import EmailClient`, Python copies that name into `invoice_mailer`'s own namespace. When `InvoiceMailer` later calls `EmailClient()`, it looks the name up *there* — in its own module. If you patched `email_client.EmailClient` instead, `invoice_mailer` would never see the replacement; it would still find the real class under its own copy of the name.

> **Patch where the name is *used*, not where it is *defined*.**

Keep this in mind for the next two examples.

## Test Example 2: Patching a Non-Deterministic Function — `DiceGame`

Open `src/unit/mocking_patching/dice_game.py`. The `roll` method calls `random.randint(1, 6)`. Because the result is random, a test cannot make a definite assertion — it will sometimes pass and sometimes fail.

By patching `random.randint` inside `dice_game`, you fix the return value and make the test deterministic.

The patch string follows the same rule as before — patch where the name is used. `dice_game.py` does `import random`, so `random` is bound in that module's namespace. The path is:

```
"src.unit.mocking_patching.dice_game.random.randint"
```

✋ **Create `test/student/unit/mocking_patching/test_dice_game.py` and write these three tests:**

- `test_roll_returns_mocked_value` — `roll()` returns the mocked value
- `test_is_winner_when_roll_meets_target` — `is_winner(5)` returns `True` when the roll is `5`
- `test_is_not_winner_when_roll_below_target` — `is_winner(5)` returns `False` when the roll is `2`

<details>
<summary>Hint</summary>

```python
from unittest.mock import patch
from src.unit.mocking_patching.dice_game import DiceGame

def test_roll_returns_mocked_value():
    with patch("src.unit.mocking_patching.dice_game.random.randint") as mock_randint:
        mock_randint.return_value = 4
        game = DiceGame()
        result = game.roll()
        assert result == 4
```

Here you are patching a function, not a class, so there is no extra `.return_value` level — `mock_randint.return_value` is the value `randint(...)` returns directly.

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/unit/mocking_patching/test_dice_game.py](../test/_solutions/unit/mocking_patching/test_dice_game.py)

Run `pytest test/student/unit/mocking_patching/test_dice_game.py -v` and confirm all tests pass.

## Test Example 3: Stacking Multiple Patches — `ShopAssistant`

Open `src/unit/mocking_patching/shop_assistant.py`. It creates both a `StockChecker()` and a `PriceFetcher()` internally — both need to be patched.

You could nest two `with patch(...)` blocks, but `patch` can also be used as a decorator, which is cleaner when patching multiple targets:

```python
@patch("src.unit.mocking_patching.shop_assistant.PriceFetcher")
@patch("src.unit.mocking_patching.shop_assistant.StockChecker")
def test_something(MockStockChecker, MockPriceFetcher):
    ...
```

The decorator replaces the name for the entire test function and passes the mock as an extra parameter. Notice the parameter order: the decorator *closest to the function* (`StockChecker`) fills the *first* parameter. They arrive bottom-up.

✋ **Create `test/student/unit/mocking_patching/test_shop_assistant.py`. Stack two `@patch` decorators and write two tests — one where the item is in stock, one where it is out of stock.**

<details>
<summary>Hint</summary>

```python
from unittest.mock import patch
from src.unit.mocking_patching.shop_assistant import ShopAssistant

@patch("src.unit.mocking_patching.shop_assistant.PriceFetcher")
@patch("src.unit.mocking_patching.shop_assistant.StockChecker")
def test_describe_available_item(MockStockChecker, MockPriceFetcher):
    MockStockChecker.return_value.is_in_stock.return_value = True
    MockPriceFetcher.return_value.get_price.return_value = 199.0

    assistant = ShopAssistant()
    result = assistant.describe("Headphones")

    assert result == "Headphones: available at 199.0 SEK."
```

If your mocks seem to do nothing, check the parameter order — getting it backwards is the most common mistake with stacked decorators.

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/unit/mocking_patching/test_shop_assistant.py](../test/_solutions/unit/mocking_patching/test_shop_assistant.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass.

## Summary

| Source file           | Tests | Concepts practised                                                       |
| --------------------- | ----- | ------------------------------------------------------------------------ |
| `invoice_mailer.py`   | 2     | `patch` context manager, `.return_value`, namespace rule                 |
| `dice_game.py`        | 3     | Patching a module-level function (`random.randint`)                      |
| `shop_assistant.py`   | 2     | Stacked `@patch` decorators, bottom-up parameter order                   |

> **Key idea:** Use `patch` when a class creates its own dependency internally. Patch where the name is *used*, not where it is *defined*. When stacking `@patch` decorators, the one closest to the function fills the first parameter.
