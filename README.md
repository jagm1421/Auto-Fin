# 📄 Document question answering template

A simple Streamlit app that answers questions about an uploaded document via OpenAI's GPT-3.5.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://document-question-answering-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

# 🧠 Git Pull & Push Cheat Sheet

## ✅ Check Current Git Status
```bash
git status
```

### 🔄 1. Pull Latest Changes from GitHub
```bash
git pull origin main
```
### ➡️ For a cleaner history, use rebase:
```bash
git pull origin main --rebase
```
### 💾 2. Stage & Commit Your Changes
```bash
git add .
git commit -m "Your commit message"
```
### 📤 3. Push Local Commits to GitHub
```bash
git push origin main
```
## 🧰 Useful Git Commands
| Action                             | Command                                |
|------------------------------------|----------------------------------------|
| Show local changes                 | `git status`                           |
| View commit log (one-liners)       | `git log --oneline`                    |
| Save uncommitted changes           | `git stash`                            |
| Reapply stashed changes            | `git stash pop`                        |
| See unstaged changes               | `git diff`                             |
| See staged changes                 | `git diff --cached`                    |
| Undo last commit (keep changes)    | `git reset --soft HEAD~1`              |
| Discard all local changes ⚠️       | `git reset --hard`                     |


# 🧪 Typical Workflow

## Start
```bash
git status
git pull origin main --rebase
```
## make edits...
```bash
git add .
git commit -m "Updated chart logic"
git push origin main
```

## 🚨 Pro Tips
Always git pull before starting new work.

Use --rebase to avoid unnecessary merge commits.

Commit often with meaningful messages.

---