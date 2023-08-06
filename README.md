
# sliver2modrewrite
> Convert sliver's http-c2.json file to apache modrewrite
## Description
This is a script that helps automate the process of converting sliver's http-c2 file to apache modrewrite format to allow use with a C2 redirector.
## How it works
* Takes an argument of
  * http-c2
  * team server URL
  * redirection URL
  * optional - .htaccess file name
* Checks if the URL is formatted correctly
* Parses the supplied values in the config
* Places the values into a apache modrewrite template
* Outputs the .htaccess to the screen (or to the a file)
## Usage
```
usage: sliver2modrewrite.py [-h] -i INPUTFILE -c C2SERVER -r REDIRECT [-o OUT_FILE]

Python 3.0+ Converts sliver http-c2 json file to Apache mod_rewrite. This outputs .htaccess file format which contains the rewrite rules.

options:
  -h, --help    show this help message and exit
  -i INPUTFILE  Sliver http-c2.json file
  -c C2SERVER   Sliver Server (http://teamserver)
  -r REDIRECT   Redirect to this URL (http://google.com)
  -o OUT_FILE   Write .htaccess contents to target file
```
## Supported Config Options
The following options in the http-config file are currently supported:
* `stager_files`,`stager_file_ext`,`stager_paths`
* `poll_files`,`poll_file_ext`,`poll_paths`
* `start_session_file_ext`,`session_files`,`session_file_ext`,`session_paths`
* `close_files`,`close_file_ext`,`close_paths`
* `min/max values for paths` 
## How to use with Apache Mod Rewrite



## Credit
Shoutout to threatexpress for their fantastic scripts, from which this script is based.
