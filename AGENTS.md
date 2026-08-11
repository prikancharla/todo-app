# AGENTS.md

## Project Purpose

This repo is a hands-on learning project for software engineering fundamentals through a todo app.

Learning path:

1. Design Python OOP classes.
2. Build a FastAPI backend.
3. Deploy the FastAPI backend.
4. Build a frontend to learn html, javascript and css.
5. Deploy the frontend.
6. Build a simple React frontend and replace the earlier frontend.
7. Integrate SQL Server persistence.
8. CI/CD.
9. Maybe add an assistant service that can perform todo add/edit operations.

## Teaching Style

When the user is learning a new technology:

- work in small, sequential steps;
- explain the goal of each step before asking the user to make the change;
- let the user write the code unless they explicitly ask for code or an implementation;
- pause after each step to review their result before continuing.

## Learning Journal

Maintain `LEARNINGS.md` and the `study-guide/` folder as a beginner-friendly study guide.

`LEARNINGS.md` is the index and current project snapshot. Detailed concept notes live in topic files under `study-guide/`.

The guide should help the user return days or weeks later and understand:

- what was learned;
- why design choices were made;
- how concepts appear in this project;
- what commands, files, and runtime behavior matter;
- what mistakes, confusions, or tradeoffs came up.

It is not a changelog, transcript, or exhaustive action log.

## When To Update The Study Guide

Update the study guide when the user asks for review or feedback, moves into a new concept, expresses confusion, debugs an issue, makes a meaningful design/tooling decision, or receives an explanation that would be useful to revisit later.

Make that update during the same task without waiting for a reminder. Keep it concise and reusable: capture the concept, why it matters, and the smallest helpful example. Do not turn the guide into a record of a specific conversation, branch, commit, or session unless that detail is essential to the concept.

If a topic already exists, improve that topic file instead of creating a duplicate. If a topic has only been mentioned but not worked through, keep it short in `study-guide/deferred-topics.md`.

Keep `LEARNINGS.md` focused on navigation and the current project snapshot. Do not use subagents to edit study-guide files unless the user explicitly approves the proposed note changes first.

## Quality Bar For Notes

Before adding or changing a note, check that it:

- helps a beginner reconstruct the mental model later;
- is based on something the user actually encountered, asked about, debugged, or decided;
- is transferable beyond one exact line of code;
- explains why the idea matters in this project;
- includes a concrete command, code snippet, or file example when that would make the idea easier to remember.

Prefer concept-based organization over strict chronology. Avoid notes that only say a file/function/route was added.

## Command And Tool Notes

When documenting a command in the study guide, explain:

- where to run it from;
- what the command does;
- what files or state it reads;
- what files or state it writes or changes;
- why important flags/options are used;
- what result to expect;
- whether generated files should be committed or ignored.
