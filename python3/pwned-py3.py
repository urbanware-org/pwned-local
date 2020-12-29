#!/usr/bin/env python3

# ============================================================================
# pwned-local - Check for exposed password matches of 'haveibeenpwned.com'
# Copyright (C) 2019 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/pwned-local
# GitLab: https://gitlab.com/urbanware-org/pwned-local
# ============================================================================

__version__ = "2.0.0"

import getpass
import hashlib
import os
import sys
import time


def main():
    from core import clap
    from core import paval

    try:
        p = clap.Parser()
    except Exception as e:
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Check for exposed passwords offline on the local " +
                      "system via password hash list.")
    # p.set_epilog()

    # Required arguments
    p.add_avalue("-l", "--pwned-list", "path to the text file containing " +
                 "all the password hashes", "pwned_list", None, True)

    # Optional arguments
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_avalue("-i", "--input-file", "check passwords using a plain text" +
                 "file containing your passwords", "input_file", None, False)
    p.add_switch("-p", "--prompt", "manually check your passwords via prompt",
                 None, True, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        print()
        print("Usage examples:")
        print("  ./pwned-py3.py -l pwned-passwords.txt -i my-passwords.txt")
        print("  ./pwned-py3.py -l pwned-passwords.txt -p")
        sys.exit(0)
    elif "--version" in sys.argv:
        print(__version__)
        sys.exit(0)

    args = p.parse_args()

    try:
        paval.path(args.pwned_list, "password hash file", True, True)
    except:
        p.error("The given password hash list file does not exist.")

    if not args.input_file and not args.prompt:
        p.error("Another argument is required, see '--help' for usage " +
                "examples.")
    elif args.input_file and args.prompt:
        p.error("The arguments '--input-file' and '--prompt' cannot be " +
                "used together.")
    elif args.prompt:
        check_prompt(args.pwned_list)
    else:
        try:
            paval.path(args.input_file, "input file", True, True)
        except:
            p.error("The given plain text input file does not exist.")
        check_file(args.pwned_list, args.input_file)


def get_file_size(file_path):
    """
        Get the size of a file in bytes.
    """
    input_file = open(file_path, "rb")
    input_file.seek(0, 2)
    file_size = input_file.tell()
    input_file.close()
    return file_size


def get_passwords_file(input_file):
    """
        Get passwords to be checked by reading them from a plain text file.
    """
    list_passwd = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.replace("\r\n", "").replace("\n", "")
            if len(line) > 0:
                hash_passwd = \
                    hashlib.sha1(line.encode("utf-8")).hexdigest().upper()
                print("SHA-1 hash: " + hash_passwd)
                list_passwd.append(hash_passwd)
        return list_passwd


def get_passwords_prompt():
    """
        Get passwords to be checked via prompt.
    """
    list_passwd = []
    while True:
        if len(list_passwd) == 1:
            print("You can either give further passwords or just leave " +
                  "blank and hit the")
            print("Return key to proceed.")
            print()

        passwd = getpass.getpass("Password: ")
        if len(passwd) == 0 and len(list_passwd) == 0:
            break
        elif len(passwd) == 0 and len(list_passwd) > 0:
            print("No further passwords given.")
            break

        hash_passwd = hashlib.sha1(passwd.encode("utf-8")).hexdigest().upper()
        print("SHA-1 hash: " + hash_passwd)
        list_passwd.append(hash_passwd)
        print()
    return list_passwd


def print_notice(pwned_list_size):
    """
        Print a global notice about the script as well as the file size of
        the the text file containing all the password hashes in case it seems
        to be too small.
    """
    print()
    print("Notice that this is just a very rudimentary tool as it simply " +
          "processes the")
    print("password hash list line by line which increases the CPU load " +
          "(that makes it")
    print("not really performant).")
    print()

    if pwned_list_size < 20000000000:
        print("The current password hash file seems to be an incomplete " +
              "or sample file.")
        print("Please download the complete password list from the " +
              "official website:")
        print()
        print("    https://haveibeenpwned.com/Passwords")
        print()


def check_file(pwned_list, input_file):
    """
        Check the password hashes via plain text file.
    """
    file_size_pwned = get_file_size(pwned_list)
    print_notice(file_size_pwned)

    list_passwd = get_passwords_file(input_file)
    if len(list_passwd) == 0:
        print("Canceled (no passwords given).")
        print()
        sys.exit(0)
    else:
        perform_check(pwned_list, list_passwd)


def check_prompt(pwned_list):
    """
        Check the password hashes via prompt.
    """
    file_size_pwned = get_file_size(pwned_list)
    print_notice(file_size_pwned)

    print("Enter your password below. The input will not be echoed on " +
          "the screen.")
    print()
    print("Instead of entering the passwords here, you can also " +
          "provide a text file")
    print("containing them, see '--help' for further information.")
    print()
    list_passwd = get_passwords_prompt()
    if len(list_passwd) == 0:
        print()
        print("Canceled (no passwords given).")
        print()
        sys.exit(0)
    else:
        perform_check(pwned_list, list_passwd)


def perform_check(pwned_list, list_passwd):
    """
        Main method to perform the check.
    """
    count = 0
    file_size_pwned = get_file_size(pwned_list)
    line_len = 44   # average line length
    line_count = file_size_pwned / line_len
    pwned = False
    percent = 0
    retval = 0

    if len(list_passwd) == 1:
        single_passwd = True
    else:
        single_passwd = False

    print()
    print("Passwords given: " + str(len(list_passwd)))
    print()
    print("Password database size: %s bytes" % str(file_size_pwned).rjust(12))
    print("Approximate line count: %s lines" % str(int(line_count)).rjust(12))
    print()
    print("Processing password file. Please wait as this may take a while.")
    print()
    with open(pwned_list, "r") as f:
        for line in f:
            if count % 1000000 == 0:
                percent = count / float(file_size_pwned / line_len) * 100
                sys.stdout.write("Progress: " + ('%6.2f' % percent) + " % (" +
                                 str(int(count / 1000000)) +
                                 " million lines)\r")
                sys.stdout.flush()
                time.sleep(0.002)   # reduce a bit of the CPU load
            hash_line = line.rstrip().split(":")[0]
            count += 1
            for hash_passwd in list_passwd:
                if hash_passwd == hash_line:
                    passwd = str(list_passwd.index(hash_passwd) + 1)
                    if single_passwd:
                        print("Pwned! The given password has been seen " +
                              "before!")
                        print("Found corresponding match in line %s." %
                              str(count))
                        pwned = True
                        break
                    else:
                        print("Pwned! Password #%s has been seen before!" %
                              passwd)
                        print("Found corresponding match in line %s." %
                              str(count))
                        print()
                        pwned = True

    if single_passwd:
        if pwned:
            retval = 1
    else:
        if pwned:
            print("Pwned! At least one password has been seen before!")
            retval = 1
    if not pwned:
        print("No pwnage found (no match in password file).")
    print()

    sys.exit(retval)


if __name__ == "__main__":
    main()

# EOF
