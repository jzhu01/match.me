#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import os
import jinja2
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment (
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class UserInputHandler(webapp2.RequestHandler):
    def get(self):
        header_template = JINJA_ENVIRONMENT.get_template('templates/header.html')
        header_values = {}
        header_values["page_title"] = "match.me | Account Settings"
        header_values["link_to_stylesheet"] = "../css/userinput.css"
        header_values["script_source"] = "http://yui.yahooapis.com/3.18.1/build/yui/yui-min.js"
        # header_values["link_to_stylesheet"] = "../css/header.css"
        self.response.write(header_template.render(header_values))

        # body_template = JINJA_ENVIRONMENT.get_template('templates/create-account.html')
        user_input_page = open('templates/userinput.html').read()
        self.response.write(user_input_page)




class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/userinput', UserInputHandler),
], debug=True)
