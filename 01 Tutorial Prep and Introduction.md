# Tutorial Design

## Document Structure

Students complete tutorials in the following order. After the prep and introduction, each tutorial focuses on a single concept, but the recommended order reflects genuine dependencies: mocking Basics assumes fixtures knowledge, and integration tutorials build on unit test skills.

| File                                                                                            | Purpose                                                                          |
| ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [01 Tutorial Prep and Introduction](01%20Tutorial%20Prep%20and%20Introduction.md)               | Environment setup and repository orientation; complete before any topic tutorial |
| [02 Unit Tests - Assert](02%20Unit%20Tests%20-%20Assert.md)                                     | `assert`, AAA pattern, equivalence partitioning                                  |
| [03 Unit Tests - Fixtures](03%20Unit%20Tests%20-%20Fixtures.md)                                 | `@pytest.fixture`, shared setup                                                  |
| [04 Unit Tests - Parameterization](04%20Unit%20Tests%20-%20Parameterization.md)                 | `@pytest.mark.parametrize`                                                       |
| [05 Unit Tests - Mocking Basics](05%20Unit%20Tests%20-%20Mocking%20Basics.md)                   | `MagicMock`, injected dependencies, `.return_value`, mock fixture                |
| [06 Unit Tests - Mocking Patching](06%20Unit%20Tests%20-%20Mocking%20Patching.md)               | `patch`, namespace rule, impure functions, stacked decorators                    |
| [07 Integration Tests - Basics](07%20Integration%20Tests%20-%20Basics.md)                       | Two real components tested together; no mocking, no fixtures                     |
| [08 Integration Tests - Fixtures](08%20Integration%20Tests%20-%20Fixtures.md)                   | Fixture teardown with `yield`, filesystem side effects                           |
| [09 Integration Tests - Mocking Injected](09%20Integration%20Tests%20-%20Mocking%20Injected.md) | `MagicMock(spec=...)`, selective mocking, A→B→C chain                            |
| [10 Integration Tests - Patching](10%20Integration%20Tests%20-%20Patching.md)                   | `patch` in integration tests; hard-coded external dependency, namespace rule     |
| [11 GUI Tests - Setup](11%20GUI%20Tests%20-%20Setup.md)                                         | Cypress setup, `cy.visit`, `cy.get`, `should` assertions, `not.be.visible`       |
| [12 GUI Tests - Selectors](12%20GUI%20Tests%20-%20Selectors.md)                                 | Imperative (`cy.get`), declarative (`cy.contains`), chained (`.find`) selectors  |
| [13 GUI Tests - Interactions](13%20GUI%20Tests%20-%20Interactions.md)                           | `.type`, `.click`, `click({ force: true })`, `not.exist` vs `not.be.visible`     |
| [14 GUI Tests - beforeEach](14%20GUI%20Tests%20-%20beforeEach.md)                               | Shared setup hook; eliminating repeated `cy.visit`; pre-populated state          |

## Tutorial Structure

Each concept tutorial has three matching locations in the repository:

**`src/<unit|integration>/<concept>/`** — the source files students will write tests against. All source code is provided; students do not modify these files.

**`test/student/<unit|integration|gui>/<concept>/`** — where students write their tests. One stub file is provided for the first (simplest) example in the tutorial, so students have the correct import and a `# TODO` to start from. Students create the remaining test files themselves, following the same naming and import conventions as the stub.

**`test/_solutions/<unit|integration|gui>/<concept>/`** — complete reference solutions for every example in the tutorial. These are there if you get stuck or want to check your work after completing an exercise. Try not to look at them until you have made a genuine attempt.

The reason only one stub is provided per tutorial (rather than one per example) is intentional: creating a test file from scratch — choosing the file name, writing the import, and deciding on the test function names — is itself part of the skill being practised. The stub for the first example removes that friction while you are still getting oriented, then hands the scaffolding responsibility to you for the rest.

> **Exception — GUI Tests: Setup (Tutorial 11):** All three examples in this tutorial have pre-existing stubs. Tutorial 11 is the first JavaScript-based tutorial and introduces a completely new language and framework, so the extra scaffolding is provided throughout the whole tutorial to keep the focus on learning Cypress rather than on file and import boilerplate.

## Tutorial Concepts

### Unit Tests: Assert

