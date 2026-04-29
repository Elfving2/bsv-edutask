# PA1417 — GUI Tests: Setup

This tutorial introduces GUI testing with Cypress. Instead of testing Python functions, you are testing a real web application by scripting the same interactions a user would perform in a browser: visiting a page, finding elements, and asserting that the page looks and behaves correctly.

> The ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint, expand it only if you need support.

## What is a GUI test?

A **GUI test** (also called an end-to-end or E2E test) drives a real browser and verifies the application from the outside, the same perspective a user has. It does not import source files or call functions directly. Instead, it:

1. **Visits** a URL
2. **Finds** elements on the page
3. **Asserts** that those elements have the expected properties

This tutorial uses **Cypress**, a JavaScript testing framework, and the **TodoMVC** application at `https://todomvc.com/examples/javascript-es6/dist/`, a small, stable todo-list app used widely as a frontend testing demo target.

## Setting Up Cypress

### 1. Install Node.js

Cypress requires Node.js 18 or later. Download and install it from [https://nodejs.org](https://nodejs.org), choosing the **LTS** version, which will be 18 or higher. Verify the installation:

```shell
node --version
npm --version
```

Both commands should print a version number.

### 2. Install Cypress

From the root of the repository, install the project's JavaScript dependencies:

```shell
npm install
```

This reads `package.json` and installs Cypress into `node_modules/`. The first install may take a minute.

> **Note for Python developers:** `npm install` is roughly equivalent to creating and populating a `venv`. Packages are installed locally inside the project's `node_modules/` folder, not machine-wide, so they won't affect other Node projects. Unlike Python, there is nothing to "activate", Node automatically finds packages in the nearest `node_modules/` folder.

Verify Cypress is available:

```shell
npx cypress --version
```

### 3. Confirm the configuration

Open `cypress.config.js` at the root of the repository. It points Cypress at the student test folder:

```javascript
specPattern: "test/student/gui/**/*.cy.js";
```

This means Cypress will discover and run any file matching that pattern. Solution files live under `test/_solutions/gui/` and are not run by default.

## Cypress Test Structure

A Cypress test file uses three building blocks:

| Construct                         | Purpose                   | Python analogy       |
| --------------------------------- | ------------------------- | -------------------- |
| `describe('name', () => { ... })` | Groups related tests      | test class or module |
| `it('name', () => { ... })`       | One test case             | `def test_name():`   |
| `cy.` commands                    | Interact with the browser | pytest + mock calls  |

The smallest possible test:

```javascript
describe("TodoMVC — page load", () => {
    it("shows the main heading", () => {
        cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
        cy.get("h1").should("contain.text", "todos");
    });
});
```

- `cy.visit(url)`: navigates the browser to that URL
- `cy.get(selector)`: finds an element using a CSS selector
- `.should('contain.text', 'todos')`: asserts that the element contains the text `"todos"`

## Test Example 1: The Main Heading

### Step 1: Run the starter file

Open `test/student/gui/setup/todo_mvc_heading.cy.js`. It contains a single test with a TODO comment.

Launch the Cypress test runner:

```shell
npx cypress open
```

Select **E2E Testing**, choose any browser (Chrome or Electron), and click on `todo_mvc_heading.cy.js` from the spec list. The test will run and immediately fail with "Not implemented".

> **Keep the Cypress runner open** for all remaining examples in this and subsequent tutorials. Whenever you save changes to a spec file, Cypress reruns it automatically. If you create a new spec file, it will appear in the spec list, click it to run it for the first time.

### Step 2: Write the test

You may not have written a GUI test before, so let's walk through it together, one line at a time.

**Add the visit call.**

Inside the `it(...)` callback, add this line:

```javascript
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
```

`cy.visit` tells Cypress to open that URL in the browser it controls. Save the file now and watch the Cypress runner, it will rerun automatically. You should see the TodoMVC app load in the Cypress preview pane. The test will still pass (it has no assertion yet), but you can confirm the page is actually being visited.

**Add the selector.**

On the next line, add:

```javascript
cy.get("h1");
```

`cy.get` finds an element on the page using a CSS selector. `"h1"` matches the heading element. Save again and watch Cypress rerun. Nothing visible changes yet because you have not told Cypress what to do with the element. However, you can hover over the **get h1** step in the left sidebar of the Cypress window and Cypress will highlight the matched element directly on the page, which is a handy way to confirm your selector found what you expected.

**Add the assertion.**

Chain `.should(...)` on to the `cy.get` call so the two lines become one:

```javascript
cy.get("h1").should("contain.text", "todos");
```

`.should("contain.text", "todos")` is an assertion that checks the `<h1>` element's text includes the word `"todos"`. Save the file and watch the Cypress runner, the test should turn green.

**Now make it fail on purpose.**

Change `"todos"` to something that is not on the page, such as `"hello"`:

```javascript
cy.get("h1").should("contain.text", "hello");
```

Save and watch the test turn red. Read the error message in the Cypress runner. It tells you what text it found (`"todos"`) and what it expected (`"hello"`). This is what a real assertion failure looks like, and reading these messages is a skill you will use constantly. Revert the change back to `"todos"` before moving on.

Your finished test body, when configured correctly, looks like this:

```javascript
cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
cy.get("h1").should("contain.text", "todos");
```

Once you are ready to compare, open the solution: [test/\_solutions/gui/setup/todo_mvc_heading.cy.js](../test/_solutions/gui/setup/todo_mvc_heading.cy.js)

## Test Example 2: The Input Field

Here is the specification for the TodoMVC input field you need to verify:

| ID    | Requirement                                                                            |
| ----- | -------------------------------------------------------------------------------------- |
| REQ-1 | The input field must be visible to the user when the page loads.                       |
| REQ-2 | The input field must be enabled (i.e., the user can type into it) when the page loads. |
| REQ-3 | The input field must display the placeholder text `"What needs to be done?"`.          |

Before writing any assertions, you need to work out which CSS selector targets the input field. This section walks you through using Cypress's built-in **Selector Playground** to do that.

### Step 1: Open the stub file

Open [test/student/gui/setup/todo_mvc_input.cy.js](../test/student/gui/setup/todo_mvc_input.cy.js). It has one active `it` block and two commented-out ones. In the Cypress runner, click the spec to run it. The first test will fail with "Not implemented", and the TodoMVC page will appear in the preview pane on the right.

### Step 2: Open the Selector Playground

Look at the toolbar running across the top of the Cypress runner window. Find the small **crosshair icon** (it looks like ⊕) and click it. This opens the **Selector Playground**.

The cursor on the preview pane will change to a crosshair. Hovering over any element now highlights it in blue and shows a suggested CSS selector in the bar at the top of the preview pane.

### Step 3: Identify the input field's selector

Move your cursor over the text input near the top of the TodoMVC page, the one with the placeholder text "What needs to be done?". Click on it.

Cypress highlights the element and displays a selector in the bar, something like:

```
cy.get('.new-todo')
```

This is the CSS class selector for the input field. Copy it. Click the crosshair icon again (or press Escape) to exit the Selector Playground.

### Step 4: Write the first test

Go back to the stub file. In the first `it` block, and a `cy.get` using the selector you just found:

```javascript
it("is visible", () => {
    cy.visit("https://todomvc.com/examples/javascript-es6/dist/");
    cy.get(".new-todo").should("be.visible");
    // Remove or comment out the Error line
});
```

Save the file. The first test should turn green in the Cypress runner.

### Step 5: Write the remaining two tests

✋ **Uncomment the second and third `it` blocks, then fill them in yourself.** Each one should visit the page, get the same element, and assert a different property from the specification table above.

The assertion keywords you need are:

- `be.enabled`: the element is interactive and can receive input
- `have.attr`: the element has a specific HTML attribute set to a specific value

<details>
<summary>Hint: enabled assertion</summary>

```javascript
cy.get(".new-todo").should("be.enabled");
```

`be.enabled` takes no extra arguments, it just checks the element is interactive.

</details>

<details>
<summary>Hint: attribute assertion</summary>

```javascript
cy.get(".new-todo").should("have.attr", "placeholder", "What needs to be done?");
```

`have.attr` takes two arguments: the attribute name and its expected value.

</details><br>

Confirm both tests pass (green tick) in the Cypress runner.

Once you are ready to compare, open the solution: [test/\_solutions/gui/setup/todo_mvc_input.cy.js](../test/_solutions/gui/setup/todo_mvc_input.cy.js)

## Test Example 3: The Empty State

Here is the specification for the TodoMVC empty state you need to verify:

| ID    | Requirement                                                                     |
| ----- | ------------------------------------------------------------------------------- |
| REQ-4 | The main section must not be visible to the user when no todos have been added. |
| REQ-5 | The footer must not be visible to the user when no todos have been added.       |

When no todos have been added, the TodoMVC app hides both the `.main` section and the `.footer`. It hides them using CSS (`display: none`) rather than removing them from the DOM. This matters for your assertion choice:

- `.should('not.exist')`: the element is **not in the DOM** at all
- `.should('not.be.visible')`: the element **is in the DOM** but is not visible

Because `.main` and `.footer` are always in the DOM (just hidden), use `.should('not.be.visible')`.

✋ **Open [test/student/gui/setup/todo_mvc_empty_state.cy.js](../test/student/gui/setup/todo_mvc_empty_state.cy.js). Write two tests: one asserting that `.main` is not visible, and one asserting that `.footer` is not visible.**

<details>
<summary>Hint: not.be.visible</summary>

```javascript
cy.get(".main").should("not.be.visible");
```

</details><br>

In the Cypress test runner, select the spec from the spec list and confirm all tests pass (green tick).

Once you are ready to compare, open the solution: [test/\_solutions/gui/setup/todo_mvc_empty_state.cy.js](../test/_solutions/gui/setup/todo_mvc_empty_state.cy.js)

## Summary

| Test file                    | Tests | Concepts practised                      |
| ---------------------------- | ----- | --------------------------------------- |
| `todo_mvc_heading.cy.js`     | 1     | `cy.visit`, `cy.get`, `contain.text`    |
| `todo_mvc_input.cy.js`       | 3     | `be.visible`, `be.enabled`, `have.attr` |
| `todo_mvc_empty_state.cy.js` | 2     | `not.be.visible` vs `not.exist`         |

> **Key idea:** Every Cypress test follows the same three-step shape: visit a page, get an element, assert something about it. The assertion keyword (`contain.text`, `be.visible`, `have.attr`) changes depending on what property you are checking.
