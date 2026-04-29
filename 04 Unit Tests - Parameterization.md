# PA1417 — Unit Tests: Fixtures

This tutorial introduces `@pytest.fixture` for shared test setup. You will apply it to two in-memory classes, learning when fixtures are preferable to plain helper functions and which tests must bypass the shared fixture entirely.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## Test Example 1: Reducing Repetition — `Playlist`

Open `src/unit/fixtures/playlist.py` and read the class and its docstring. It has four methods to test.

Notice that every test for `Playlist` will need to start the same way: create a `Playlist` and add a few tracks. Without fixtures, every test's Arrange section would repeat those same four lines.

✋ **Open `test/student/unit/fixtures/test_playlist.py`. Write a plain Python function called `make_playlist()` that creates and returns a pre-populated `Playlist`. Call it at the top of each test's Arrange section.**

<details>
<summary>Hint: plain function approach</summary>

```python
from src.unit.fixtures.playlist import Playlist

def make_playlist():
    p = Playlist("My Mix")
    p.add_track("Song A")
    p.add_track("Song B")
    p.add_track("Song C")
    return p

def test_track_count():
    # Arrange
    playlist = make_playlist()
    # Act
    result = playlist.track_count()
    # Assert
    assert result == 3
```

</details><br>

✋ **Now rewrite `make_playlist()` as a `@pytest.fixture`. Declare `playlist` as a parameter in each test function — pytest will call the fixture automatically and inject the result.**

<details>
<summary>Hint: fixture approach</summary>

```python
import pytest
from src.unit.fixtures.playlist import Playlist

@pytest.fixture
def playlist():
    p = Playlist("My Mix")
    p.add_track("Song A")
    p.add_track("Song B")
    p.add_track("Song C")
    return p

def test_track_count(playlist):
    # Arrange
    # (handled by fixture)
    # Act
    result = playlist.track_count()
    # Assert
    assert result == 3
```

> **Why use a fixture at all if a plain function also works?** For pure in-memory objects like `Playlist`, a plain function is technically equivalent. We use a fixture because it is the pytest convention for shared setup, and it prepares you for integration tests where `yield`-based teardown becomes genuinely necessary (see [Integration Tests — Fixtures](08%20Integration%20Tests%20-%20Fixtures.md)).

</details><br>

✋ **Write the remaining tests: `test_contains_existing_track`, `test_contains_missing_track`, `test_remove_track_decreases_count`, and `test_remove_nonexistent_track_raises`. Use `pytest.raises` for the exception test.**

Once you're ready to compare, open the solution: [test/\_solutions/unit/fixtures/test_playlist.py](../test/_solutions/unit/fixtures/test_playlist.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass.

## Test Example 2: More Fixture Practice — `Stack`

Open `src/unit/fixtures/stack.py` and read the class and its docstring. A `Stack` is a last-in, first-out collection: the last item pushed is the first one returned by `pop` or `peek`.

✋ **Create `test/student/unit/fixtures/test_stack.py` with a fixture that pushes three items onto a fresh `Stack`. Write tests for `size`, `is_empty`, `peek`, `pop`, and the error cases.**

One or more of the tests cannot use the pre-populated fixture — think about which ones, and why. For that test, create the object directly inside the test body instead.

Once you're ready to compare, open the solution: [test/\_solutions/unit/fixtures/test_stack.py](../test/_solutions/unit/fixtures/test_stack.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass.

## Test Example 3: Two Fixtures for Two States — `ShoppingCart`

Open `src/unit/fixtures/shopping_cart.py` and read the class. It has five methods to test.

You will find that the tests fall naturally into two groups: some need an empty cart, others need a cart that already has items. Trying to serve both groups with a single fixture means either the fixture builds in items (wrong for empty-state tests) or it does nothing (wrong for populated-state tests).

The solution is two fixtures: one for each meaningful starting state.

✋ **Create `test/student/unit/fixtures/test_shopping_cart.py`. Define two fixtures — `empty_cart` and `stocked_cart` — and write tests that use whichever fixture matches the state each test needs.**

<details>
<summary>Hint: two fixtures for different states</summary>

```python
import pytest
from src.unit.fixtures.shopping_cart import ShoppingCart

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.fixture
def stocked_cart():
    cart = ShoppingCart()
    cart.add_item("apple", 1.50)
    cart.add_item("bread", 2.00)
    cart.add_item("milk", 0.99)
    return cart

def test_new_cart_is_empty(empty_cart):
    assert empty_cart.is_empty() is True

def test_stocked_cart_total(stocked_cart):
    assert stocked_cart.total() == pytest.approx(4.49)
```

> **`pytest.approx`:** Floating-point arithmetic can produce results like `4.490000000000001` instead of exactly `4.49`, so a plain `==` comparison sometimes fails even when the value is correct. `pytest.approx` treats two values as equal if they are close enough (within a small tolerance). Use it whenever you are asserting on `float` results.

> **Rule of thumb:** Define as many fixtures as you have distinct meaningful starting states, not one fixture that tries to do everything. A test that needs a different state from what your fixture provides is a signal to write a second fixture — or, for a truly unique case, to set up inline.

</details><br>

✋ **Write tests for `item_count`, `is_empty`, `add_item`, `remove_item`, and `remove_nonexistent_item_raises`. Use whichever fixture fits each test.**

Once you're ready to compare, open the solution: [test/\_solutions/unit/fixtures/test_shopping_cart.py](../test/_solutions/unit/fixtures/test_shopping_cart.py)

Run `pytest test/student/unit/ -v` and confirm all tests pass.

## Summary

| Source file        | Tests | Concepts practised                                              |
| ------------------ | ----- | --------------------------------------------------------------- |
| `playlist.py`      | 5     | `@pytest.fixture`, shared setup, `pytest.raises`                |
| `stack.py`         | 7     | Fixture practice, LIFO behaviour, setup inline vs fixture       |
| `shopping_cart.py` | 10    | Two fixtures for different states, choosing the right fixture   |

> **Key idea:** Fixtures centralise repeated setup so each test body focuses only on what is unique to that test. When tests split across two distinct starting states, define two fixtures rather than forcing one fixture to cover both. When a test needs a state that no fixture provides, create the object inline.
