# Git Basics Used In This Project

Git tracks changes to project files over time. A commit is a saved snapshot of a meaningful project state.

## Working Tree, Staging Area, And Commit

Git has three important states:

- Working tree: files as they currently exist on disk.
- Staging area: changes selected for the next commit.
- Commit: saved snapshot in Git history.

Typical flow:

```bash
git status
git add <files>
git commit -m "Message"
```

What to remember: editing a file does not automatically put it into a commit. You stage changes first, then commit them.

## Checking Status

```bash
git status --short
```

Shows a compact view of changed files.

Common symbols:

- `M`: modified file.
- `A`: added file.
- `D`: deleted file.
- `??`: untracked file.

Example:

```text
 M AGENTS.md
?? backend/Dockerfile
```

Meaning:

- `AGENTS.md` is tracked and modified.
- `backend/Dockerfile` is new and not tracked yet.

## Seeing What Changed

```bash
git diff
```

Shows unstaged changes.

```bash
git diff --cached
```

Shows staged changes that will be included in the next commit.

```bash
git diff --stat
```

Shows a summary of changed files and line counts.

What to remember: inspect changes before committing so the commit contains what you intend.

## Staging Changes

```bash
git add AGENTS.md LEARNINGS.md backend/Dockerfile backend/.dockerignore
```

Stages specific files.

```bash
git add -A
```

Stages all changes, including additions, modifications, and deletions.

Tradeoff:

- specific files are safer when changes are mixed;
- `git add -A` is convenient when all current changes belong in the same commit.

## Committing Changes

```bash
git commit -m "Dockerize FastAPI backend"
```

Creates a commit with a message.

Good commit messages are short and describe the meaningful project change.

Examples from this project:

```text
Build initial FastAPI todo backend
Dockerize FastAPI backend
```

What to remember: a commit should represent a coherent checkpoint, not every tiny edit.

## Clean Working Tree

After committing, this should ideally show no output:

```bash
git status --short
```

That means there are no uncommitted changes.

Why it matters:

- easier to see what changes next;
- safer before starting a new project stage;
- easier to debug or roll back later.

## Branches

A branch is a movable pointer to a line of work.

Common commands:

```bash
git branch
```

List local branches.

```bash
git switch -c feature/frontend
```

Create and switch to a new branch.

```bash
git switch main
```

Switch back to `main`.

Why branches matter:

- you can work on a feature without disturbing `main`;
- experiments can be isolated;
- teams commonly use branches for pull requests.

What to remember: commits belong to the branch you are currently on.

## Fetch Vs Pull

Remote repositories, such as GitHub, can have commits your local repo does not know about yet.

```bash
git fetch
```

Downloads information and commits from the remote, but does not merge them into your current branch.

```bash
git pull
```

Fetches remote changes and then integrates them into your current branch.

Mental model:

```text
fetch = look at what changed remotely
pull = fetch + update my current branch
```

Why fetch is useful:

- safer when you want to inspect remote changes first;
- avoids immediately modifying your working branch.

What to remember: `git pull` changes your current branch; `git fetch` only updates your view of the remote.

## Stash

`git stash` temporarily saves uncommitted work so you can return to a clean working tree.

Example:

```bash
git stash
```

Saves tracked changes and reverts the working tree.

```bash
git stash list
```

Shows saved stashes.

```bash
git stash pop
```

Reapplies the latest stash and removes it from the stash list.

```bash
git stash apply
```

Reapplies the latest stash but keeps it in the stash list.

Why stash is useful:

- you need to switch branches but have unfinished work;
- you want to quickly test something from a clean state;
- you need to pull changes but your local edits would conflict.

Important caution: stash is temporary storage, not a substitute for commits. If work is meaningful, commit it.

## Ignored Files

`.gitignore` tells Git which generated or local files should not be tracked.

Examples:

```text
.venv/
__pycache__/
*.pyc
```

Why this matters:

- virtual environments are machine-specific;
- Python cache files are generated;
- committing generated files creates noise and portability problems.

If a file is already tracked, adding it to `.gitignore` does not automatically untrack it. `.gitignore` mainly prevents new untracked files from being added.

What to remember: commit source/config/lock files; ignore generated machine-local output.

