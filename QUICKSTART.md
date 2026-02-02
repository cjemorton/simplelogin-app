# 🚀 QUICK START - Upstream Contribution

> **TL;DR**: You have a fix for SimpleLogin. Here's how to contribute it back in 5 minutes.

## Your Fix
```diff
- Remove: ignore-init-module-imports = true
+ From: pyproject.toml (line 111)
```

## 3-Step Process

### Step 1: Create Issue (2 min)
1. Go to: https://github.com/simple-login/app/issues/new
2. Title: `Remove deprecated ignore-init-module-imports from Ruff configuration`
3. Body: Copy everything from `UPSTREAM_ISSUE.md`
4. Submit ✓

### Step 2: Create Branch (1 min)
```bash
git fetch upstream master
git checkout -b fix/remove-deprecated-ruff-option upstream/master
git diff master upstream/master -- pyproject.toml | git apply
git add pyproject.toml
git commit -m "Remove deprecated ignore-init-module-imports from Ruff config

Fixes #<ISSUE_NUMBER_FROM_STEP_1>"
git push origin fix/remove-deprecated-ruff-option
```

### Step 3: Create PR (2 min)
1. Go to: https://github.com/simple-login/app
2. Click "Compare & pull request" banner
3. Title: `Remove deprecated ignore-init-module-imports from Ruff configuration`
4. Body: Copy everything from `UPSTREAM_PR.md`
5. Submit ✓

## Done! 🎉

**Your contribution is submitted!** Now:
- ✅ Wait for CI checks to pass
- ✅ Respond to any maintainer feedback
- ✅ Celebrate becoming a SimpleLogin contributor!

---

## Need More Details?

📖 Full documentation: `README_UPSTREAM_CONTRIBUTION.md`  
📋 Complete guide: `CONTRIBUTING_TO_UPSTREAM.md`  
📊 Visual overview: `VISUAL_GUIDE.md`

---

**Ready? Start with Step 1!** ⬆️
