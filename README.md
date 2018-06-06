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

Even though, the website protects the privacy of searched passwords, some people still don't want to enter their passwords online.

However, the website also provides that password list as a downloadable text file and *pwned-local* allows to search that list for exposed passwords offline on the local machine.

[Top](#pwned-local)

## Requirements

In order to use *pwned-local*, the *Python* framework must be installed on the system.

Depending on which version of the framework you are using:

*   *Python* 2.x (version 2.7 or higher is recommended, may also work with earlier versions)
*   *Python* 3.x (version 3.2 or higher is recommended, may also work with earlier versions)

[Top](#pwned-local)

## Usage

Before you can use *pwned-local*, you have to download the password list from the [haveibeenpwned.com](https://haveibeenpwned.com/Passwords) website.

Follow the link above and scroll down to the table that provides the download links.

### Download the latest list version

First, download the newest version of the list which is the largest file you can get (has more than 8 gigabytes).

The password list itself is a simple text file containing SHA-1 hashes of the exposed passwords and has a size of about 30 gigabytes. Due to this, the password list is compressed as a *7z* archive.

So, download the archive and extract it (may take a while). After that, rename the extracted file to `pwned-passwords.txt`, for example:

```bash
$ mv pwned-passwords-2.0.txt pwned-passwords.txt
```

Copy that file into the same directory where `pwned-py2.py` and `pwned-py3.py` are located.

### Apply list updates

The password list can be enhanced with updates also provided on the same website.

Download and extract those archives. Then, append them to the main list like this:

```bash
$ cat pwned-passwords-update-2.txt >> pwned-passwords.txt
```

### Search exposed passwords

Now, you can search for exposed passwords. Either run `pwned-py2.py` or `pwned-py3.py` (depending on which *Python* framework is installed).

The script will prompt for your password (hidden) and after confirming, it starts searching the password list and returns the information if it has been exposed.

[Top](#pwned-local)

## Contact

Any suggestions, questions, bugs to report or feedback to give?

You can contact me by sending an email to <dev@urbanware.org>.

[Top](#pwned-local)
