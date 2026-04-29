# PA1417 — GUI Tests: Interactions

This tutorial covers the commands that simulate user actions: typing text into an input, clicking a button or checkbox, and handling the case where a button is intentionally hidden until the user hovers over it.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint, expand it only if you need support.

## What is an interaction?

A selector finds an element. An **interaction** acts on it, the same way a user would. The two most common Cypress interaction commands are:

| Command         | What it does                                      |
| --------------- | ------------------------------------------------- |
| `.type('text')` | Types into an input field, character by character |
| `.click()`      | Clicks an element                                 |

Special keys are typed using curly-brace notation inside `.type()`: `{enter}` presses Enter, `{backspace}` deletes a character.

After an interaction, you assert that the page has changed in the expected way: a new item appeared, a class was added, an element disappeared.

## Test Example 1: Typing and Adding Todos — `.type`

Open `test/student/gui/interactions/type_and_add.cy.js`. It has three tests, each with a TODO.

The TodoMVC input field has the CSS class `.new-todo`. Typing text followed by `{enter}` adds a new item to `.todo-list`:

```javascript
cy.get(".new-todo").type("Buy milk{enter}");
```

Useful assertions after adding items:

- `.should('have.length', n)`: asserts a collection has exactly `n` elements
- `.should('have.value', '')`: asserts an input field's value equals the given string

Here is the specification for todo creation you need to verify:

| ID     | Requirement                                                                              |
| ------ | ---------------------------------------------------------------------------------------- |
| REQ-15 | When a user types a todo and presses Enter, that item must appear in the list.           |
| REQ-16 | After a todo is submitted, the input field must be cleared and ready for the next entry. |
| REQ-17 | When two todos are added in sequence, both items must appear in the list.                |

✋ **Fill in all three tests:**

1. Add one todo and assert the list has one item
2. Add one todo and assert the input field is now empty
3. Add two todos in sequence and assert the list has two items

<details>
<summary>Hint: list length assertion</summary>

```javascript
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
cy.get(".new-todo").type("Buy milk{enter}");
cy.get(".todo-list li").should("have.length", 1);
```

`cy.get('.todo-list li')` selects all `<li>` elements inside `.todo-list`. `have.length` checks how many were matched.

</details><br>

In the Cypress test runner, select the spec from the spec list and confirm all tests pass (green tick).

Once you are ready to compare, open the solution: [test/\_solutions/gui/interactions/type_and_add.cy.js](../test/_solutions/gui/interactions/type_and_add.cy.js)

## Test Example 2: Clicking a Checkbox — `.click` and CSS Classes

Here is the specification for todo completion you need to verify:

| ID     | Requirement                                                                        |
| ------ | ---------------------------------------------------------------------------------- |
| REQ-18 | When a todo is toggled, its list item must receive the `completed` CSS class.      |
| REQ-19 | When a todo is completed, its text label must remain visible.                      |
| REQ-20 | When a completed todo is toggled again, the `completed` CSS class must be removed. |

✋ **Create `test/student/gui/interactions/toggle_todo.cy.js`. Write three tests:**

1. Add a todo, click its toggle, assert the `<li>` has the class `completed`
2. Add a todo, click its toggle, assert the label is still visible
3. Add a todo, toggle it twice, assert the `<li>` does **not** have the class `completed`

Each test needs to first add a todo item, then interact with it. Use the chained selector pattern from Tutorial 12: `cy.contains('li', 'text').find('.toggle').click()`.

Useful assertions:

- `.should('have.class', 'completed')`: asserts the element has that CSS class
- `.should('not.have.class', 'completed')`: asserts the element does not have that CSS class

<details>
<summary>Hint: toggling a specific item</summary>

```javascript
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
cy.get(".new-todo").type("Buy milk{enter}");
cy.contains("li", "Buy milk").find(".toggle").click();
cy.contains("li", "Buy milk").should("have.class", "completed");
```

`cy.contains('li', 'Buy milk')` gets the list item. `.find('.toggle')` narrows to its checkbox. `.click()` checks it. The final assertion targets the `<li>` itself to check its CSS class.

</details><br>

In the Cypress test runner, select the spec from the spec list and confirm all tests pass (green tick).

Once you are ready to compare, open the solution: [test/\_solutions/gui/interactions/toggle_todo.cy.js](../test/_solutions/gui/interactions/toggle_todo.cy.js)

## Test Example 3: Clicking a Hidden Button — `click({ force: true })`

The TodoMVC delete button (`.destroy`) is hidden by CSS unless the user is hovering over the todo item. Cypress refuses to click elements it considers invisible, so a plain `.click()` will fail.

The `{ force: true }` option overrides this safety check and clicks the element regardless of its visibility:

```javascript
cy.contains("li", "Buy milk").find(".destroy").click({ force: true });
```

This reflects a real-world pattern: some UI elements are legitimately hidden until a hover state activates them, and the test needs to interact with them anyway.

Here is the specification for todo deletion you need to verify:

| ID     | Requirement                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------- |
| REQ-21 | When a todo is deleted, it must be removed from the DOM entirely.                                       |
| REQ-22 | When one of two todos is deleted, only that item must be removed and the other must remain in the list. |

✋ **Create `test/student/gui/interactions/delete_todo.cy.js`. Write two tests:**

1. Add one todo, delete it, assert it no longer exists in the DOM
2. Add two todos, delete one by name, assert the list has one item and the other todo is still there

For deletion, use `.should('not.exist')`, unlike the empty-state tests in Tutorial 11, a deleted item is completely removed from the DOM (not just hidden).

<details>
<summary>Hint: force click and not.exist</summary>

```javascript
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
cy.get(".new-todo").type("Buy milk{enter}");
cy.contains("li", "Buy milk").find(".destroy").click({ force: true });
cy.contains("li", "Buy milk").should("not.exist");
```

After deletion the element is gone from the DOM, so `not.exist` is correct here, unlike `not.be.visible`, which only checks visibility.

</details><br>

In the Cypress test runner, select the spec from the spec list and confirm all tests pass (green tick).

Once you are ready to compare, open the solution: [test/\_solutions/gui/interactions/delete_todo.cy.js](../test/_solutions/gui/interactions/delete_todo.cy.js)

## Summary

| Test file            | Tests | Concepts practised                              |
| -------------------- | ----- | ----------------------------------------------- |
| `type_and_add.cy.js` | 3     | `.type`, `{enter}`, `have.length`, `have.value` |
| `toggle_todo.cy.js`  | 3     | `.click`, `have.class`, `not.have.class`        |
| `delete_todo.cy.js`  | 2     | `.click({ force: true })`, `not.exist`          |

> **Key idea:** After every interaction, assert the specific change you expect to see: a new item in a list, a class added to an element, or an element removed from the DOM. `not.be.visible` and `not.exist` are different: use `not.be.visible` when the element stays in the DOM but is hidden (CSS), and `not.exist` when the element is actually removed.
