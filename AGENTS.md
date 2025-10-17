# AGENTS.md - Terraform Version Update Scripts

This repository contains two Python scripts for updating Terraform module and repository versions in `.tf` files. This document provides comprehensive instructions for AI agents working with these scripts.

## 📁 Repository Structure

```
.
├── update-tf-submodule.py      # Updates specific module subdirectories
├── update-tf-repo.py           # Updates entire repository references
├── tests.tf                    # Test file for submodule script
├── tests.tf.original           # Original test cases for submodule script
├── repo-tests.tf               # Test file for repository script
├── repo-tests.tf.original      # Original test cases for repository script
└── AGENTS.md                   # This documentation file
```

## 🎯 Script Overview

### `update-tf-submodule.py`
**Purpose**: Updates version references for specific module subdirectories within git repositories.

**Key Behavior**:
- Matches exact module paths (e.g., `test` matches `//test` but NOT `//test/example`)
- Preserves subdirectory structure when updating versions
- Handles nested paths correctly (e.g., `test/example` matches `//test/example`)

### `update-tf-repo.py`
**Purpose**: Updates ALL version references for a specific git repository, regardless of subdirectories.

**Key Behavior**:
- Matches repository names with `.git` extension
- Updates all references to the repository regardless of subdirectory paths
- Preserves existing subdirectory paths while updating versions

## 🚀 Usage Examples

### Submodule Script
```bash
# Update specific module 'test' to version 'v2.0.0'
python3 update-tf-submodule.py test v2.0.0

# Update nested module 'test/example' to version 'v1.5.0'
python3 update-tf-submodule.py test/example v1.5.0

# Update in specific directory
python3 update-tf-submodule.py mymodule v3.0.0 --path ./terraform
```

### Repository Script
```bash
# Update all references to 'repo.git' to version 'v3.0.0'
python3 update-tf-repo.py repo v3.0.0

# Update specific repository in directory
python3 update-tf-repo.py my-modules v1.0.0 --path ./infrastructure
```

## 🧪 Testing Methodology

### Test File Structure
Each script has corresponding test files:
- `*.original` - Master copy with original test cases (NEVER modify these)
- `*.tf` - Working copy for testing (gets reset from .original between tests)

### Test Workflow
1. **Reset test file**: `cp tests.tf.original tests.tf`
2. **Run script**: `python3 update-tf-submodule.py <args>`
3. **Verify results**: Check which modules were updated vs. ignored
4. **Repeat**: Reset and test different scenarios

### Test Case Documentation
Test files include inline comments indicating expected behavior:
```terraform
# Should be matched with `test`
module "example3" {
  source = "git@github.com:example/repo.git//test"
}

# Should NOT be matched with `test` (matches test/example)
module "example5" {
  source = "git@github.com:example/repo.git//test/example"
}
```

## 🔧 Technical Implementation Details

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

## 🐛 Common Issues and Debugging

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

## 📋 Agent Instructions for Modifications

### When Modifying Scripts:

1. **Always test both positive and negative cases**
   - Verify intended matches work correctly
   - Verify unintended matches are ignored

2. **Use the test files for validation**
   - Reset from `.original` before each test
   - Check multiple scenarios (different module/repo names)

3. **Preserve existing functionality**
   - Don't break backward compatibility
   - Maintain support for all URL formats

4. **Update documentation**
   - Modify docstrings if behavior changes
   - Update this AGENTS.md if new patterns emerge

### When Adding New Features:

1. **Create comprehensive test cases first**
   - Add new examples to `.original` files
   - Document expected behavior in comments

2. **Test edge cases**
   - Empty directories, missing files
   - Malformed URLs, special characters
   - Very long paths, unicode characters

3. **Maintain performance**
   - Scripts should handle large codebases efficiently
   - Avoid unnecessary file reads/writes

## 🎯 Script-Specific Behaviors

### `update-tf-submodule.py` Specifics

**Exact Path Matching**:
- `test` matches `//test` but NOT `//test/example`
- `test/example` matches `//test/example` but NOT `//test`
- Path boundaries are enforced to prevent partial matches

**Use Cases**:
- Updating specific microservice modules
- Selective version bumps for particular components
- Maintaining different versions for different module paths

### `update-tf-repo.py` Specifics

**Repository-Wide Updates**:
- `repo` matches ALL references to `repo.git`
- Ignores subdirectory paths completely
- Updates entire repository to same version

**Use Cases**:
- Bulk version updates across all modules in a repository
- Security patches that affect entire repositories
- Major version migrations

## 🔍 Verification Commands

After running either script, verify results with:

```bash
# Check what was updated
grep -n "?ref=" tests.tf

# Compare with original
diff tests.tf.original tests.tf

# Verify specific patterns
grep -E "repo\.git.*\?ref=" tests.tf
```

## 📚 Additional Resources

### Regular Expression Testing
Test regex patterns at: https://regex101.com/
- Use Python flavor
- Test with actual Terraform source examples

### Terraform Module Documentation
- [Terraform Module Sources](https://www.terraform.io/docs/modules/sources.html)
- [Git Repository Sources](https://www.terraform.io/docs/modules/sources.html#git-repositories)

### Best Practices
- Always backup important `.tf` files before running scripts
- Test in development environments first
- Use version control to track changes
- Document version update reasons in commit messages

---

*This documentation is maintained for AI agents working with the Terraform version update scripts. Keep it updated as scripts evolve.*
