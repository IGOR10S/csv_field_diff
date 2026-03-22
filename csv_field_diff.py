#!/usr/bin/env python3

import os
import sys
import csv

def load_data(filename, field):
    data = set()

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if field not in reader.fieldnames:
            print(f"Error: Column '{field}' not found in '{filename}'")
            sys.exit(1)

        for row in reader:
            name = row.get(field)
            if name:
                data.add(name.strip())

    return data


def file_check(old_file, new_file):
    error = False

    for file in (old_file, new_file):
        if not os.path.exists(file):
            print(f"Error: File not found: {file}")
            error = True
    if error:
        sys.exit(1)


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <old_file> <new_file> <column_name>")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]
    col = sys.argv[3]
    
    file_check(old_file, new_file)
    old_hosts = load_data(old_file, col)
    new_hosts = load_data(new_file, col)

    diff_new = new_hosts - old_hosts
    diff_old = old_hosts - new_hosts

    if not diff_new and not diff_old:
        print(f"No difference found between '{old_file}' and '{new_file}'")
        return

    print(f"\n[+] Hosts present in the new file ({new_file}) but not in the old one ({old_file}): {len(diff_new)}\n")
    for host in sorted(diff_new):
        print(host)

    print(f"\n[-] Hosts present in the old file ({old_file}) but not in the new one ({new_file}): {len(diff_old)}\n")
    for host in sorted(diff_old):
        print(host)


if __name__ == "__main__":
    main()
