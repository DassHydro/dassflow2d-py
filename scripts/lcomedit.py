import os
import sys

def process_file(filepath, new_comment):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Detect and skip leading multi-line comment
    in_multiline_comment = False
    skip_until = 0

    for i, line in enumerate(lines):
        if i == 0 and line.strip().startswith('"""'):
            in_multiline_comment = True
        if in_multiline_comment and '"""' in line and i != 0:
            skip_until = i + 1
            break

    # Write new comment and the rest of the file
    with open(filepath, 'w') as f:
        f.write(f'"""\n{new_comment}\n"""\n')
        if skip_until > 0:
            f.writelines(lines[skip_until:])
        else:
            f.writelines(lines)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <directory> <comment_file>")
        sys.exit(1)

    directory = sys.argv[1]
    comment_file = sys.argv[2]

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    if not os.path.isfile(comment_file):
        print(f"Error: {comment_file} is not a valid file.")
        sys.exit(1)

    with open(comment_file, 'r') as f:
        new_comment = f.read().strip()

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                process_file(filepath, new_comment)

if __name__ == "__main__":
    main()
