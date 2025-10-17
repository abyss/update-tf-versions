#!/usr/bin/env python3
"""
Terraform Repository Version Updater

This script updates version references for git repositories in Terraform module sources.
Unlike update-tf-submodule.py which targets specific subdirectory modules, this script
updates ALL references to a specific repository regardless of subdirectories.

Usage:
    python3 update-tf-repo.py <repo_name> <version> [--path <directory>]

Examples:
    # Update all references to 'repo.git' to version 'v2.0.0'
    python3 update-tf-repo.py repo v2.0.0

    # Update in a specific directory
    python3 update-tf-repo.py my-modules v1.5.0 --path ./terraform

The script will match:
- git@github.com:org/repo.git                    -> git@github.com:org/repo.git?ref=v2.0.0
- git@github.com:org/repo.git?ref=v1.0.0         -> git@github.com:org/repo.git?ref=v2.0.0
- git@github.com:org/repo.git//modules           -> git@github.com:org/repo.git//modules?ref=v2.0.0
- https://github.com/org/repo.git//modules/test   -> https://github.com/org/repo.git//modules/test?ref=v2.0.0

The script will NOT match:
- git@github.com:org/other-repo.git (different repository name)
- git@github.com:org/repo-extended.git (partial name match protection)
"""
import os
import re
import sys
import argparse

def update_repo_version(file_path, repo_name, version):
    """
    Recursively searches for .tf files and updates repository references
    for the specified repo_name to use the provided version.
    Matches repository names regardless of subdirectories.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Pattern to match source lines with the specific repository name
    # This matches any git URL containing the repository name (with .git extension)
    # and captures any subdirectories and existing version parameters
    pattern = r'(source\s*=\s*"[^"]*/)(' + re.escape(repo_name) + r'\.git)(//[^"?]*|)(\?ref=[^"]*|)(")'

    def replace_match(match):
        prefix = match.group(1)  # Everything before repo_name.git
        repo = match.group(2)    # repo_name.git
        subdir = match.group(3)  # Any subdirectory path (//path)
        existing_ref = match.group(4)  # Existing ?ref=version or empty
        quote = match.group(5)   # The closing quote

        # Always preserve subdirectories but replace the version
        return f'{prefix}{repo}{subdir}?ref={version}{quote}'

    updated_content = re.sub(pattern, replace_match, content)

    if content != updated_content:
        with open(file_path, 'w') as file:
            file.write(updated_content)
        print(f"Updated {file_path}")

def find_and_update_tf_files(root_dir, repo_name, version):
    """Recursively find .tf files and update the specified repository version."""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .terraform directories
        if '.terraform' in dirnames:
            dirnames.remove('.terraform')

        # Process .tf files in the current directory
        for filename in [f for f in filenames if f.endswith('.tf')]:
            file_path = os.path.join(dirpath, filename)
            update_repo_version(file_path, repo_name, version)

def main():
    parser = argparse.ArgumentParser(description='Update Terraform repository versions.')
    parser.add_argument('repo_name', help='The name of the repository to update (without .git extension)')
    parser.add_argument('version', help='The version to set for the repository')
    parser.add_argument('--path', default='.', help='Path to start the recursive search (default: current directory)')

    args = parser.parse_args()

    find_and_update_tf_files(args.path, args.repo_name, args.version)

if __name__ == "__main__":
    main()