Concept: `assert`

The "assert" keyword raises a special exception if a condition is not met and prints information in the test log.

Students derive test cases using equivalence partitioning, write tests following the AAA pattern, and run pytest to verify coverage.

Matching Source Files

- [src/unit/asserts/sign.py](../src/unit/asserts/sign.py) — 3 equivalence partitions (negative, zero, positive)
- [src/unit/asserts/fizzbuzz.py](../src/unit/asserts/fizzbuzz.py) — 4 equivalence partitions (FizzBuzz, Fizz, Buzz, neither)
- [src/unit/asserts/age_classifier.py](../src/unit/asserts/age_classifier.py) — 5 valid partitions + 1 invalid (raises ValueError)

Test Stub - Student Starting Point

- [test/student/unit/asserts/test_sign.py](../test/student/unit/asserts/test_sign.py)

Matching Solution Tests

- [test/\_solutions/unit/asserts/test_sign.py](../test/_solutions/unit/asserts/test_sign.py)
- [test/\_solutions/unit/asserts/test_fizzbuzz.py](../test/_solutions/unit/asserts/test_fizzbuzz.py)
- [test/\_solutions/unit/asserts/test_age_classifier.py](../test/_solutions/unit/asserts/test_age_classifier.py)

---

### Unit Tests: Fixtures

Concept: `@pytest.fixture`

Sometimes tests need to be set up — think of preparing a specific object state before each test. Additionally, you sometimes need to do things after the tests have run, such as clean up state for the next test. For pure in-memory objects this means resetting the object; for integration tests it means deleting files, resetting databases, etc.

This tutorial covers the unit test side: fixtures that use `return` because there is nothing to clean up.

Matching Source Files

- [src/unit/fixtures/playlist.py](../src/unit/fixtures/playlist.py) — in-memory class; fixture uses `return` (nothing to clean up)
- [src/unit/fixtures/stack.py](../src/unit/fixtures/stack.py) — in-memory class; one test requires inline setup rather than the fixture
- [src/unit/fixtures/shopping_cart.py](../src/unit/fixtures/shopping_cart.py) — in-memory class; two fixtures for different starting states (`empty_cart` and `stocked_cart`)

Test Stub - Student Starting Point

- [test/student/unit/fixtures/test_playlist.py](../test/student/unit/fixtures/test_playlist.py)

Matching Solution Tests

- [test/\_solutions/unit/fixtures/test_playlist.py](../test/_solutions/unit/fixtures/test_playlist.py)
- [test/\_solutions/unit/fixtures/test_stack.py](../test/_solutions/unit/fixtures/test_stack.py)
- [test/\_solutions/unit/fixtures/test_shopping_cart.py](../test/_solutions/unit/fixtures/test_shopping_cart.py)

---

### Unit Tests: Parameterization

Concept: `@pytest.mark.parametrize`

Parametrisation allows us to reuse the same test implementation with different parameters.

Matching Source Files

- [src/unit/parameterization/day_type.py](../src/unit/parameterization/day_type.py) — 7 bounded inputs (day names); makes repetition without parametrize obvious
- [src/unit/parameterization/palindrome.py](../src/unit/parameterization/palindrome.py) — infinite input domain; demonstrates choosing a representative sample
- [src/unit/parameterization/triangle_type.py](../src/unit/parameterization/triangle_type.py) — 3 input parameters; demonstrates multi-argument tuples and `pytest.param` IDs for readable test names

Test Stub - Student Starting Point

- [test/student/unit/parameterization/test_day_type.py](../test/student/unit/parameterization/test_day_type.py)

Matching Solution Tests

- [test/\_solutions/unit/parameterization/test_day_type.py](../test/_solutions/unit/parameterization/test_day_type.py)
- [test/\_solutions/unit/parameterization/test_palindrome.py](../test/_solutions/unit/parameterization/test_palindrome.py)
- [test/\_solutions/unit/parameterization/test_triangle_type.py](../test/_solutions/unit/parameterization/test_triangle_type.py)

---

### Unit Tests: Mocking Basics

Concept: `MagicMock`, injected dependencies, `.return_value`

When a class receives its dependencies via the constructor, you can test it in isolation by passing a `MagicMock()` instead of the real dependency. Setting `.return_value` on a mock method gives the test full control over what the class sees when it calls that method. When multiple tests share the same mock configuration, the mock belongs inside a `@pytest.fixture`.

