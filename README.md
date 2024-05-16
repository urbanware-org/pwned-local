# *pwned-local*

**Table of contents**
*   [Definition](#definition)
*   [Details](#details)
*   [Requirements](#requirements)
*   [Usage](#usage)
*   [Contact](#contact)

----

## Definition

Check for exposed password matches inside the giant password list of [haveibeenpwned.com](https://haveibeenpwned.com/Passwords) offline on the local system.

[Top](#pwned-local)

## Details

The [haveibeenpwned.com](https://haveibeenpwned.com/Passwords) website provides a giant password list to check for exposed passwords online.

Even though the website protects the privacy of searched passwords, some people still do not want to enter their passwords online.

However, it also provides the password list as a downloadable text file and *pwned-local* allows to search that list for exposed passwords offline on the local machine.

This is just a rudimentary tool due to the fact that it simply processes the password list line by line which is not really performant. Furthermore, the code should be revised in general. It works so far, but it does not look very nice.

[Top](#pwned-local)

## Requirements

### Runtime environment

In order to use *pwned-local*, the *Python* framework must be installed on the system.

Depending on which version of the framework you are using:

*   *Python* 2.x (version 2.7 or higher is recommended, may also work with earlier versions)
*   *Python* 3.x (version 3.2 or higher is recommended, may also work with earlier versions)

### Password list

The password list is no longer available as plain text file as a download directly from the website. Instead, there is the official [PwnedPasswordsDownloader](https://github.com/HaveIBeenPwned/PwnedPasswordsDownloader) tool to get the password list.

However, I have not used that tool before, so I cannot tell anything about it.

You have to download the file containing the password hashes in the **SHA-1** format as *pwned-local* only supports those.

[Top](#pwned-local)

## Usage

If the requirements are met, you can check for exposed passwords. There are two modes as shown below.

In these usage examples the downloaded file which contains all the password hashes is called `pwned-passwords.txt`.

### Input prompt

You can check the passwords by entering them manually one after another via prompt.

In case you are using the *Python* 3 version the command would look like this:

```
$ ./pwned-py3.py -l pwned-passwords.txt -p
```

### Input plain text file

Another way to check the passwords is to give a plain text file which contains all passwords you want to check for.

For example, create a file called `my-passwords.txt` containing some passwords you would like to check:

```
sample
1234
12345
foo
foobar
thisshouldnotbeinsidethepwnedfile
```

In case you are using the *Python* 3 version the command to check the passwords this way would look like this:

```
$ ./pwned-py3.py -l pwned-passwords.txt -i my-passwords.txt
```

[Top](#pwned-local)

## Contact

Any suggestions, questions, bugs to report or feedback to give?

You can contact me by sending an email to [dev@urbanware.org](mailto:dev@urbanware.org) or by opening a *GitHub* issue (which I would prefer if you have a *GitHub* account).

[Top](#pwned-local)
