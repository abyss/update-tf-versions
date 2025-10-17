#!/usr/bin/env python3
import os
import re
import sys
import argparse

def update_module_version(file_path, module_name, version):
    """
    Recursively searches for .tf files and updates module references
    for the specified module_name to use the provided version.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Pattern to match source lines with the specific module name
    # This matches the repository URL, followed by //, followed by the module name,
    # ensuring the module name is at a path boundary (followed by ?, /, or ")
    # This prevents "test" from matching "test/example" when looking for exact "test"
    pattern = r'(source\s*=\s*"[^"]+//)(' + re.escape(module_name) + r')(\?ref=[^"]*|/[^"]*|)(")'

    def replace_match(match):
        prefix = match.group(1)  # Everything before module_name
        module = match.group(2)  # module_name
        existing_suffix = match.group(3)  # Existing ?ref=version, /path, or empty
        quote = match.group(4)  # The closing quote

        # If the suffix starts with '/' and doesn't match our exact module path, skip this match
        if existing_suffix.startswith('/'):
            # Extract the full path after //
            full_path = module + existing_suffix
            # If we're looking for 'test' but found 'test/something', it's not a match
            if not full_path == module_name and not full_path.startswith(module_name + '?'):
                return match.group(0)  # Return original unchanged

        # If there's already a ?ref= or a path after the module name, replace it
        # Otherwise, just add the new version
        if existing_suffix.startswith('?ref='):
            return f'{prefix}{module}?ref={version}{quote}'
        elif existing_suffix.startswith('/'):
            # Keep any subpath after the module name but remove any existing ?ref= and add the new version
            # Handle case where path contains ?ref= parameter
            if '?ref=' in existing_suffix:
                path_part = existing_suffix.split('?ref=')[0]
                return f'{prefix}{module}{path_part}?ref={version}{quote}'
            else:
                return f'{prefix}{module}{existing_suffix}?ref={version}{quote}'
        else:
            # No existing ref or path, just add the version
            return f'{prefix}{module}?ref={version}{quote}'

    updated_content = re.sub(pattern, replace_match, content)

    if content != updated_content:
        with open(file_path, 'w') as file:
            file.write(updated_content)
        print(f"Updated {file_path}")

def find_and_update_tf_files(root_dir, module_name, version):
    """Recursively find .tf files and update the specified module version."""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .terraform directories
        if '.terraform' in dirnames:
            dirnames.remove('.terraform')

        # Process .tf files in the current directory
        for filename in [f for f in filenames if f.endswith('.tf')]:
            file_path = os.path.join(dirpath, filename)
            update_module_version(file_path, module_name, version)

def main():
    parser = argparse.ArgumentParser(description='Update Terraform module versions.')
    parser.add_argument('module_name', help='The name of the module to update')
    parser.add_argument('version', help='The version to set for the module')
    parser.add_argument('--path', default='.', help='Path to start the recursive search (default: current directory)')

    args = parser.parse_args()

    find_and_update_tf_files(args.path, args.module_name, args.version)

if __name__ == "__main__":
    main()
