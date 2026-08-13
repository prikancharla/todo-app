# CSS Basics And Selectors

CSS controls how HTML looks without changing the HTML's meaning or adding behavior. In this project, `frontend/index.html` links to `frontend/styles.css` from its `head`:

```html
<link rel="stylesheet" href="styles.css">
```

`rel="stylesheet"` tells the browser what kind of file it is, and `href="styles.css"` gives the path from `index.html` to that file.

## Rules, Selectors, And Properties

A CSS rule selects HTML elements, then gives them presentation properties:

```css
li {
    padding: 10px 0;
    border-bottom: 1px solid #C9907A;
}
```

- `li` is the selector: it targets every task list item.
- `padding` creates space inside each item.
- `border-bottom` draws only the divider below each item.
- A semicolon ends each property declaration.

## Common Selectors Used Here

```css
h1 { }
.status { }
li[data-is-complete="true"] { }
li:last-child { }
```

- `h1` selects every `h1` element.
- `.status` selects elements with `class="status"`; classes are reusable labels for elements with the same presentation role.
- `li[data-is-complete="true"]` selects only tasks whose existing HTML data attribute says they are complete.
- `li:last-child` selects only the final task in the list. It removes the unnecessary final divider.

## Spacing And Readability

CSS separates space outside an element from space inside it:

```css
body { margin: 40px; }
li { padding: 10px 0; }
```

`margin` creates outer space, so the page content does not touch the browser edge. `padding` creates inner space, so content has room within its element. Browser headings and paragraphs have default margins; setting a smaller explicit margin makes a compact task list easier to control.

## Color And Fonts

Colors can be written as hexadecimal values such as `#4A2C24`. A palette works best when it assigns roles: darker colors for readable text, lighter colors for the page background, and an accent color for the title and dividers.

The page uses an imported web font for its title:

```css
@import url("https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&display=swap");

h1 {
    font-family: Caveat, cursive;
}
```

The fallback `cursive` is used if the web font cannot load. Imported fonts must appear before ordinary CSS rules.

## What CSS Does Not Do Yet

The page is still static. CSS changes presentation only; it does not fetch `GET /tasks`, save a task, or toggle completion. Those need JavaScript and a later backend connection.
