# Contributing Your Changes Back to SimpleLogin Upstream

This document provides guidance on how to contribute the Ruff configuration fix from your fork back to the upstream SimpleLogin repository.

## Overview

Your fork contains an important fix that removes a deprecated Ruff configuration option (`ignore-init-module-imports`). This change would benefit the entire SimpleLogin project and community.

## What Changed

**Repository**: Your fork at `cjemorton/simplelogin-app`  
**Upstream**: Original repository at `simple-login/app`

**Change Summary**:
- **File modified**: `pyproject.toml`
- **Change type**: Remove deprecated configuration option
- **Lines changed**: 1 deletion
- **Commits**: 1 merged PR (#10)

## Steps to Contribute Upstream

### 1. Verify Your Change is Current

First, ensure your master branch has the latest changes from upstream and that the issue still exists there:

```bash
# Fetch the latest from upstream
git fetch upstream master

# Check if the deprecated option still exists in upstream
git show upstream/master:pyproject.toml | grep "ignore-init-module-imports"
```

If the grep command returns a result, the fix is still needed. ✅

### 2. Create an Issue in the Upstream Repository

Navigate to https://github.com/simple-login/app/issues and create a new issue.

**Use the content from**: `UPSTREAM_ISSUE.md`

**Issue Title**: `Remove deprecated ignore-init-module-imports from Ruff configuration`

**Labels to add** (if available):
- `maintenance`
- `good first issue` (it's a simple fix)
- `dependencies` or `tooling`

### 3. Create a Branch for Your Contribution

Create a clean branch from the latest upstream master:

```bash
# Ensure you're up to date with upstream
git fetch upstream master

# Create a new branch from upstream/master
git checkout -b fix/remove-deprecated-ruff-option upstream/master

# Cherry-pick your fix (adjust the commit hash as needed)
# Or manually apply the change from your master branch
git diff master upstream/master -- pyproject.toml | git apply

# Commit the change
git add pyproject.toml
git commit -m "Remove deprecated ignore-init-module-imports from Ruff config

Ruff emits a deprecation warning for the ignore-init-module-imports
option, which will be removed in a future release. Ruff now correctly
handles imports in __init__.py files by default, making this
configuration unnecessary.

This change:
- Eliminates deprecation warnings during Ruff operations
- Aligns with Ruff's current best practices
- Prevents potential issues when the option is fully removed

Fixes #<ISSUE_NUMBER>"
```

### 4. Push Your Branch

Push the branch to your fork:

```bash
# Push to your fork
git push origin fix/remove-deprecated-ruff-option
```

### 5. Create the Pull Request

1. Go to https://github.com/simple-login/app
2. You should see a banner suggesting to create a PR from your recently pushed branch
3. Click "Compare & pull request"

**Use the content from**: `UPSTREAM_PR.md`

**PR Title**: `Remove deprecated ignore-init-module-imports from Ruff configuration`

**Important PR Settings**:
- Base repository: `simple-login/app`
- Base branch: `master` (or their default branch)
- Head repository: `cjemorton/simplelogin-app`
- Compare branch: `fix/remove-deprecated-ruff-option`

**Additional PR Details**:
- Reference the issue you created: "Fixes #<ISSUE_NUMBER>"
- Check "Allow edits by maintainers" (if you're comfortable with that)

### 6. Follow Up

After submitting the PR:

1. **Watch for CI/CD results**: The upstream repository likely has automated tests. Ensure they pass.
2. **Respond to feedback**: Maintainers may have questions or suggestions. Be responsive and collaborative.
3. **Be patient**: Open source maintainers are often volunteers. It may take time for them to review.
4. **Check for conflicts**: If the upstream merges other changes, you may need to rebase your PR.

## Expected Outcome

This is a straightforward maintenance fix with:
- ✅ Minimal risk
- ✅ Clear benefit (removes deprecation warnings)
- ✅ No breaking changes
- ✅ Alignment with best practices

The PR should be well-received as it improves the project's code quality and prevents future issues.

## Alternative: Just Submit an Issue

If you prefer not to create the PR yourself, you can submit just the issue (using `UPSTREAM_ISSUE.md`). Someone else from the community or the maintainers can then implement the fix. Your contribution of identifying and documenting the issue is still valuable!

## Communication Tips

- **Be respectful**: The maintainers are giving their time to maintain this project
- **Be clear**: Your issue and PR descriptions should be comprehensive (we've prepared them for you!)
- **Be collaborative**: If they suggest changes, be open to feedback
- **Be patient**: Response times vary in open source projects

## Questions?

If you have questions about contributing to SimpleLogin:
- Check their `CONTRIBUTING.md` file in the upstream repository
- Look at recently merged PRs to understand their process
- Ask in the PR comments or issue tracker

## Summary

You have:
1. ✅ `UPSTREAM_ISSUE.md` - Ready to copy/paste into a new issue
2. ✅ `UPSTREAM_PR.md` - Ready to copy/paste into a new pull request
3. ✅ `CONTRIBUTING_TO_UPSTREAM.md` (this file) - Step-by-step guide

Your change is valuable and the SimpleLogin project will benefit from your contribution. Good luck! 🎉
