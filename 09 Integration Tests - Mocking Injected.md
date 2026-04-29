# PA1417 — Integration Tests: Fixtures

This tutorial extends fixture knowledge to integration tests — tests where the code under test interacts with something outside memory, such as the filesystem. You will discover why plain helper functions are insufficient at this level and why `yield`-based teardown is essential.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## Test Example 1: `NoteWriter`

### Step 1: When a Plain Function Is Not Enough

Open `src/integration/fixtures/note_writer.py` and read the class and its docstring. Unlike the classes from the unit test tutorials, `NoteWriter` reads and writes a real file on disk. This makes it an **integration test** — the code is no longer isolated in memory, it depends on the filesystem.

Open `test/student/integration/fixtures/test_note_writer_integration.py`.

✋ **Start by writing a plain Python helper function called `writer()` that creates an empty file and returns a `NoteWriter` instance. Use it in your tests the same way you used `make_playlist()` in [Unit Tests — Fixtures](03%20Unit%20Tests%20-%20Fixtures.md) — call it at the top of each test's Arrange section.**

```python
import os
from src.integration.fixtures.note_writer import NoteWriter

def writer():
    filepath = "test_notes.txt"
    with open(filepath, 'a', encoding='utf-8'):
        pass
    return NoteWriter(filepath)

def test_count_starts_at_zero():
    # Arrange
    w = writer()
    # Act
    result = w.count()
    # Assert
    assert result == 0

def test_add_increases_count():
    # Arrange
    w = writer()
    # Act
    w.add("buy milk")
    result = w.count()
    # Assert
    assert result == 1

# ... write the remaining tests the same way
```

> Note: `'a'` (append) mode creates the file if it does not exist — it does **not** truncate it if it does. This is intentionally different from `'w'` (write) mode, which would erase the file each time.

✋ **Run `pytest test/student/integration/ -v` and read the results carefully. Do all tests pass?**

<details>
<summary>What did you observe?</summary>

Some tests fail. `test_notes.txt` is not deleted after each test, so it accumulates notes as tests run. A later test opens a file that already contains notes written by an earlier test — the counts are wrong before that test has even called `add()`.

You might think switching to `'w'` mode would fix this — and it would make the tests pass, because `'w'` truncates the file to empty at the start of each test. But that only masks the problem: the file is still never deleted after the tests finish. Every test run leaves `test_notes.txt` sitting in your working directory. On a real project this silently pollutes the repository, and for resources that cannot be overwritten (a directory, a database row, a network session) there is no `'w'`-mode equivalent to fall back on.

A plain function can only run code *before* the test. It has no mechanism to run code *after* — whether the test passed, failed, or was interrupted.

</details><br>

### Step 2: Fixture Teardown with `yield`

✋ **Rewrite `writer()` as a pytest fixture using `yield`. The code before `yield` is the setup — the code after `yield` is the teardown. Delete the file in the teardown.**

<details>
<summary>Hint: fixture with teardown</summary>

```python
import os
import pytest
from src.integration.fixtures.note_writer import NoteWriter

@pytest.fixture
def writer():
    filepath = "test_notes.txt"
    # Setup: create an empty file
    with open(filepath, 'w', encoding='utf-8'):
        pass
    w = NoteWriter(filepath)
    # yield pauses this function and hands the value to the test.
    # pytest remembers where it paused. Once the test finishes,
    # pytest resumes the function from this point and runs whatever
    # comes after — the teardown. This is why os.remove() below
    # runs after the test rather than before it.
    yield w
    # Teardown: delete the file so it does not affect the next test
    os.remove(filepath)
```

Each test that declares `writer` as a parameter receives a fresh `NoteWriter` pointing at an empty file. Once the test finishes — whether it passed or failed — pytest runs the teardown and deletes the file.

</details><br>

Run `pytest test/student/integration/ -v` several times in a row and confirm the results are consistent every time.

Once you're ready to compare, open the solution: [test/\_solutions/integration/fixtures/test_note_writer_integration.py](../test/_solutions/integration/fixtures/test_note_writer_integration.py)

## Test Example 2: Append-Mode Files — `CsvLogger`

Open `src/integration/fixtures/csv_logger.py` and read the class. Unlike `NoteWriter`, which overwrites the file on each operation, `CsvLogger` *appends* to the CSV file. This makes the isolation problem even more concrete: every single test run adds rows to the file, so a test that does not clean up will see a larger and larger row count on subsequent runs.

Create the file `test/student/integration/fixtures/test_csv_logger_integration.py`.

✋ **Write a fixture that creates an empty CSV file and yields a `CsvLogger` instance. Delete the file in the teardown. Then write four tests: initial row count is zero, logging one row gives count 1, logging two rows gives count 2, and `read_all()` returns the logged data.**

<details>
<summary>Hint: fixture with teardown</summary>

```python
import os
import pytest
from src.integration.fixtures.csv_logger import CsvLogger

@pytest.fixture
def logger():
    filepath = "test_log.csv"
    with open(filepath, "w", encoding="utf-8"):
        pass
    yield CsvLogger(filepath)
    os.remove(filepath)
```

The teardown (`os.remove`) is the same pattern as `NoteWriter`. The difference is the *consequence* of skipping it: with `NoteWriter` the count might be off by a fixed amount; with `CsvLogger` it grows with every test run because every call to `log()` adds a new row.

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/integration/fixtures/test_csv_logger_integration.py](../test/_solutions/integration/fixtures/test_csv_logger_integration.py)

Run `pytest test/student/integration/ -v` several times in a row and confirm the results are consistent.

## Test Example 3: A Whole Directory — `FileCache`

Open `src/integration/fixtures/file_cache.py` and read the class. `FileCache` stores each key as a separate `.txt` file inside a directory. Cleaning up now means removing *an entire directory*, not just a single file. `shutil.rmtree` removes a directory and everything inside it.

Create the file `test/student/integration/fixtures/test_file_cache_integration.py`.

✋ **Write a fixture that creates the cache directory with `os.makedirs`, yields a `FileCache` instance, and calls `shutil.rmtree` in the teardown. Then write five tests covering `has`, `store`, `retrieve`, two keys stored independently, and overwriting a key.**

<details>
<summary>Hint: fixture with shutil.rmtree teardown</summary>

```python
import os
import shutil
import pytest
from src.integration.fixtures.file_cache import FileCache

@pytest.fixture
def cache():
    directory = "test_cache_dir"
    os.makedirs(directory, exist_ok=True)
    yield FileCache(directory)
    shutil.rmtree(directory)
```

`shutil.rmtree` deletes the directory and all files inside it in one call. This is the standard teardown pattern whenever your fixture creates a directory rather than a single file.

</details><br>

Once you're ready to compare, open the solution: [test/\_solutions/integration/fixtures/test_file_cache_integration.py](../test/_solutions/integration/fixtures/test_file_cache_integration.py)

Run `pytest test/student/integration/ -v` several times in a row and confirm the results are consistent.

## Summary

| Source file      | Tests | Concepts practised                                                   |
| ---------------- | ----- | -------------------------------------------------------------------- |
| `note_writer.py` | 4     | Integration fixture, `yield`-based teardown, `os.remove`             |
| `csv_logger.py`  | 4     | Append-mode file — isolation failure is more visible without teardown |
| `file_cache.py`  | 5     | Directory teardown with `shutil.rmtree`                              |

> **Key idea:** Use `yield` in a fixture whenever setup creates something that must be cleaned up — a file, a directory, a database record. The code after `yield` runs after the test completes, whether the test passed or failed. When teardown removes an entire directory, use `shutil.rmtree` rather than `os.remove`.
