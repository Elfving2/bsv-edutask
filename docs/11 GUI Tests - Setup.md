# PA1417 — Integration Tests: Patching a Hard-Coded Dependency

This tutorial applies `patch` in an integration context. When a component creates its own dependency internally — rather than receiving it via the constructor — you cannot inject a mock. You must patch the name in the module where it is used. The integration between the two real components you are testing stays intact; only the hard-coded external call is replaced.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## Recap: patch vs MagicMock

In [Tutorial 09](09%20Integration%20Tests%20-%20Mocking%20Injected.md) the dependency that needed mocking was *injected* via the constructor — you passed a `MagicMock()` directly. That works only when the class is designed to receive its dependency from outside.

When the class creates its own dependency internally (a hard-coded instantiation inside a method body), the constructor gives you no leverage. `patch` solves this by temporarily replacing the name in the module's namespace for the duration of the test. When the test ends, the original name is restored automatically.

This is the same technique covered in [Tutorial 06 — Unit Tests: Mocking Patching](06%20Unit%20Tests%20-%20Mocking%20Patching.md). The difference here is that we are *not* mocking everything — `CheckoutService` and `CurrencyConverter` both run for real.

## Test Example 1: `CurrencyConverter` and `CheckoutService`

### Step 1: Read the Components

Open [src/integration/patching/exchange_api.py](../src/integration/patching/exchange_api.py). `ExchangeApi` would call a live currency rate service. It raises `NotImplementedError` to make clear it cannot be used in tests.

Open [src/integration/patching/currency_converter.py](../src/integration/patching/currency_converter.py). `CurrencyConverter.convert()` creates an `ExchangeApi()` **internally** — the dependency is hard-coded inside the method body, not injected.

Open [src/integration/patching/checkout_service.py](../src/integration/patching/checkout_service.py). `CheckoutService` accepts a `CurrencyConverter` via its constructor and calls `convert()` to express a SEK total in the customer's preferred currency.

The chain is: `CheckoutService` (A) → `CurrencyConverter` (B) → `ExchangeApi` (C, hard-coded).

### Step 2: Apply the Namespace Rule

`CurrencyConverter` imports `ExchangeApi` with `from src.integration.patching.exchange_api import ExchangeApi`. Once that import runs, the name `ExchangeApi` lives in `CurrencyConverter`'s own namespace (`src.integration.patching.currency_converter`).

> **Patch where the name is *used*, not where it is *defined*.**

Patch `src.integration.patching.currency_converter.ExchangeApi` — not `src.integration.patching.exchange_api.ExchangeApi`. Patching the definition site is too late; the consumer module already holds its own reference to the name.

### Step 3: Write the Integration Tests

Open the stub at `test/student/integration/patching/test_checkout_service_integration.py`.

✋ **Write at least three tests. Patch `ExchangeApi` in `currency_converter`'s namespace, then create real `CurrencyConverter` and `CheckoutService` instances inside the patch context.**

<details>
<summary>Hint: test structure</summary>

```python
from unittest.mock import patch
from src.integration.patching.currency_converter import CurrencyConverter
from src.integration.patching.checkout_service import CheckoutService

def test_total_in_eur_applies_correct_rate():
    with patch("src.integration.patching.currency_converter.ExchangeApi") as MockApi:
        mock_api = MockApi.return_value
        mock_api.get_rate.return_value = 0.087   # 1 SEK = 0.087 EUR
        converter = CurrencyConverter()           # real
        service = CheckoutService(converter)      # real
        # Act
        result = service.total_in(1000.0, "EUR")
        # Assert
        assert result == 87.0
```

`MockApi` is the patched *class*. `MockApi.return_value` is the instance that `CurrencyConverter` will receive when it calls `ExchangeApi()` internally — this is the object whose `get_rate` method you control.

</details><br>

Suggested test cases:

- Converting SEK to EUR with a realistic rate (e.g. 0.087)
- Converting SEK to USD with a different rate
- A rate of 1.0 (same currency, amount should be unchanged)

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/patching/test_checkout_service_integration.py](../test/_solutions/integration/patching/test_checkout_service_integration.py)

## Test Example 2: `WeatherFormatter` and `WeatherDashboard`

Open [src/integration/patching/weather_api.py](../src/integration/patching/weather_api.py). `WeatherApi` would call a live weather service. It raises `NotImplementedError` when called directly.

Open [src/integration/patching/weather_formatter.py](../src/integration/patching/weather_formatter.py). `WeatherFormatter.format` creates a `WeatherApi()` **internally** — the dependency is hard-coded inside the method body. It returns a string like `"Karlskrona: sunny, 22°C"`.

Open [src/integration/patching/weather_dashboard.py](../src/integration/patching/weather_dashboard.py). `WeatherDashboard` accepts a `WeatherFormatter` in its constructor and wraps the output in a `"Weather report — ..."` string.

The chain is: `WeatherDashboard` (A) → `WeatherFormatter` (B) → `WeatherApi` (C, hard-coded).

