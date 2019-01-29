#!/usr/bin/env python2

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
pwned_lines = sum((1 for i in open(path_list, 'rb')))
pwned = False
percent = 0
perstep = pwned_lines / 100

if not os.path.exists(path_list):
    print "error: Password file '" + file_name + "' not found"
    sys.exit(2)
elif not os.path.isfile(path_list):
    print "error: Given path to password file is a directory, not a file"
    sys.exit(2)

print
print "Enter your password below. The input will not be echoed on the screen."
print
passwd = getpass.getpass("Password: ")
if passwd == "":
    print
    print "Canceled (no password given)."
    print
    sys.exit(0)

hash_passwd = hashlib.sha1(passwd).hexdigest().upper()
print "SHA-1 hash: " + hash_passwd
print
print "Database size in bytes: " + str(get_file_size(path_list))
print "Total count of lines:   " + str(pwned_lines)
print
print "Please wait. This may take a while."
print
with open(path_list, "r") as f:
    for line in f:
        if count % perstep == 0:
            percent += 1
            sys.stdout.write('Progress: ' + str(percent).rjust(3) + ' % (' +
                             str(count) + ' lines)\r')
            sys.stdout.flush()
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

print result
if pwned:
    print "Found corresponding match in line " + str(count) + "."
print

sys.exit(retval)

# EOF
