# PA1417 — GUI Tests: Selectors

This tutorial introduces the two main strategies for finding elements in a GUI test: **imperative** (white-box) selectors, which target technical properties of the HTML source, and **declarative** (black-box) selectors, which target visible text. A third form, **chained** selectors, narrows a search to elements inside a previously found element.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint, expand it only if you need support.

## What is a selector?

Before a Cypress test can assert anything about an element, it must locate that element. A **selector** is the instruction that tells Cypress which element to find.

There are two contrasting strategies:

| Strategy        | Method                | Targets                             | Perspective                          |
| --------------- | --------------------- | ----------------------------------- | ------------------------------------ |
| **Imperative**  | `cy.get(cssSelector)` | Tag name, CSS class, HTML attribute | White-box: you read the source code  |
| **Declarative** | `cy.contains(text)`   | Visible text content                | Black-box: you describe what you see |

Neither is always better. Imperative selectors are precise and fast; they break when class names or attributes change. Declarative selectors are resilient to refactoring; they break when the visible text changes.

## Test Example 1: Imperative Selectors — `cy.get`

`cy.get` accepts any CSS selector. The three most common forms:

| Form      | Example                         | Matches                            |
| --------- | ------------------------------- | ---------------------------------- |
| Tag name  | `cy.get('h1')`                  | All `<h1>` elements                |
| CSS class | `cy.get('.new-todo')`           | Elements with class `new-todo`     |
| Attribute | `cy.get('[placeholder="..."]')` | Elements with that attribute value |

Here is the specification for the TodoMVC page you need to verify:

| ID    | Requirement                                                                      |
| ----- | -------------------------------------------------------------------------------- |
| REQ-6 | The page must display a visible main heading element.                            |
| REQ-7 | A todo input field with the CSS class `new-todo` must be present and enabled.    |
| REQ-8 | The todo input field must carry the placeholder text `"What needs to be done?"`. |

Open `test/student/gui/selectors/imperative_selector.cy.js`. It has three tests, each with a TODO.

✋ **Fill in all three tests using imperative selectors.**

<details>
<summary>Hint: three selectors</summary>

```javascript
// by tag name
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
cy.get("h1").should("be.visible");

// by CSS class
cy.get(".new-todo").should("be.enabled");

// by attribute
cy.get('[placeholder="What needs to be done?"]').should("be.visible");
```

</details><br>

In the Cypress test runner, select the spec from the spec list and confirm all tests pass (green tick).

Once you are ready to compare, open the solution: [test/\_solutions/gui/selectors/imperative_selector.cy.js](../test/_solutions/gui/selectors/imperative_selector.cy.js)

## Test Example 2: Declarative Selectors — `cy.contains`

`cy.contains` finds elements by their visible text. It has two forms:

```javascript
cy.contains("todos"); // finds any element containing that text
cy.contains("li", "Buy milk"); // finds an <li> element containing that text
```

The second form is more precise: it restricts which element types are considered. Without the tag restriction, `cy.contains('todos')` might match any element that contains that text, but adding the element type ensures only elements of that type are considered.

Here is the specification for the TodoMVC page you need to verify:

| ID     | Requirement                                                                              |
| ------ | ---------------------------------------------------------------------------------------- |
| REQ-9  | The page must display visible text reading `"todos"`.                                    |
| REQ-10 | The element displaying `"todos"` must be an `<h1>` heading.                              |
| REQ-11 | The footer must include a paragraph containing the text `"Double-click to edit a todo"`. |

✋ **Create `test/student/gui/selectors/declarative_selector.cy.js`. Write three tests:**

1. Find the heading by its text content (`cy.contains('todos')`)
2. Find the heading using a type restriction (`cy.contains('h1', 'todos')`)
3. Find the footer paragraph that contains the text `'Double-click to edit a todo'`

<details>
<summary>Hint: contains with a type restriction</summary>

```javascript
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
cy.contains("todos").should("be.visible");
cy.contains("h1", "todos").should("be.visible");
```

The type restriction narrows the search to `<h1>` elements only. Without it, `cy.contains('todos')` would match the first element anywhere in the DOM that contains that text, which may not be the element you intend.

</details><br>

In the Cypress test runner, select the spec from the spec list and confirm all tests pass (green tick).

Once you are ready to compare, open the solution: [test/\_solutions/gui/selectors/declarative_selector.cy.js](../test/_solutions/gui/selectors/declarative_selector.cy.js)

## Test Example 3: Chained Selectors — `.find`

When you have located a parent element, you can narrow the search to its children using `.find(cssSelector)`:

```javascript
cy.contains("p", "Part of").find("a");
```

This finds the `<p>` containing "Part of", then within that element only, finds the `<a>`. The TodoMVC footer contains **two** `<a>` links (one for the author, one for TodoMVC), so `cy.get('a')` matches both of them. If you then try to assert `.should('have.text', 'TodoMVC')`, Cypress fails because the assertion cannot apply to a collection of elements. Chaining `.find` onto the specific paragraph reduces the match to exactly one element, making the assertion possible.

All three tests below use elements that are always present on the page, so no setup is needed.

Here is the specification for the TodoMVC page you need to verify:

| ID     | Requirement                                                                         |
| ------ | ----------------------------------------------------------------------------------- |
| REQ-12 | The "Part of" attribution paragraph must contain a link with the label `"TodoMVC"`. |
| REQ-13 | The todo input field must exist within the `.header` section of the application.    |
| REQ-14 | The main heading must exist within the `.todoapp` section of the application.       |

✋ **Create `test/student/gui/selectors/chained_selector.cy.js`. Write three tests, each using `.find` to locate a child element within a parent:**

1. Find the `a` link inside the paragraph containing "Part of" and assert its text is `'TodoMVC'`
2. Find the `.new-todo` input inside `.header` and assert it is visible
3. Find the `h1` inside `.todoapp` and assert its text is `'todos'`

<details>
<summary>Hint: why cy.get('a') fails here</summary>

```javascript
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
// cy.get('a').should('have.text', 'TodoMVC') — fails: matches two <a> elements
cy.contains("p", "Part of").find("a").should("have.text", "TodoMVC");
```

The footer has two `<a>` elements: one for the author and one for TodoMVC. `cy.get('a')` returns both, so any single-element assertion on the collection fails. Chaining `.find('a')` onto the specific paragraph that contains "Part of" reduces the match to exactly one.

</details><br>

In the Cypress test runner, select the spec from the spec list and confirm all tests pass (green tick).

Once you are ready to compare, open the solution: [test/\_solutions/gui/selectors/chained_selector.cy.js](../test/_solutions/gui/selectors/chained_selector.cy.js)

## Summary

| Test file                    | Tests | Concepts practised                                                            |
| ---------------------------- | ----- | ----------------------------------------------------------------------------- |
| `imperative_selector.cy.js`  | 3     | `cy.get` with tag, class, and attribute selectors                             |
| `declarative_selector.cy.js` | 3     | `cy.contains` without type restriction, with type restriction, on footer text |
| `chained_selector.cy.js`     | 3     | `.find` to narrow within a parent, avoiding ambiguous multi-element matches   |

> **Key idea:** Use `cy.get` when you want to target a specific technical property (class, attribute, tag). Use `cy.contains` when you want to target what the user sees (visible text). Use `.find` when you need to locate a child within an already-found parent, to avoid accidental matches elsewhere on the page.
