import re
import os
import sys
import argparse

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="proprietary-file-cleaner")
    parser.add_argument('-p', required=True, help='path to proprietary-files.txt')
    parser.add_argument('-l', required=True, help='path to list')

    args = parser.parse_args()

    # Define file paths from command-line arguments
    files = {
        'target': args.p,
        'list': args.l
    }

    RED = "\033[31m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    # Check if the files exist
    for k, file in files.items():
        if os.path.exists(file):
            print(f"{GREEN}{file} exists.{RESET}")
        else:
            print(f"{RED}{file} does not exist!{RESET}")
            sys.exit(1)

    # Function to extract file paths from notfound.txt
    def extract_file_paths(line):
        match = re.search(r'!!\s*(.*): file not found', line)
        if match:
            return match.group(1).strip()
        return None

    # Read notfound file into a set of file paths
    notfound_set = set()
    with open(files['list'], 'r') as nf:
        for line in nf:
            path = extract_file_paths(line)
            if path:
                notfound_set.add(path)

    # Read target file and write lines not in notfound_set to a new file
    with open(files['target'], 'r') as pb, open("cleaned-proprietary-files.txt", 'w') as out:
        for line in pb:
            if line.strip() in notfound_set:
                print(f"{RED}Removed {line.strip()}! {RESET}")
            else:
                out.write(line)

if __name__ == "__main__":
    main()
