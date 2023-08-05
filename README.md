
# sliver2modrewrite
> Convert sliver's http-config.json file to apache modrewrite
## Description
This is a script that helps automate the process of converting sliver's http-config file to apache modrewrite format to allow use with a C2 redirector.
## How it works
* Takes an argument of
  * http-config
  * team server URL
  * redirection URL
  * optional - .htaccess file name
* Checks if the URL is formatted correctly
* Parses the supplied values in the config
* Places the values into a apache modrewrite template
* Outputs the .htaccess to the screen (or to the a file)
## Usage
```
NEED TO PASTE THE -h in
```
## Supported Config Options
The following options in the http-config file are currently supported:
* `stager_files`,`stager_file_ext`,`stager_paths`
* `poll_files`,`poll_file_ext`,`poll_paths`
* `start_session_file_ext`,`session_files`,`session_file_ext`,`session_paths`
* `close_files`,`close_file_ext`,`close_paths`
* `min/max values for paths` 
## Credit
Shoutout to threatexpress for their fantastic scripts, from which this script is based.
