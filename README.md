
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
1. `sudo apt install apache2`
2. edit the /etc/apache2/apache2.config file - change allow overide to all
```
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride All
	Require all granted
</Directory>
```
3. `sudo a2enmod rewrite proxy proxy_http`
4. `sudo service apache2 restart`
5. Run the script to generate the .htaccess
```
python3 sliver2modrewrite.py -i http-c2.json -c http://10.10.10.10 -r https://google.co.uk
```
6. Save the output into `/var/www/html/.htaccess` or copy the saved .htacces file to the directory
7. `sudo systemctl restart apache2`

## Exmaple apache mod rewrite config
```
########################################
## .htaccess START
RewriteEngine On

## C2 Traffic (HTTP-GET, HTTP-POST, HTTP-STAGER URIs)
## Logic: If a requested URI matches and the User-Agent String matches, proxy the connection to the Teamserver
## Refer to http://httpd.apache.org/docs/current/mod/mod_rewrite.html
## Only allow GET and POST methods to pass to the C2 server
RewriteCond %{REQUEST_METHOD} ^(GET|POST) [NC]
## Profile URIs
RewriteCond %{REQUEST_URI} ^(/php/?|/api/?|/upload/?|/actions/?|/rest/?|/v1/?|/auth/?|/authenticate/?|/oauth/?|/oauth2/?|/oauth2callback/?|/database/?|/db/?|/namespaces/?|/js/?|/umd/?|/assets/?|/bundle/?|/bundles/?|/scripts/?|/script/?|/javascripts/?|/javascript/?|/jscript/?|/static/?|/www/?|/assets/?|/images/?|/icons/?|/image/?|/icon/?|/png/?|/static/?|/assets/?|/fonts/?|/locales/?|/?){2,4}(login|signin|api|samples|rpc|index|admin|register|sign-up|bootstrap|bootstrap.min|jquery.min|jquery|route|app|app.min|array|backbone|script|email|favicon|sample|example|attribute_text_w01_regular|ZillaSlab-Regular.subset.bbc33fb47cf6|ZillaSlab-Bold.subset.e96c15f68c68|Inter-Regular|Inter-Medium)(.php|.html|.js|.png|.woff)$
## Profile UserAgent
RewriteCond %{HTTP_USER_AGENT} ^.*$
RewriteRule ^.*$ "http://192.168.239.136%{REQUEST_URI}" [P,L]

## Redirect all other traffic here
RewriteRule ^.*$ https://google.co.uk/? [L,R=302]

## .htaccess END
########################################
```


## Debugging

If you need to debug the rules to check if they are working or where they are failing you can add the following to the `etc/apache/apache2.conf`
```
LogLevel alert rewrite:trace5
```
Then you can read `/var/log/apache2/error.log` and `/var/log/apache2/error.log`


## Credit
Shoutout to threatexpress for their fantastic scripts, from which this script is based.
