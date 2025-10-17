# Terraform Version Update Scripts

Two Python scripts to automate updating version references in your Terraform module sources. Perfect for managing git-based Terraform modules across large codebases.

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- Terraform files using git-based module sources

### Download & Use
```bash
# Clone or download the scripts
git clone <repository-url>
cd update-tf-submodule

# Make scripts executable (optional)
chmod +x update-tf-submodule.py update-tf-repo.py

# Update specific module subdirectories
python3 update-tf-submodule.py network v2.1.0

# Update entire repository references
python3 update-tf-repo.py my-terraform-modules v3.0.0
```

## 📋 What These Scripts Do

### `update-tf-submodule.py` - Surgical Module Updates
Updates **specific module paths** within git repositories. Use when you want to update only certain modules while leaving others unchanged.

**Example**: Update only the `network` module to v2.1.0, but leave `storage` and `compute` modules at their current versions.

### `update-tf-repo.py` - Repository-Wide Updates
Updates **all references** to a git repository regardless of which modules/subdirectories are used. Use for repository-wide version bumps.

**Example**: Update every reference to `my-terraform-modules.git` to v3.0.0, whether it's using `//network`, `//storage`, `//compute`, or any other subdirectory.

## 🎯 Usage Examples

### Scenario 1: Update a Specific Module
You have a networking module that you want to update to v2.1.0, but other modules should stay at their current versions.

```bash
python3 update-tf-submodule.py network v2.1.0
```

**Before:**
```hcl
module "vpc" {
  source = "git@github.com:myorg/terraform-modules.git//network?ref=v2.0.0"
}

module "storage" {
  source = "git@github.com:myorg/terraform-modules.git//storage?ref=v1.5.0"
}
```

**After:**
```hcl
module "vpc" {
  source = "git@github.com:myorg/terraform-modules.git//network?ref=v2.1.0"  # ✅ Updated
}

module "storage" {
  source = "git@github.com:myorg/terraform-modules.git//storage?ref=v1.5.0"  # ✅ Unchanged
}
```

### Scenario 2: Update Nested Module Paths
You have a nested module structure and want to update a specific nested path.

```bash
python3 update-tf-submodule.py aws/vpc v1.3.0
```

**Before:**
```hcl
module "aws_vpc" {
  source = "git@github.com:myorg/modules.git//aws/vpc?ref=v1.2.0"
}

module "aws_s3" {
  source = "git@github.com:myorg/modules.git//aws/s3?ref=v1.1.0"
}
```

**After:**
```hcl
module "aws_vpc" {
  source = "git@github.com:myorg/modules.git//aws/vpc?ref=v1.3.0"  # ✅ Updated
}

module "aws_s3" {
  source = "git@github.com:myorg/modules.git//aws/s3?ref=v1.1.0"  # ✅ Unchanged
}
```

### Scenario 3: Repository-Wide Version Bump
You've released v3.0.0 of your entire module repository and want to update all references across your codebase.

```bash
python3 update-tf-repo.py terraform-modules v3.0.0
```

**Before:**
```hcl
module "vpc" {
  source = "git@github.com:myorg/terraform-modules.git//network?ref=v2.5.0"
}

module "database" {
  source = "git@github.com:myorg/terraform-modules.git//database?ref=v2.3.0"
}

module "monitoring" {
  source = "git@github.com:myorg/terraform-modules.git//monitoring?ref=v2.1.0"
}
```

**After:**
```hcl
module "vpc" {
  source = "git@github.com:myorg/terraform-modules.git//network?ref=v3.0.0"  # ✅ Updated
}

module "database" {
  source = "git@github.com:myorg/terraform-modules.git//database?ref=v3.0.0"  # ✅ Updated
}

module "monitoring" {
  source = "git@github.com:myorg/terraform-modules.git//monitoring?ref=v3.0.0"  # ✅ Updated
}
```

## 🔧 Command Reference

### `update-tf-submodule.py`
```bash
python3 update-tf-submodule.py <module_path> <version> [--path <directory>]
```

**Parameters:**
- `module_path` - The module path after `//` (e.g., `network`, `aws/vpc`, `modules/compute`)
- `version` - The git tag/version to set (e.g., `v2.1.0`, `main`, `feature-branch`)
- `--path` - Directory to search (default: current directory)

