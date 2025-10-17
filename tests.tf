# Raw Repository
# Should not be matched
module "example" {
  source = "git@github.com:example/repo.git"

  test = "example"
}

# Repository with Version Tag
# Should not be matched
module "example2" {
  source = "git@github.com:example/repo.git?ref=v1.0.0"

  test = "example"
}

# Subdirectory within Repository
# Should be matched with `test`
module "example3" {
  source = "git@github.com:example/repo.git//test"

  test = "example"
}

# Subdirectory with Version Tag
# Should be matched with `test`
module "example4" {
  source = "git@github.com:example/repo.git//test?ref=v1.0.0"

  test = "example"
}

# Nested Subdirectory within Repository
# Should be matched with `test/example`
module "example5" {
  source = "git@github.com:example/repo.git//test/example"

  test = "example"
}

# Nested Subdirectory with Version Tag
# Should be matched with `test/example`
module "example6" {
  source = "git@github.com:example/repo.git//test/example?ref=v1"

  test = "example"
}