Matching Source Files

- [src/unit/mocking_basics/weather_reporter.py](../src/unit/mocking_basics/weather_reporter.py) — single injected service; demonstrates bare `MagicMock` and `.return_value`
- [src/unit/mocking_basics/cart_pricer.py](../src/unit/mocking_basics/cart_pricer.py) — single injected service; multiple tests sharing a mock fixture
- [src/unit/mocking_basics/loan_calculator.py](../src/unit/mocking_basics/loan_calculator.py) — two injected services; one independent mock per dependency

Test Stub - Student Starting Point

- [test/student/unit/mocking_basics/test_weather_reporter.py](../test/student/unit/mocking_basics/test_weather_reporter.py)

Matching Solution Tests

- [test/\_solutions/unit/mocking_basics/test_weather_reporter.py](../test/_solutions/unit/mocking_basics/test_weather_reporter.py)
- [test/\_solutions/unit/mocking_basics/test_cart_pricer.py](../test/_solutions/unit/mocking_basics/test_cart_pricer.py)
- [test/\_solutions/unit/mocking_basics/test_loan_calculator.py](../test/_solutions/unit/mocking_basics/test_loan_calculator.py)

---

### Unit Tests: Mocking Patching

Concept: `patch`, namespace rule, non-deterministic functions, stacked decorators

When a class creates its own dependency internally (hard-coded), `MagicMock` alone cannot reach it — you must use `patch` to replace the name in the module where it is used. Key rules: always patch at the consumer namespace, not the definition site; when stacking `@patch` decorators, parameters arrive bottom-up (innermost decorator → first parameter).

Matching Source Files

- [src/unit/mocking_patching/email_client.py](../src/unit/mocking_patching/email_client.py) — the hard-coded dependency used by `InvoiceMailer`
- [src/unit/mocking_patching/invoice_mailer.py](../src/unit/mocking_patching/invoice_mailer.py) — creates `EmailClient()` internally; demonstrates `patch` context manager and namespace rule
- [src/unit/mocking_patching/dice_game.py](../src/unit/mocking_patching/dice_game.py) — calls `random.randint`; demonstrates patching a non-deterministic function
- [src/unit/mocking_patching/stock_checker.py](../src/unit/mocking_patching/stock_checker.py) — hard-coded dependency used by `ShopAssistant`
- [src/unit/mocking_patching/price_fetcher.py](../src/unit/mocking_patching/price_fetcher.py) — hard-coded dependency used by `ShopAssistant`
- [src/unit/mocking_patching/shop_assistant.py](../src/unit/mocking_patching/shop_assistant.py) — creates two dependencies internally; demonstrates stacked `@patch` decorators

Test Stub - Student Starting Point

- [test/student/unit/mocking_patching/test_invoice_mailer.py](../test/student/unit/mocking_patching/test_invoice_mailer.py)

Matching Solution Tests

- [test/\_solutions/unit/mocking_patching/test_invoice_mailer.py](../test/_solutions/unit/mocking_patching/test_invoice_mailer.py)
- [test/\_solutions/unit/mocking_patching/test_dice_game.py](../test/_solutions/unit/mocking_patching/test_dice_game.py)
- [test/\_solutions/unit/mocking_patching/test_shop_assistant.py](../test/_solutions/unit/mocking_patching/test_shop_assistant.py)

---

### Integration Tests: Basics

Concept: integration testing without mocking or external resources

The simplest integration test: two classes in separate source files, both running for real. No mocking, no fixtures, no side effects. The test verifies that the two components collaborate correctly — if either had a bug in isolation or a mismatched interface, this test would catch it.

Matching Source Files

- [src/integration/basics/tip_calculator.py](../src/integration/basics/tip_calculator.py) — computes tip amount; used as the real dependency in BillSplitter
- [src/integration/basics/bill_splitter.py](../src/integration/basics/bill_splitter.py) — accepts injected TipCalculator; splits bill+tip among N people
- [src/integration/basics/score_normalizer.py](../src/integration/basics/score_normalizer.py) — converts a raw score to a percentage; used as the real dependency in GradeAssigner
- [src/integration/basics/grade_assigner.py](../src/integration/basics/grade_assigner.py) — accepts injected ScoreNormalizer; maps percentage to letter grade
- [src/integration/basics/price_formatter.py](../src/integration/basics/price_formatter.py) — formats a monetary amount as a string; used as the real dependency in ReceiptPrinter
- [src/integration/basics/receipt_printer.py](../src/integration/basics/receipt_printer.py) — accepts injected PriceFormatter; calls format for every item in the list

