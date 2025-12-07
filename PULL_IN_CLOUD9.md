# How to Pull Latest Changes in Cloud9

Quick guide to pull the latest updates from GitHub in your Cloud9 environment.

---

## Steps to Pull Latest Changes

### Step 1: Open Cloud9 Terminal

1. Open your **Cloud9 IDE**
2. The terminal is at the bottom of the screen
3. If not visible, go to **Window** → **New Terminal**

### Step 2: Navigate to Project Directory

```bash
# Navigate to your MyPOS project directory
cd ~/MyPOS
```

**Note**: If you haven't cloned the repository yet, see the "First Time Setup" section below.

### Step 3: Check Current Status

```bash
# Check if you have any uncommitted changes
git status
```

**If you have uncommitted changes**, you have two options:

**Option A: Save your changes first (recommended)**
```bash
# Save your local changes
git add .
git commit -m "Save local changes before pull"
```

**Option B: Discard local changes (if you don't need them)**
```bash
# Discard all local changes
git reset --hard HEAD
```

### Step 4: Pull Latest Changes

```bash
# Pull the latest changes from GitHub
git pull origin main
```

**If you get "divergent branches" error**, use one of these:

**Option A: Merge (Recommended - safer)**
```bash
git pull origin main --no-rebase
```

**Option B: Rebase (Creates cleaner history)**
```bash
git pull origin main --rebase
```

**Option C: Set default behavior (one-time setup)**
```bash
# Set merge as default (recommended)
git config pull.rebase false
git pull origin main
```

**If you get a merge conflict**, you'll see a message like:
```
Auto-merging filename.py
CONFLICT (content): Merge conflict in filename.py
```

**To resolve conflicts:**
1. Open the conflicted file in Cloud9
2. Look for conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
3. Edit the file to resolve the conflict
4. Save the file
5. Run:
   ```bash
   git add .
   git commit -m "Resolve merge conflicts"
   ```

### Step 5: Verify Changes

```bash
# Check what files were updated
git log --oneline -5

# List changed files
git diff HEAD~1 --name-only
```

### Step 6: Restart Django Server (if running)

If your Django server is running, you need to restart it:

1. **Stop the server**: Press `Ctrl+C` in the terminal where the server is running
2. **Start it again**:
   ```bash
   python3 manage.py runserver 0.0.0.0:8080
   ```

---

## First Time Setup (If You Haven't Cloned Yet)

If you haven't cloned the repository to Cloud9 yet:

```bash
# Navigate to home directory
cd ~

# Clone the repository
git clone https://github.com/x23379014/MyPOS.git

# Navigate into the project
cd MyPOS

# Install dependencies
pip3 install -r requirements.txt --user

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Initialize AWS resources
python3 manage.py init_aws

# Start the server
python3 manage.py runserver 0.0.0.0:8080
```

---

## Quick Pull Command (One-Liner)

If you're already in the project directory and have no local changes:

```bash
cd ~/MyPOS && git pull origin main
```

---

## Troubleshooting

### Issue: "Your branch is behind 'origin/main'"

**Solution**: This is normal. Just run:
```bash
git pull origin main
```

### Issue: "divergent branches" or "Need to specify how to reconcile"

**Solution**: Your local and remote branches have diverged. Use one of these:

**Option 1: Merge (Recommended)**
```bash
git pull origin main --no-rebase
```

**Option 2: Rebase**
```bash
git pull origin main --rebase
```

**Option 3: Set default and pull**
```bash
git config pull.rebase false
git pull origin main
```

**If you get merge conflicts after this:**
1. Open the conflicted files in Cloud9
2. Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
3. Edit to resolve conflicts
4. Save files
5. Run: `git add . && git commit -m "Resolve merge conflicts"`

### Issue: "Please commit your changes or stash them"

**Solution**: You have uncommitted changes. Either:
- **Commit them**: `git add . && git commit -m "Your message"`
- **Stash them**: `git stash` (then `git stash pop` after pull to restore)

### Issue: "Merge conflict"

**Solution**: 
1. Open the conflicted file
2. Resolve the conflict manually
3. Run: `git add . && git commit -m "Resolve conflicts"`

### Issue: "Repository not found" or "Permission denied"

**Solution**: 
- Make sure the repository URL is correct: `https://github.com/x23379014/MyPOS.git`
- If it's a private repo, you may need to authenticate with GitHub

### Issue: "fatal: not a git repository"

**Solution**: You're not in the project directory. Run:
```bash
cd ~/MyPOS
```

---

## What Changed in Latest Update?

The latest update includes:

✅ **Fixed customer name display** - Customer names now show correctly in transactions instead of "Unknown"
✅ **Improved SNS error handling** - Better error messages for notification failures
✅ **New architecture diagrams** - Added architecture documentation
✅ **SNS troubleshooting guide** - Helpful guide for debugging SNS issues
✅ **Updated deployment docs** - Enhanced ELB deployment instructions

---

## After Pulling - Verify Everything Works

1. **Check the application**:
   ```bash
   python3 manage.py runserver 0.0.0.0:8080
   ```

2. **Test customer name in transactions**:
   - Create a new transaction
   - Check that customer name displays correctly (not "Unknown")

3. **Verify SNS notifications**:
   - Create a transaction
   - Check for improved error messages if notification fails

---

## Quick Reference

```bash
# Navigate to project
cd ~/MyPOS

# Pull latest changes
git pull origin main

# Check status
git status

# View recent commits
git log --oneline -5

# Restart server
python3 manage.py runserver 0.0.0.0:8080
```

---

**That's it!** Your Cloud9 environment is now up to date with the latest changes from GitHub. 🚀

