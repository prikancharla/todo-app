# HTML Document Structure

HTML gives a page structure and meaning. CSS will later control appearance, and JavaScript will later add behavior.

## A Small Todo Example

```html
<!doctype html>
<html lang="en">
  <head>
    <title>Todo List</title>
  </head>
  <body>
    <h1>My Todo List</h1>
    <section>
      <h2>Tasks</h2>
      <ul>
        <li data-uid="11111111-1111-1111-1111-111111111111" data-is-complete="false">
          <h3>Buy milk</h3>
          <p>From the grocery store</p>
          <p>Status: Incomplete</p>
        </li>
      </ul>
    </section>
  </body>
</html>
```

HTML elements normally have an opening tag, content, and a matching closing tag. Nesting shows which content belongs inside which element: the task `li` belongs in the `ul`, which belongs in the task `section`.

## Tags Used Here

- `<!doctype html>`: tells the browser to use modern HTML rules. It is a declaration, not a visible page element.
- `<html lang="en">`: wraps the entire page. `lang="en"` declares English for browsers and assistive technology.
- `<head>`: holds information about the page rather than visible content.
- `<title>`: sets the browser-tab title.
- `<body>`: contains everything visible in the page.
- `<h1>`, `<h2>`, and `<h3>`: headings in order from the page title to smaller sections. Their order communicates structure, not just text size.
- `<section>`: groups one related part of a page; here, the task-list area.
- `<ul>` and `<li>`: an unordered collection and one item in that collection. Tasks are a list with no required numerical order.
- `<p>`: a paragraph of supporting text, used for a task description and its visible status.

## Attributes And Backend-Shaped Mock Data

Attributes add information to an opening tag. In this example, `data-uid` and `data-is-complete` are custom `data-*` attributes. They do not display on the page, but they let a static task carry information that matches the backend response:

```text
uid         -> data-uid
title       -> h3 text
description -> first paragraph
is_complete -> data-is-complete and status text
```

Attribute values are text in HTML, so `data-is-complete="false"` represents the backend Boolean value `false`. Later, JavaScript can read these values or replace the mock tasks with real responses from `GET /tasks`.

## What Static Means

Opening `frontend/index.html` in a browser displays the markup exactly as written. At this stage, it does not fetch tasks, save edits, or change completion status. That is intentional: first learn page structure, then add styling and behavior in later steps.