Test Stub - Student Starting Point

- [test/student/integration/basics/test_bill_splitter_integration.py](../test/student/integration/basics/test_bill_splitter_integration.py)

Matching Solution Tests

- [test/\_solutions/integration/basics/test_bill_splitter_integration.py](../test/_solutions/integration/basics/test_bill_splitter_integration.py)
- [test/\_solutions/integration/basics/test_grade_assigner_integration.py](../test/_solutions/integration/basics/test_grade_assigner_integration.py)
- [test/\_solutions/integration/basics/test_receipt_printer_integration.py](../test/_solutions/integration/basics/test_receipt_printer_integration.py)

---

### Integration Tests: Fixtures

Concept: `@pytest.fixture` with `yield` teardown

Integration tests interact with real external resources (filesystem, database, network). Fixtures must clean up those resources after each test so that tests do not affect one another. The `yield` keyword in a fixture separates setup (before `yield`) from teardown (after `yield`), and pytest guarantees the teardown runs even when a test fails.

This tutorial covers the integration test side, contrasting it with the plain-function approach from the unit test fixture tutorial to show why teardown is necessary.

Matching Source Files

- [src/integration/fixtures/note_writer.py](../src/integration/fixtures/note_writer.py) — writes to a real file on disk; fixture must delete the file after each test
- [src/integration/fixtures/csv_logger.py](../src/integration/fixtures/csv_logger.py) — appends rows to a CSV file; append mode makes isolation failure more visible
- [src/integration/fixtures/file_cache.py](../src/integration/fixtures/file_cache.py) — stores key-value pairs as individual files in a directory; teardown uses `shutil.rmtree`

Test Stub - Student Starting Point

- [test/student/integration/fixtures/test_note_writer_integration.py](../test/student/integration/fixtures/test_note_writer_integration.py)

Matching Solution Tests

- [test/\_solutions/integration/fixtures/test_note_writer_integration.py](../test/_solutions/integration/fixtures/test_note_writer_integration.py)
- [test/\_solutions/integration/fixtures/test_csv_logger_integration.py](../test/_solutions/integration/fixtures/test_csv_logger_integration.py)
- [test/\_solutions/integration/fixtures/test_file_cache_integration.py](../test/_solutions/integration/fixtures/test_file_cache_integration.py)

---

### Integration Tests: Mocking Injected

Concept: selective mocking in integration tests; `MagicMock(spec=...)`

Two components (A and B) run with real logic. B has an injected dependency C that would require a live external connection — only C is mocked. This illustrates the spectrum from unit test (everything mocked) to end-to-end test (nothing mocked), and specifically why replacing B with a mock would collapse this back into a unit test of A.

Matching Source Files

- [src/integration/mocking_injected/loyalty_service.py](../src/integration/mocking_injected/loyalty_service.py) — C: external loyalty points API; mocked in integration tests
- [src/integration/mocking_injected/discount_engine.py](../src/integration/mocking_injected/discount_engine.py) — B: injected LoyaltyService; applies discount based on points threshold
- [src/integration/mocking_injected/order_pricer.py](../src/integration/mocking_injected/order_pricer.py) — A: injected DiscountEngine; computes final order price
- [src/integration/mocking_injected/sentiment_api.py](../src/integration/mocking_injected/sentiment_api.py) — C: external sentiment scoring API; mocked in integration tests
- [src/integration/mocking_injected/review_analyzer.py](../src/integration/mocking_injected/review_analyzer.py) — B: injected SentimentApi; classifies text as positive/neutral/negative
- [src/integration/mocking_injected/rating_engine.py](../src/integration/mocking_injected/rating_engine.py) — A: injected ReviewAnalyzer; maps classification to 1–5 star rating
- [src/integration/mocking_injected/risk_database.py](../src/integration/mocking_injected/risk_database.py) — C: external fraud risk scoring service; mocked in integration tests
- [src/integration/mocking_injected/fraud_detector.py](../src/integration/mocking_injected/fraud_detector.py) — B: injected RiskDatabase; exposes two real methods (`is_blocked`, `is_flagged`)
- [src/integration/mocking_injected/payment_processor.py](../src/integration/mocking_injected/payment_processor.py) — A: injected FraudDetector; returns blocked/flagged/approved outcome