**Examples:**
```bash
# Update network module to v2.1.0
python3 update-tf-submodule.py network v2.1.0

# Update nested AWS VPC module
python3 update-tf-submodule.py aws/networking/vpc v1.5.0

# Update in specific directory
python3 update-tf-submodule.py compute v2.0.0 --path ./environments/production
```

### `update-tf-repo.py`
```bash
python3 update-tf-repo.py <repo_name> <version> [--path <directory>]
```

**Parameters:**
- `repo_name` - Repository name without `.git` extension (e.g., `terraform-modules`, `infra-modules`)
- `version` - The git tag/version to set
- `--path` - Directory to search (default: current directory)

**Examples:**
```bash
# Update all references to terraform-modules.git
python3 update-tf-repo.py terraform-modules v3.0.0

# Update specific repo in staging environment
python3 update-tf-repo.py infra-modules v2.1.0 --path ./environments/staging
```

## 🎨 Supported URL Formats

Both scripts work with various git URL formats:

✅ **SSH URLs**
```hcl
source = "git@github.com:myorg/repo.git//module?ref=v1.0.0"
source = "git@gitlab.com:myorg/repo.git//path/to/module"
```

✅ **HTTPS URLs**
```hcl
source = "https://github.com/myorg/repo.git//module?ref=v1.0.0"
source = "https://gitlab.com/myorg/repo.git//module"
```

✅ **With and without existing versions**
```hcl
source = "git@github.com:myorg/repo.git//module"              # No version
source = "git@github.com:myorg/repo.git//module?ref=v1.0.0"  # Has version
```

## ⚠️ Important Notes

### Safety First
- **Always test on a small subset first** before running on your entire codebase
- **Use version control** - commit your changes before running the scripts
- **Review the changes** before applying them to production

### Backup Recommendation
```bash
# Create a backup before running
git add . && git commit -m "Backup before version update"

# Run the script
python3 update-tf-repo.py my-modules v2.0.0

# Review changes
git diff HEAD~1

# If happy, push. If not, revert:
git reset --hard HEAD~1
```

### Precision Matters
- `update-tf-submodule.py network` will NOT match `network-extended` modules
- `update-tf-repo.py repo` will NOT match `repo-backup.git` repositories
- Path matching is exact: `aws/vpc` matches `//aws/vpc` but not `//aws/vpc/subnets`

## 🔍 Verification

After running either script, verify the changes:

```bash
# See what was changed
git diff

# Count updated references
grep -r "?ref=v2.0.0" . --include="*.tf" | wc -l

# Find specific patterns
grep -r "myrepo\.git.*\?ref=" . --include="*.tf"
```

## 🐛 Troubleshooting

### No files were updated
- Check that you're in the right directory
- Verify the module/repo name is correct (case-sensitive)
- Ensure your `.tf` files use the expected URL format

### Too many files were updated
- Double-check the module path or repository name
- Use `--path` to limit the search scope
- Test on a single file first

### Unexpected results
- Review the command syntax
- Check for typos in module names or versions
- Use `git diff` to see exactly what changed

## 📚 Real-World Workflows

### Development Team Workflow
```bash
# 1. Developer updates a specific module
python3 update-tf-submodule.py database v2.1.0 --path ./environments/dev

# 2. Test in dev environment
terraform plan

# 3. If successful, promote to staging
python3 update-tf-submodule.py database v2.1.0 --path ./environments/staging

# 4. Finally, update production
python3 update-tf-submodule.py database v2.1.0 --path ./environments/prod
```

### Major Release Workflow
```bash
# 1. Update all modules to new major version
python3 update-tf-repo.py company-terraform-modules v3.0.0

# 2. Run terraform plan across all environments
for env in dev staging prod; do
  cd environments/$env
  terraform plan
  cd ../..
done

# 3. Apply changes environment by environment
```

---

## 📞 Need Help?

- Check the [AGENTS.md](AGENTS.md) file for technical implementation details
- Review your Terraform module source URLs for compatibility
- Test on a small subset of files first
- Use `git diff` to verify changes before committing
