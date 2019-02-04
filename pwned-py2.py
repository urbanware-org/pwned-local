#!/usr/bin/env python2

# ============================================================================
# pwned-local - Check for exposed password matches of 'haveibeenpwned.com'
# Copyright (C) 2019 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/pwned-local
# GitLab: https://gitlab.com/urbanware-org/pwned-local
# ============================================================================

__version__ = "1.2.1"

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


def get_passwords():
    """
        Get passwords to be checked.
    """
    list_passwd = []
    while True:
        if len(list_passwd) == 1:
            print "You can either give further passwords or just leave " + \
                  "blank and hit the"
            print "Return key to proceed."
            print

        passwd = getpass.getpass("Password: ")
        if len(passwd) == 0:
            print "No further password given."
            break

        hash_passwd = hashlib.sha1(passwd).hexdigest().upper()
        print "SHA-1 hash: " + hash_passwd
        list_passwd.append(hash_passwd)
        print
    return list_passwd


def read_passwords(input_file):
    list_passwd = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.replace("\r\n", "").replace("\n", "")
            if len(line) > 0:
                hash_passwd = hashlib.sha1(line).hexdigest().upper()
                print "SHA-1 hash: " + hash_passwd
                list_passwd.append(hash_passwd)
        return list_passwd


count = 0
file_name = "pwned-passwords.txt"
path_script = os.path.dirname(os.path.realpath(sys.argv[0]))
path_list = os.path.join(path_script, file_name)
file_size = get_file_size(path_list)
line_len = 44   # average line length
line_count = file_size / line_len
pwned = False
percent = 0
retval = 0

if len(sys.argv) == 1:
    if not os.path.exists(path_list):
        print "error: Password file '%s' not found" % file_name
        sys.exit(2)
    elif not os.path.isfile(path_list):
        print "error: Given path to password file is a directory, not a file"
        sys.exit(2)
else:
    if not os.path.exists(sys.argv[1]):
        print "error: Input text file '%s' not found" % sys.argv[1]
        sys.exit(2)
    elif not os.path.isfile(sys.argv[1]):
        print "error: Given path to input text file is a directory, " + \
              "not a file"
        sys.exit(2)

print
print "Notice that this is just a rudimentary tool as it simply " + \
      "processes the "
print "password list line by line which increases the CPU load (that " + \
      "makes it"
print "not really performant)."
print

if file_size < 20000000000:
    print "The current password file seems to be an incomplete or " + \
          "sample file."
    print "Please download the complete password list from the official " + \
          "website:"
    print
    print "    https://haveibeenpwned.com/Passwords"
    print

if len(sys.argv) == 1:
    print "Enter your password below. The input will not be echoed on " + \
          "the screen."
    print
    print "Instead of entering the passwords here, you can also " + \
          "provide a text"
    print "file containing them, for example:"
    print
    print "    %s mypasswords.txt" % sys.argv[0]
    print
    list_passwd = get_passwords()
    if len(list_passwd) == 0:
        print
        print "Canceled (no passwords given)."
        print
        sys.exit(0)
else:
    list_passwd = read_passwords(sys.argv[1])

if len(list_passwd) == 1:
    single_passwd = True
else:
    single_passwd = False

print
print "Passwords given: " + str(len(list_passwd))
print
print "Password database size: %s bytes" % str(file_size).rjust(12)
print "Approximate line count: %s lines" % str(int(line_count)).rjust(12)
print
print "Processing password file. Please wait as this may take a while."
print
with open(path_list, "r") as f:
    for line in f:
        if count % 1000000 == 0:
            percent = count / float(file_size / line_len) * 100
            sys.stdout.write("Progress: " + ('%6.2f' % percent) + " % (" +
                             str(int(count / 1000000)) + " million lines)\r")
            sys.stdout.flush()
            time.sleep(0.002)   # reduce a bit of the CPU load
        hash_line = line.rstrip().split(":")[0]
        count += 1
        for hash_passwd in list_passwd:
            if hash_passwd == hash_line:
                passwd = str(list_passwd.index(hash_passwd) + 1)
                if single_passwd:
                    print "Pwned! The given password has been seen before!"
                    print "Found corresponding match in line %s." % \
                          str(count)
                    pwned = True
                    break
                else:
                    print "Pwned! Password #%s has been seen before!" % passwd
                    print "Found corresponding match in line %s." % \
                          str(count)
                    print
                    pwned = True

if single_passwd:
    if pwned:
        retval = 1
else:
    if pwned:
        print "Pwned! At least one password has been seen before!"
        retval = 1
if not pwned:
    print "No pwnage found (no match in password file)."
print

sys.exit(retval)

# EOF
