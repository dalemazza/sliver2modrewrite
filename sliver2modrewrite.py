#!/usr/bin/env python

## Title:       sliver2modrewrite.py
## Thanks: Massive shout out the threatexpress for their amazing modrewrite scripts,from which this script is based
## Author:      Dalemazza

import argparse
import sys
import re
import json

description = '''
Python 3.0+
Converts sliver http-c2 json file to Apache mod_rewrite. This outputs .htaccess file format which contains the rewrite rules.
'''

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-i', dest='inputfile', help='Sliver http-c2.json file', required=True)
parser.add_argument('-c', dest='c2server', help='Sliver Server (http://teamserver)', required=True)
parser.add_argument('-r', dest='redirect', help='Redirect to this URL (http://google.com)', required=True)
parser.add_argument('-o', dest='out_file', help='Write .htaccess contents to target file', required=False)

args = parser.parse_args()

# Make sure we were provided with vaild URLs
# https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

if re.match(regex, args.c2server) is None:
    parser.print_help()
    print("[!] c2server is malformed. Are you sure {} is a valid URL?".format(args.c2server),file=sys.stderr)
    sys.exit(1)

if re.match(regex, args.redirect) is None:
    parser.print_help()
    print("[!] redirect is malformed. Are you sure {} is a valid URL?".format(args.redirect),file=sys.stderr)
    sys.exit(1)

# Read in the http Config file
configFile = open(args.inputfile,"r")
contents = configFile.read()
contents = json.loads(contents)

# Errors
errorfound = False
errors = "\n##########\n[!] ERRORS\n"

# Make sure a implant_config exists in the config before we continue
if "implant_config" in contents:
    implant_config = contents["implant_config"]
else:
    print("[!] Could not find implant_config in the provided JSON file",file=sys.stderr)
    sys.exit(1)


# Extract User-Agent string
ua = ''
uas = contents["implant_config"]["user_agent"]
if uas == "":
    ua = "^.*$"
else:
    ua = '"' + uas + '"'

# URI path stuff
uris = []
paths = ["session_paths","poll_paths","close_paths","stager_paths"]

# extract all uri path values
for path in paths:
    uri_paths = contents["implant_config"][path]

    if uri_paths == "":
        print("No " + path + " found")
    else:
        for i in uri_paths:
            uris.append("\/" + i)

# Extension stuff
extensions = []
exts = ["session_file_ext","start_session_file_ext","poll_file_ext","close_file_ext","stager_file_ext"]

# extract all file extension values
for file_ext in exts:
    ext_p = contents["implant_config"][file_ext]

    if ext_p == "":
        print("No " + exts + " found")
    else:
         extensions.append(ext_p)
# File path stuff
f_paths = []
file_paths = ["session_files","poll_files","close_files","stager_files"]

# extract all file path values
for path in file_paths:
    file_key = contents["implant_config"][path]

    if file_key == "":
        print("No " + path + " found")
    else:
        for i in file_key:
            f_paths.append(i)

# Create UA in modrewrite syntax. No regex needed in UA string matching, but () characters must be escaped
ua_string = ua.replace('(','\(').replace(')','\)')

# Create regex strings in modrewrite syntax. "*" are needed in regex to support GET and uri-append parameters on the URI
uris_string = "\/?|".join(uris) + "\/?|\/"
files_string = "|".join(f_paths)
exts_string = "|".join(extensions)
mmvars = "{1,8}"
htaccess_template = '''
########################################
## .htaccess START
RewriteEngine On

## C2 Traffic (HTTP-GET, HTTP-POST, HTTP-STAGER URIs)
## Logic: If a requested URI matches and the User-Agent String matches, proxy the connection to the Teamserver
## Refer to http://httpd.apache.org/docs/current/mod/mod_rewrite.html
## Only allow GET and POST methods to pass to the C2 server
RewriteCond %{{REQUEST_METHOD}} ^(GET|POST) [NC]
## Profile URIs
RewriteCond %{{REQUEST_URI}} ^({uris}){min_max}({files})({exts})(?.*)$
## Profile UserAgent
RewriteCond %{{HTTP_USER_AGENT}} {ua}
RewriteRule ^.*$ "{c2server}%{{REQUEST_URI}}" [P,L]

## Redirect all other traffic here
RewriteRule ^.*$ {redirect}/? [L,R=302]

## .htaccess END
########################################
'''
print("#### Save the following as .htaccess in the root web directory")
if ua == "^.*$":
    print("## Profile User-Agent was empty, Setting it to accept all User-Agent strings:")
    print("# {}".format(ua))
else:
    print("## Profile User-Agent found:")
    print("# {}".format(ua))
print("## Profile paths found ({})".format(str(len(uris))))
print("## Profile file paths found ({})".format(str(len(f_paths))))
print("## Profile file extension paths found ({})".format(str(len(extensions))))
htaccess = htaccess_template.format(uris=uris_string, ua=ua_string, c2server=args.c2server, redirect=args.redirect, files=files_string, exts=exts_string, min_max=mmvars)
if args.out_file:
    with open(args.out_file, 'w') as outfile:
        outfile.write(htaccess)
else:
    print(htaccess)

# Print Errors Found
if errorfound:
    print(errors, file=sys.stderr)