The namespace rule applies as before: `WeatherFormatter` imports `WeatherApi` with `from src.integration.patching.weather_api import WeatherApi`, so the name lives in `src.integration.patching.weather_formatter`. Patch `src.integration.patching.weather_formatter.WeatherApi`.

✋ **Create `test/student/integration/patching/test_weather_dashboard_integration.py`. Write three tests — one per weather condition (sunny, rainy, snowy). Patch `WeatherApi` in the formatter's namespace and keep `WeatherFormatter` and `WeatherDashboard` real.**

<details>
<summary>Hint: test structure</summary>

```python
from unittest.mock import patch
from src.integration.patching.weather_formatter import WeatherFormatter
from src.integration.patching.weather_dashboard import WeatherDashboard

def test_sunny_weather_report():
    with patch("src.integration.patching.weather_formatter.WeatherApi") as MockApi:
        mock_api = MockApi.return_value
        mock_api.get_conditions.return_value = {"temp_c": 24, "condition": "sunny"}
        formatter = WeatherFormatter()
        dashboard = WeatherDashboard(formatter)
        assert dashboard.display("Karlskrona") == "Weather report — Karlskrona: sunny, 24°C"
```

</details><br>

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/patching/test_weather_dashboard_integration.py](../test/_solutions/integration/patching/test_weather_dashboard_integration.py)

## Test Example 3: Two Hard-Coded Dependencies — `StoreInventory` and `ProductCatalog`

Open [src/integration/patching/price_api.py](../src/integration/patching/price_api.py) and [src/integration/patching/stock_api.py](../src/integration/patching/stock_api.py). Both raise `NotImplementedError` when called directly.

Open [src/integration/patching/store_inventory.py](../src/integration/patching/store_inventory.py). `StoreInventory.lookup` creates **both** `PriceApi()` and `StockApi()` internally. Both are hard-coded — neither is injected. Both must be patched.

Open [src/integration/patching/product_catalog.py](../src/integration/patching/product_catalog.py). `ProductCatalog` accepts a `StoreInventory` in its constructor and formats a product description string.

The chain is: `ProductCatalog` (A) → `StoreInventory` (B) → `PriceApi` + `StockApi` (C1 and C2, both hard-coded).

Because B hard-codes **two** external dependencies, the test must apply **two** `patch` calls simultaneously. Use a `with` statement with two patches at once:

```python
with patch("src.integration.patching.store_inventory.PriceApi") as MockPriceApi, \
     patch("src.integration.patching.store_inventory.StockApi") as MockStockApi:
```

Both names live in `src.integration.patching.store_inventory` — apply the namespace rule to each.

✋ **Create `test/student/integration/patching/test_product_catalog_integration.py`. Write three tests: an item in stock at a normal price, an item out of stock, and an expensive item in stock. Patch both APIs in `store_inventory`'s namespace.**

<details>
<summary>Hint: test structure</summary>

```python
from unittest.mock import patch
from src.integration.patching.store_inventory import StoreInventory
from src.integration.patching.product_catalog import ProductCatalog

def test_item_in_stock_at_normal_price():
    with patch("src.integration.patching.store_inventory.PriceApi") as MockPriceApi, \
         patch("src.integration.patching.store_inventory.StockApi") as MockStockApi:
        MockPriceApi.return_value.get_price.return_value = 49.99
        MockStockApi.return_value.in_stock.return_value = True
        inventory = StoreInventory()
        catalog = ProductCatalog(inventory)
        assert catalog.describe("SKU-001") == "SKU-001: 49.99 SEK, in stock"
```

`MockPriceApi.return_value` is the instance `StoreInventory` receives when it calls `PriceApi()` internally. The same pattern applies to `MockStockApi`.

</details><br>

✋ **Why is a `with` statement with two patches preferable to two separate `with` blocks here?**

<details>
<summary>Answer</summary>

Two *sequential* `with` blocks would each be active only within their own scope — you cannot have both patches active at the same time. Two *nested* `with` blocks would work, but add an extra level of indentation for no benefit. A single `with` statement with a comma is the idiomatic approach: both patches are active for exactly the same block of code, and it reads more cleanly.

</details><br>

Run `pytest test/student/integration/ -v` and confirm all tests pass.

Once you are ready to compare, open the solution: [test/\_solutions/integration/patching/test_product_catalog_integration.py](../test/_solutions/integration/patching/test_product_catalog_integration.py)

## Summary

| Source files | Tests | Concepts practised |
| --- | --- | --- |
| `currency_converter.py`, `checkout_service.py` | 3 | Integration test with `patch`, namespace rule, hard-coded dependency |
| `weather_formatter.py`, `weather_dashboard.py` | 3 | Second patching chain, different domain |
| `store_inventory.py`, `product_catalog.py` | 3 | Two hard-coded dependencies, two patches in one `with` statement |

> **Key idea:** `patch` in an integration test targets only the hard-coded external call. The components you are integrating still run with their real logic. When a component hard-codes two dependencies, patch both in the same `with` statement to ensure both replacements are active simultaneously. Apply the namespace rule to each patch independently.