Test Stub - Student Starting Point

- [test/student/integration/mocking_injected/test_order_pricer_integration.py](../test/student/integration/mocking_injected/test_order_pricer_integration.py)

Matching Solution Tests

- [test/\_solutions/integration/mocking_injected/test_order_pricer_integration.py](../test/_solutions/integration/mocking_injected/test_order_pricer_integration.py)
- [test/\_solutions/integration/mocking_injected/test_rating_engine_integration.py](../test/_solutions/integration/mocking_injected/test_rating_engine_integration.py)
- [test/\_solutions/integration/mocking_injected/test_payment_processor_integration.py](../test/_solutions/integration/mocking_injected/test_payment_processor_integration.py)

---

### Integration Tests: Patching

Concept: `patch` in integration tests; namespace rule; hard-coded external dependency

Same `patch` mechanics as Unit Tests — Mocking Patching, but applied at the integration level. Two components (A and B) run for real; B creates its dependency C internally (hard-coded). C is patched in B's namespace, removing the external call while leaving the A→B integration intact.

Matching Source Files

- [src/integration/patching/exchange_api.py](../src/integration/patching/exchange_api.py) — C: live currency rate API; hard-coded inside CurrencyConverter
- [src/integration/patching/currency_converter.py](../src/integration/patching/currency_converter.py) — B: hard-codes ExchangeApi; converts amounts between currencies
- [src/integration/patching/checkout_service.py](../src/integration/patching/checkout_service.py) — A: injected CurrencyConverter; expresses SEK totals in target currency
- [src/integration/patching/weather_api.py](../src/integration/patching/weather_api.py) — C: live weather data API; hard-coded inside WeatherFormatter
- [src/integration/patching/weather_formatter.py](../src/integration/patching/weather_formatter.py) — B: hard-codes WeatherApi; formats city weather as a string
- [src/integration/patching/weather_dashboard.py](../src/integration/patching/weather_dashboard.py) — A: injected WeatherFormatter; displays formatted weather report
- [src/integration/patching/price_api.py](../src/integration/patching/price_api.py) — C1: live pricing service; hard-coded inside StoreInventory
- [src/integration/patching/stock_api.py](../src/integration/patching/stock_api.py) — C2: live stock service; hard-coded inside StoreInventory
- [src/integration/patching/store_inventory.py](../src/integration/patching/store_inventory.py) — B: hard-codes both PriceApi and StockApi; requires two stacked `@patch` decorators
- [src/integration/patching/product_catalog.py](../src/integration/patching/product_catalog.py) — A: injected StoreInventory; describes a product with price and availability

Test Stub - Student Starting Point

- [test/student/integration/patching/test_checkout_service_integration.py](../test/student/integration/patching/test_checkout_service_integration.py)

Matching Solution Tests

- [test/\_solutions/integration/patching/test_checkout_service_integration.py](../test/_solutions/integration/patching/test_checkout_service_integration.py)
- [test/\_solutions/integration/patching/test_weather_dashboard_integration.py](../test/_solutions/integration/patching/test_weather_dashboard_integration.py)
- [test/\_solutions/integration/patching/test_product_catalog_integration.py](../test/_solutions/integration/patching/test_product_catalog_integration.py)

---

### GUI Tests: Setup

Concept: Cypress installation, `cy.visit`, `cy.get`, `should` assertions

Introduces Cypress as a JavaScript GUI testing framework. Students install Node.js and Cypress, learn the `describe`/`it`/`cy.` structure, and write their first tests against the TodoMVC vanillaJS application. Key assertion concepts: `contain.text`, `be.visible`, `be.enabled`, `have.attr`, and the distinction between `not.be.visible` (element in DOM but hidden) and `not.exist` (element removed from DOM).

There are no source files for GUI tests — the target is a live website (`https://todomvc.com/examples/javascript-es6/dist/`).

Test Stubs - Student Starting Points (all three provided; see exception note above)

