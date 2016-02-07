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
from models import User
import re

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


class SaveUserHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('user_name')
        age = int(self.request.get('user_age'))
        # likes = self.request.get('user_likes')
        # logging.warning("likes")
        # logging.warning(likes)
        if self.request.get('user_img_link'):
            image_link = self.request.get('user_img_link')
        else:
            image_link = "http://www.freelanceme.net/Images/default%20profile%20picture.png"

        bio = self.request.get('user_bio')
        gender = self.request.get('user_gender')

        likes = []
        for key,value in self.request.POST.items():
            re_obj = re.search(r'like-(.*)',key)
            if re_obj and value == "on":
                likes.append(re_obj.group(0))
        logging.warning("likesfilled")
        logging.warning(likes)

        if name and age and gender:
            search_user = User.query(User.name == name, User.age == age, User.gender == gender)
            results = search_user.fetch()
            logging.info(results)
            if results:
                logging.warning("We have already a user named %s , age %s , gender %s . Skipping." % (name, age, gender))
            else:
                new_user = User(
                    name = name,
                    gender = gender,
                    bio = bio,
                    age = age,
                    image_link = image_link,
                    likes = likes
                    # likes = "yello"
                )
                new_user.put()
        else:
            # This should also be validated in the client before sending the request.
            logging.warning("Ignoring request because it has no name or age or gender")
        self.redirect('/')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/userinput', UserInputHandler),
    ('/saveuserinput', SaveUserHandler),
], debug=True)
