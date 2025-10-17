# Raw Repository
# Should be matched with `repo` (matches repo.git)
module "example" {
  source = "git@github.com:example/repo.git"

  test = "example"
}

# Repository with Version Tag
# Should be matched with `repo` (matches repo.git)
module "example2" {
  source = "git@github.com:example/repo.git?ref=v1.0.0"

  test = "example"
}

# Subdirectory within Repository
# Should be matched with `repo` (matches repo.git, ignores subdirectory)
module "example3" {
  source = "git@github.com:example/repo.git//test"

  test = "example"
}

# Subdirectory with Version Tag
# Should be matched with `repo` (matches repo.git, ignores subdirectory)
module "example4" {
  source = "git@github.com:example/repo.git//test?ref=v1.0.0"

  test = "example"
}

# Nested Subdirectory within Repository
# Should be matched with `repo` (matches repo.git, ignores nested subdirectory)
module "example5" {
  source = "git@github.com:example/repo.git//test/example"

  test = "example"
}

# Nested Subdirectory with Version Tag
# Should be matched with `repo` (matches repo.git, ignores nested subdirectory)
module "example6" {
  source = "git@github.com:example/repo.git//test/example?ref=v1"

  test = "example"
}

# Different Repository
# Should NOT be matched with `repo` (different repo name: other-repo.git)
module "example7" {
  source = "git@github.com:example/other-repo.git"

  test = "example"
}

# Different Repository with Subdirectory
# Should NOT be matched with `repo` (different repo name: other-repo.git)
module "example8" {
  source = "git@github.com:example/other-repo.git//some/path"

  test = "example"
}

# Repository with Similar Name
# Should NOT be matched with `repo` (different repo name: repo-extended.git)
module "example9" {
  source = "git@github.com:example/repo-extended.git//test"

  test = "example"
}

# HTTPS Repository
# Should be matched with `repo` (matches repo.git via HTTPS)
module "example10" {
  source = "https://github.com/example/repo.git"

  test = "example"
}

# HTTPS Repository with Subdirectory
# Should be matched with `repo` (matches repo.git via HTTPS, ignores subdirectory)
module "example11" {
  source = "https://github.com/example/repo.git//modules/test?ref=v2.0.0"

  test = "example"
}
