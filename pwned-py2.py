#!/usr/bin/env python2

# ============================================================================
# pwned-local - Check for exposed password matches of 'haveibeenpwned.com'
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/pwned-local
# ============================================================================

__version__ = "1.0.0"

import getpass
import hashlib
import os
import sys

count = 0
filename = "pwned-passwords.txt"
path_script = os.path.dirname(os.path.realpath(sys.argv[0]))
path_list = os.path.join(path_script, filename)
pwned = False

if not os.path.exists(path_list):
    print "error: Password file '" + filename + "' not found"
    sys.exit(2)
elif not os.path.isfile(path_list):
    print "error: Given path to password file is a directory, not a file"
    sys.exit(2)
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
print "Please wait. This may take a while."
with open(path_list, "r") as f:
    for line in f:
        hash_line = line.rstrip().split(":")[0]
        count += 1
        if hash_passwd == hash_line:
            pwned = True
            break

if pwned:
    result = "Pwned! This password has been seen before!"
    exit = 1
else:
    result = "No pwnage found (no match in password file)."
    exit = 0

print
print result
if pwned:
    print "Found corresponding match in line " + str(count) + "."
print

sys.exit(exit)

# EOF
