# Cookbook

Personal recipe collection, published with GitHub Pages.

## How it works

| File | What it is |
|---|---|
| `recipes/*.md` | One file per recipe. The source of truth. |
| `recipes/_TEMPLATE.md` | Copy this to start a new recipe. Skipped by the build. |
| `build.py` | Turns the recipe files into `recipes.js`. |
| `index.html` | The website. Reads `recipes.js`. |

## Add a recipe

1. Copy `recipes/_TEMPLATE.md` to `recipes/<short-name>.md` (lowercase, dashes, e.g. `lemon-pasta.md`).
2. Fill in the top block. `score` is 1-5, `make_again` is yes/no, `tags` are comma-separated.
3. `python3 build.py`
4. Open `index.html` in a browser to check it.
5. Publish (below).

## Publish to GitHub

One-time setup is in the section after this. Every update afterwards is three commands:

```
git add .
git commit -m "Add lemon pasta"
git push
```

The site updates about a minute after the push.

## One-time GitHub setup

1. Create a free account at github.com (personal email, not work).
2. Tell git who you are:
   `git config --global user.name "Your Name"`
   `git config --global user.email "you@example.com"`
3. Install the GitHub command line tool and log in:
   `brew install gh`
   `gh auth login` (choose GitHub.com, HTTPS, log in with a web browser)
4. From this folder, create the repo and push:
   `gh repo create cookbook --public --source . --push`
5. Turn on Pages: on github.com open the repo, Settings, Pages, Source "Deploy from a branch", branch `main`, folder `/ (root)`, Save.
6. Your link: `https://<your-username>.github.io/cookbook/`

Note: GitHub Pages on a free account needs a **public** repo, so anyone can see the recipe files.
