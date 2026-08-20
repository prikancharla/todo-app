# JavaScript: Fetching And Rendering Data

JavaScript gives a web page behavior. A common frontend job is to request data from an API and turn that data into visible HTML.

## The General Pattern

```text
request data
→ wait for the response
→ convert JSON into JavaScript values
→ create HTML elements from those values
→ insert the elements into the page
```

CSS controls how the generated elements look. JavaScript controls when they are created and what data they contain.

## Values With `const`

`const` gives a value a descriptive name that should not later point to a different value.

```javascript
const apiUrl = "https://example.com/items";
const itemList = document.getElementById("item-list");
```

`apiUrl` stores text. `itemList` stores a reference to an HTML element. `const` does not make an object or element completely unchangeable: it means the variable cannot be reassigned to a different value. For example, JavaScript can still add children to `itemList`.

## Functions, `async`, `await`, And `fetch`

A function is a named group of instructions. Calling it runs those instructions:

```javascript
async function loadItems() {
    const response = await fetch(apiUrl);
    const items = await response.json();
}

loadItems();
```

`fetch` is the browser's built-in way to make an HTTP request. With no additional options, `fetch(apiUrl)` sends a `GET` request.

The request follows this sequence:

```text
JavaScript calls fetch
→ browser sends an HTTP request
→ server processes the request and sends a response
→ browser receives the response
→ JavaScript reads the response body as JSON
```

Network requests finish later, not immediately. `fetch` returns a Promise: a value representing work still in progress. `await` pauses only the current `async` function until that work finishes; it does not freeze the whole browser page. An `await` expression can only be used inside an `async` function.

## The Two Results Of A Request

`fetch` has two stages:

```javascript
const response = await fetch(apiUrl);
const items = await response.json();
```

The first line gives an HTTP Response, not the data itself. It contains HTTP-level information:

```javascript
response.ok      // true for a successful 2xx response
response.status  // for example, 200, 404, or 500
```

The second line reads the response body and converts JSON text into JavaScript values. A response body can be read only once, and reading it may take time, which is why `response.json()` also uses `await`.

For example, JSON like this:

```json
[
  {"id": "a1", "title": "Read", "complete": false}
]
```

becomes an array containing one JavaScript object. Its values can be read with dot notation:

```javascript
item.id
item.title
item.complete
```

For this todo app, a successful local `GET /tasks` response currently has this shape (the UUID values change when the in-memory backend restarts):

```json
[
  {
    "uid": "a4fa8d9a-3035-465c-8120-331b3f8cee36",
    "title": "buy milk",
    "description": "",
    "is_complete": false
  },
  {
    "uid": "925e9c2d-334b-46bd-a2c8-ffeed566b146",
    "title": "set up internet",
    "description": "",
    "is_complete": false
  }
]
```

## Arrays And `for...of`

An array is an ordered collection of values. A `for...of` loop runs once for each value in an array:

```javascript
for (const item of items) {
    // item means the current object during this loop run
}
```

Use this when each data object should produce one repeated piece of page content, such as a task row, product card, or search result.

## The DOM: Changing The Page

The browser represents an HTML page as the DOM (Document Object Model). JavaScript can find, create, fill, and attach DOM elements.

```javascript
const item = document.createElement("li");
item.textContent = "Read";
itemList.append(item);
```

These steps are distinct:

1. `createElement` makes an element in memory.
2. `textContent` gives it visible text safely.
3. `append` places it inside another element, making it appear in the page.

An element created but not appended exists only in memory and is not visible to the visitor.

`innerHTML = ""` removes all existing HTML inside an element. It is useful before rendering a fresh list, but it also removes any static placeholder children.

## HTML Attributes From JavaScript

JavaScript can add custom HTML `data-*` attributes through `dataset`:

```javascript
item.dataset.complete = false;
```

The browser produces the HTML attribute:

```html
<li data-complete="false"></li>
```

`dataset.isComplete` maps to `data-is-complete`. The browser handles the camelCase-to-hyphenated-name conversion. These attributes can preserve useful data on the element and can be selected by CSS.

## Rendering States And Error Handling

A data-driven page should communicate more than its successful result:

```text
Loading: request is in progress.
Empty: request succeeded, but the returned array has no items.
Error: the request or response failed.
Success: render the returned items.
```

Use `try` for the normal request/rendering work and `catch` for an error:

```javascript
try {
    const response = await fetch(apiUrl);

    if (!response.ok) {
        throw new Error("Request failed");
    }
} catch (error) {
    console.error(error);
}
```

`fetch` rejects for network problems, but an HTTP error response such as `404` or `500` still produces a Response. Check `response.ok`, then use `throw` to send unsuccessful responses to `catch`.

## Cross-Origin Requests (CORS)

Browsers treat different protocol, host, or port combinations as different origins. A page at `http://127.0.0.1:5500` requesting an API at `http://127.0.0.1:8000` is making a cross-origin request because the ports differ.

The browser allows the frontend to read that response only when the API explicitly grants permission with CORS headers. The API should allow only the origins and HTTP methods the frontend actually needs.

## Applying This To The Todo App

The current frontend uses this pattern to read `GET /tasks`, create a list item for each returned task, and preserve each task's identifier and completion value as `data-*` attributes. It currently displays tasks only; changing tasks is a later feature.