- [test/student/gui/setup/todo_mvc_heading.cy.js](../test/student/gui/setup/todo_mvc_heading.cy.js)
- [test/student/gui/setup/todo_mvc_input.cy.js](../test/student/gui/setup/todo_mvc_input.cy.js)
- [test/student/gui/setup/todo_mvc_empty_state.cy.js](../test/student/gui/setup/todo_mvc_empty_state.cy.js)

Matching Solution Tests

- [test/\_solutions/gui/setup/todo_mvc_heading.cy.js](../test/_solutions/gui/setup/todo_mvc_heading.cy.js)
- [test/\_solutions/gui/setup/todo_mvc_input.cy.js](../test/_solutions/gui/setup/todo_mvc_input.cy.js)
- [test/\_solutions/gui/setup/todo_mvc_empty_state.cy.js](../test/_solutions/gui/setup/todo_mvc_empty_state.cy.js)

---

### GUI Tests: Selectors

Concept: imperative (`cy.get`), declarative (`cy.contains`), chained (`.find`) selectors

Two contrasting strategies for locating elements: imperative selectors target technical HTML properties (tag, class, attribute); declarative selectors target visible text content. Chaining with `.find` narrows a search to children of a previously found element, preventing accidental matches elsewhere on the page.

There are no source files for GUI tests — the target is a live website (`https://todomvc.com/examples/javascript-es6/dist/`).

Test Stub - Student Starting Point

- [test/student/gui/selectors/imperative_selector.cy.js](../test/student/gui/selectors/imperative_selector.cy.js)

Matching Solution Tests

- [test/\_solutions/gui/selectors/imperative_selector.cy.js](../test/_solutions/gui/selectors/imperative_selector.cy.js)
- [test/\_solutions/gui/selectors/declarative_selector.cy.js](../test/_solutions/gui/selectors/declarative_selector.cy.js)
- [test/\_solutions/gui/selectors/chained_selector.cy.js](../test/_solutions/gui/selectors/chained_selector.cy.js)

---

### GUI Tests: Interactions

Concept: `.type`, `.click`, `click({ force: true })`, post-interaction assertions

Simulating user actions: typing text with `{enter}` to submit, clicking checkboxes, and force-clicking CSS-hidden buttons. After each interaction the test asserts the specific DOM change that should result — list length, CSS class changes, element removal. Contrast between `not.be.visible` (hidden by CSS) and `not.exist` (removed from DOM) is reinforced here.

There are no source files for GUI tests — the target is a live website (`https://todomvc.com/examples/javascript-es6/dist/`).

Test Stub - Student Starting Point

- [test/student/gui/interactions/type_and_add.cy.js](../test/student/gui/interactions/type_and_add.cy.js)

Matching Solution Tests

- [test/\_solutions/gui/interactions/type_and_add.cy.js](../test/_solutions/gui/interactions/type_and_add.cy.js)
- [test/\_solutions/gui/interactions/toggle_todo.cy.js](../test/_solutions/gui/interactions/toggle_todo.cy.js)
- [test/\_solutions/gui/interactions/delete_todo.cy.js](../test/_solutions/gui/interactions/delete_todo.cy.js)

---

### GUI Tests: beforeEach

Concept: `beforeEach` hook; shared setup; pre-populated application state

`beforeEach` runs a setup callback before every `it` in its `describe`, eliminating repeated `cy.visit` calls. At higher complexity it pre-populates application state (adding one or multiple todos) so each test starts from a consistent baseline and its body contains only the action and assertion specific to that case.

There are no source files for GUI tests — the target is a live website (`https://todomvc.com/examples/javascript-es6/dist/`).

Test Stub - Student Starting Point

- [test/student/gui/before_each/shared_visit.cy.js](../test/student/gui/before_each/shared_visit.cy.js)

Matching Solution Tests

- [test/\_solutions/gui/before_each/shared_visit.cy.js](../test/_solutions/gui/before_each/shared_visit.cy.js)
- [test/\_solutions/gui/before_each/prepopulated_todo.cy.js](../test/_solutions/gui/before_each/prepopulated_todo.cy.js)
- [test/\_solutions/gui/before_each/multiple_todos.cy.js](../test/_solutions/gui/before_each/multiple_todos.cy.js)
