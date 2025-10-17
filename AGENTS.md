# AGENTS.md - Terraform Version Update Scripts

Repository contains two Python scripts for updating Terraform module and repository versions in `.tf` files.

## Repository Structure

```
├── update-tf-submodule.py      # Updates specific module subdirectories
├── update-tf-repo.py           # Updates entire repository references
├── tests.tf                    # Test file for submodule script
├── tests.tf.original           # Original test cases for submodule script
├── repo-tests.tf               # Test file for repository script
├── repo-tests.tf.original      # Original test cases for repository script
```

## Script Specifications

### `update-tf-submodule.py`
Updates version references for specific module subdirectories within git repositories.

**Behavior**:
- Matches exact module paths: `test` matches `//test` but NOT `//test/example`
- Preserves subdirectory structure when updating versions
- Handles nested paths: `test/example` matches `//test/example`

### `update-tf-repo.py`
Updates ALL version references for a specific git repository, regardless of subdirectories.

**Behavior**:
- Matches repository names with `.git` extension
- Updates all references to the repository regardless of subdirectory paths
- Preserves existing subdirectory paths while updating versions

## Usage

```bash
# Submodule script
python3 update-tf-submodule.py test v2.0.0
python3 update-tf-submodule.py test/example v1.5.0
python3 update-tf-submodule.py mymodule v3.0.0 --path ./terraform

# Repository script
python3 update-tf-repo.py repo v3.0.0
python3 update-tf-repo.py my-modules v1.0.0 --path ./infrastructure
```

## Testing

Test files:
- `*.original` - Master copy with test cases (DO NOT modify)
- `*.tf` - Working copy for testing (reset from .original between tests)

Workflow:
1. Reset: `cp tests.tf.original tests.tf`
2. Run: `python3 update-tf-submodule.py <args>`
3. Verify: Check results
4. Repeat for different scenarios

## Technical Implementation

### URL Pattern Matching

Both scripts use regex patterns to match Terraform source URLs:

**Submodule Pattern**:
```python
r'(source\s*=\s*"[^"]+//)(' + re.escape(module_name) + r')(\?ref=[^"]*|/[^"]*|)(")'
```

**Repository Pattern**:
```python
r'(source\s*=\s*"[^"]*/)(' + re.escape(repo_name) + r'\.git)(//[^"?]*|)(\?ref=[^"]*|)(")'
```

### Supported URL Formats

Both scripts support:
- SSH URLs: `git@github.com:org/repo.git`
- HTTPS URLs: `https://github.com/org/repo.git`
- URLs with subdirectories: `git@github.com:org/repo.git//path/to/module`
- URLs with existing versions: `git@github.com:org/repo.git?ref=v1.0.0`

### Version Parameter Handling

The scripts handle these transformations:
```terraform
# Before
source = "git@github.com:org/repo.git"
source = "git@github.com:org/repo.git?ref=v1.0.0"
source = "git@github.com:org/repo.git//modules"
source = "git@github.com:org/repo.git//modules?ref=v1.0.0"

# After (with version v2.0.0)
source = "git@github.com:org/repo.git?ref=v2.0.0"
source = "git@github.com:org/repo.git?ref=v2.0.0"
source = "git@github.com:org/repo.git//modules?ref=v2.0.0"
source = "git@github.com:org/repo.git//modules?ref=v2.0.0"
```

## Common Issues

### Issue: Nested Subdirectories Not Updating Correctly

**Problem**: When updating module `test`, both `//test` and `//test/example` get updated.

**Root Cause**: Regex pattern too permissive or path validation logic incorrect.

**Debug Steps**:
1. Check the regex pattern for exact boundary matching
2. Verify the `replace_match` function validates full paths
3. Test with both `test` and `test/example` to ensure selectivity

### Issue: Duplicate `?ref=` Parameters

**Problem**: Output contains `//path?ref=v1?ref=v2` instead of `//path?ref=v2`.

**Root Cause**: Replacement logic not properly handling existing version parameters.

**Solution**: Ensure the replacement function splits on `?ref=` and only keeps the path portion.

### Issue: Partial Repository Name Matches

**Problem**: Searching for `repo` matches `repo-extended.git`.

**Root Cause**: Regex not enforcing exact repository name boundaries.

**Solution**: Use `re.escape()` and ensure `.git` suffix is explicitly matched.

## Agent Modification Requirements

### When modifying scripts:
1. Test both positive and negative cases
2. Use test files for validation - reset from `.original` before each test
3. Preserve backward compatibility and all URL format support
4. Update docstrings and this file if behavior changes

### When adding features:
1. Create test cases in `.original` files first
2. Test edge cases: empty dirs, malformed URLs, special chars
3. Maintain performance for large codebases

## Script-Specific Behaviors

### `update-tf-submodule.py` Specifics

**Exact Path Matching**:
- `test` matches `//test` but NOT `//test/example`
- `test/example` matches `//test/example` but NOT `//test`
- Path boundaries enforced to prevent partial matches

### `update-tf-repo.py` Specifics

**Repository-Wide Updates**:
- `repo` matches ALL references to `repo.git`
- Ignores subdirectory paths
- Updates entire repository to same version

## Verification

Commands to verify script results:

```bash
# Check what was updated
grep -n "?ref=" tests.tf

# Compare with original
diff tests.tf.original tests.tf

# Verify specific patterns
grep -E "repo\.git.*\?ref=" tests.tf
```

---

*This documentation is for AI agents working with Terraform version update scripts.*
