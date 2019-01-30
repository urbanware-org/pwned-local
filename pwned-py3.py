#!/usr/bin/env python3

# ============================================================================
# pwned-local - Check for exposed password matches of 'haveibeenpwned.com'
# Copyright (C) 2019 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/pwned-local
# GitLab: https://gitlab.com/urbanware-org/pwned-local
# ============================================================================

__version__ = "1.0.1"

import getpass
import hashlib
import os
import sys
import time


def get_file_size(file_path):
    """
        Get the size of a file in bytes.
    """
    input_file = open(file_path, "rb")
    input_file.seek(0, 2)
    file_size = input_file.tell()
    input_file.close()

    return int(file_size)


count = 0
file_name = "pwned-passwords.txt"
path_script = os.path.dirname(os.path.realpath(sys.argv[0]))
path_list = os.path.join(path_script, file_name)
file_size = get_file_size(path_list)
line_len = 44   # average line length
line_count = int(file_size / line_len)
pwned = False
percent = 0


if not os.path.exists(path_list):
    print("error: Password file '%s' not found" % file_name)
    sys.exit(2)
elif not os.path.isfile(path_list):
    print("error: Given path to password file is a directory, not a file")
    sys.exit(2)

print()
print("Notice that this is just a rudimentary tool as it simply " +
      "processes the ")
print("password list line by line which increases the CPU load (that " +
      "makes it")
print("not really performant).")
print()

if file_size < 20000000000:
    print("The current password file seems to be an incomplete or " +
          "sample file.")
    print("Please download the complete password list from the official " +
          "website:")
    print()
    print("    https://haveibeenpwned.com/Passwords")
    print()

print("Enter your password below. The input will not be echoed on the " +
      "screen.")
print()
passwd = getpass.getpass("Password: ")
if len(passwd) == 0:
    print()
    print("Canceled (no password given).")
    print()
    sys.exit(0)

hash_passwd = hashlib.sha1(passwd.encode("utf-8")).hexdigest().upper()
print("SHA-1 hash: " + hash_passwd)
print()
print("Password database size: %s bytes" % str(file_size).rjust(12))
print("Approximate line count: %s lines" % str(line_count).rjust(12))
print()
print("Processing password file. Please wait as this may take a while.")
print()
with open(path_list, "r") as f:
    for line in f:
        if count % 1000000 == 0:
            percent = count / float(file_size / line_len) * 100
            sys.stdout.write("Progress: " + ('%6.2f' % percent) + " % (" +
                             str(count / 1000000) + " million lines)\r")
            sys.stdout.flush()
            time.sleep(0.002)   # reduce a bit of the CPU load
        hash_line = line.rstrip().split(":")[0]
        count += 1
        if hash_passwd == hash_line:
            pwned = True
            break

if pwned:
    result = "Pwned! This password has been seen before!"
    retval = 1
else:
    result = "No pwnage found (no match in password file)."
    retval = 0

print(result)
if pwned:
    print("Found corresponding match in line " + str(count) + ".")
print()

sys.exit(retval)

# EOF
