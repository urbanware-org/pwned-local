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

The [haveibeenpwned.com](https://haveibeenpwned.com/Passwords) website provides a giant password list to check for exposed passwords. Despite its privacy protections, many users are understandably reluctant to enter their passwords online.

Alternatively, the website used to provide the password list as a downloadable plain text file and *pwned-local* allows to search that list for exposed passwords offline on the local machine.

However, the password list is no longer directly downloadable as a plain text file from the website and has to be obtained another way. For details see the the [password list](#password-list) information inside the [requirements](#requirements) section below.

This is just a rudimentary tool which simply processes the password list line by line, which is not really performant. Furthermore, the code should be revised in general.

> [!NOTE]
> This project was **officially discontinued** as of August 2025 and is **no longer maintained**.

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

First of all, there are two plain text files included with *pwned-local* which are `pwned-passwords.txt` and `my-passwords.txt`.

The file `pwned-passwords.txt` just contains a **very small excerpt** from the original exposed passwords file provided by [haveibeenpwned.com](https://haveibeenpwned.com/Passwords). This is suitable for usage examples, but not for practical use. Before using *pwned-local* productively, that file has to be replaced with the original exposed passwords file mentioned earlier.

### Input prompt

You can check the passwords by entering them manually one after another via prompt.

In case you are using the *Python* 3 version the command would look like this:

```
$ ./pwned-py3.py -l pwned-passwords.txt -p
```

### Input plain text file

Another way to check the passwords is to give a plain text file which contains all passwords you want to check for.

For example, create a file (or use the included one) called `my-passwords.txt` containing some passwords you would like to check (one password per line):

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

As mentioned above, this project was discontinued. For this reason, no new features will be implemented, existing features will not be enhanced and remaining bugs will not be fixed either.

However, if you have questions about it, you can contact me by sending an email to <dev@urbanware.org>.

[Top](#pwned-local)
