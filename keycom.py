#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" 
	Copyright © 2011, Gareth Latty <gareth@lattyware.co.uk>

	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

""" This script is designed to keep you logged into a keycom service (but 
should) be easily adaptable to any other redirect-sign-in systems). It tries to 
contact a known site (e.g: google) and checks if it's been redirected to a log 
in page. If it has, it then tries to log in."""

import urllib.request
import urllib.parse

""" To use this script edit the information below (for most people, this means 
editing the username and password sections. Then add it to be run regularly, for
example, using cron or some similar method. This script has only been tested
under Linux, it should, however, run under other systems."""

################################################################################
# Configuration Section
################################################################################

# The URI of the site to test connectivity with.
test_uri = "http://www.google.co.uk"

# The URI of the log in page.
uri = "http://login.keycom.co.uk:8080/goform/HtmlLoginRequest"

# The information the log in page requires. (Form_Input_Name: Value)
information = {
	"username": "yourusername",
	"password": "yourpassword",
	# Not strictly required, but makes checking for the log in success easy.
	"original_url": "success",
}

# The path to log errors to. Use 'None' for no logging.
#log_path = '/path/to/log'
log_path = None

# The string to search for in the response given by the log in page. If this is
# contained (exactly) in the response, then it is presumed the log in was 
# successful.
success_string = ("<meta http-equiv=\"refresh\" content=\"5; URL=http://"
	+information["original_url"]+"\">")

################################################################################

test = urllib.request.urlopen(test_uri)
if test.geturl() == test_uri:
	print("Logged in.")
else:
	print("Not logged in, attempting log in.")

	data = urllib.parse.urlencode(information).encode('utf-8')
	 
	response = urllib.request.urlopen(uri, data)
	response_text = response.read().decode('utf-8')

	if (success_string in response_text):
		print("Log in successful.")
		exit(0)
	else:
		extra = ""
		if log_path:
			with open(log_path, 'w') as f:
				f.write(response_text)
			extra = " Server response written to "+log_path+"."
		exit("Log in unsuccessful."+extra)
