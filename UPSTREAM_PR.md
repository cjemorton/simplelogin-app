# Pull Request: Remove deprecated `ignore-init-module-imports` from Ruff configuration

## Summary

This PR removes the deprecated `ignore-init-module-imports` configuration option from Ruff's settings in `pyproject.toml`, eliminating unnecessary deprecation warnings and aligning with Ruff's current best practices.

## Problem

The current Ruff configuration contains a deprecated option that generates warnings:

```toml
[tool.ruff.lint]
ignore-init-module-imports = true
```

This option is no longer necessary as Ruff now correctly handles imports in `__init__.py` files by default. The deprecation warning appears during any Ruff operation (linting, formatting, checking), creating noise in development workflows and CI/CD pipelines.

## Changes

This PR makes a single, surgical change:

**File**: `pyproject.toml`

```diff
 [tool.ruff]
 exclude = [".venv", "migrations", "app/events/generated"]
 [tool.ruff.lint]
-ignore-init-module-imports = true
```

**Lines changed**: 1 deletion
**Files changed**: 1

## Why This Change is Needed

1. **Eliminates deprecation warnings**: The current configuration generates warnings that clutter development output and CI/CD logs
2. **Prevents future breaking changes**: When Ruff removes this option entirely in a future release, it could cause configuration errors
3. **Follows best practices**: Ruff documentation indicates this option is obsolete and should be removed
4. **No functional impact**: Removing this option does not change linting or formatting behavior, as Ruff's default behavior is now correct

## Testing

This change has been tested and verified:

- ✅ No deprecation warnings are generated when running Ruff commands
- ✅ Ruff linting continues to work correctly
- ✅ Ruff formatting continues to work correctly
- ✅ No changes to actual linting rules or formatting output
- ✅ All existing tests pass
- ✅ The application builds and runs normally

### Commands tested:
```bash
ruff check .
ruff format --check .
# No warnings related to deprecated options
```

## Impact

- **Risk level**: Minimal - This is a configuration cleanup with no behavioral changes
- **Breaking changes**: None
- **Backward compatibility**: Fully maintained
- **Performance**: No impact
- **Security**: No impact

## Additional Notes

- This is a maintenance improvement that keeps the project's configuration current with Ruff's evolution
- The change aligns with Ruff's philosophy of sensible defaults
- Similar deprecation warnings may appear in other projects using Ruff, making this a valuable reference

## References

- Ruff documentation on configuration options
- Ruff's handling of `__init__.py` imports has been improved to work correctly by default
- This change follows the principle of removing unnecessary configuration when tools provide good defaults

---

**Checklist:**
- [x] Code follows the project's style guidelines
- [x] Change has been tested locally
- [x] No breaking changes introduced
- [x] Documentation updated (if needed - N/A for this config change)
- [x] PR description clearly explains the change and rationale
