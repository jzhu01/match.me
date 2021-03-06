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
import json

JINJA_ENVIRONMENT = jinja2.Environment (
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

FRIEND_ENTRIES = []

class UserInputHandler(webapp2.RequestHandler):
    def get(self):
        header_template = JINJA_ENVIRONMENT.get_template('templates/header.html')
        header_values = {}
        header_values["page_title"] = "match.me | Account Settings"
        header_values["link_to_stylesheet"] = "../css/userinput.css"
        header_values["script_source"] = "../javascript/script.js"

        self.response.write(header_template.render(header_values))

        # body_template = JINJA_ENVIRONMENT.get_template('templates/create-account.html')
        user_input_page = open('templates/userinput.html').read()
        self.response.write(user_input_page)


class SaveUserHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('user_name')
        age = int(self.request.get('user_age'))
        image_link = self.request.get('user_img_link')
        bio = self.request.get('user_bio')
        gender = self.request.get('user_gender')
        likes = json.loads(self.request.get('likes'))
        zipcode = self.request.get('user_zip')

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
                    likes = likes,
                    zipcode = zipcode
                )
                new_user.put()
        else:
            # This should also be validated in the client before sending the request.
            logging.warning("Ignoring request because it has no name or age or gender")
        # self.redirect('/')

        # Here comes the comparison with interests
        friend_suggestions = User.query(User.likes.IN(likes))
        # get the specific likes that they share?

        for friend in friend_suggestions:
            logging.warning(friend)
            FRIEND_ENTRIES.append({'friendname': friend.name, 'friendage': friend.age, 'friendbio': friend.bio, 'friendgender': friend.gender, "friendlikes":friend.likes,'friendimg': friend.image_link})

class MatchesHandler(webapp2.RequestHandler):
    def get(self):
        header_template = JINJA_ENVIRONMENT.get_template('templates/header.html')
        header_values = {}
        header_values["page_title"] = "match.me | Matches"
        header_values["link_to_stylesheet"] = "../css/matches.css"
        self.response.write(header_template.render(header_values))

        logging.info(FRIEND_ENTRIES)
        template = JINJA_ENVIRONMENT.get_template('templates/matches.html')
        template_values = {
            "contentArray" : FRIEND_ENTRIES,
        }
        self.response.write(template.render(template_values))

class MessageHandler(webapp2.RequestHandler):
    def get(self):
        header_template = JINJA_ENVIRONMENT.get_template('templates/header.html')
        header_values = {}
        header_values["page_title"] = "match.me | Message"
        header_values["link_to_stylesheet"] = "../css/message.css"
        # header_values["script_source"] = ".."
        self.response.write(header_template.render(header_values))

        message_page = open('templates/message.html').read()
        self.response.write(message_page)

class MeetingHandler(webapp2.RequestHandler):
    def get(self):
        header_template = JINJA_ENVIRONMENT.get_template('templates/header.html')
        header_values = {}
        header_values["page_title"] = "match.me | Meet"
        header_values["link_to_stylesheet"] = "../css/meeting.css"
        # header_values["script_source"] = ".."
        self.response.write(header_template.render(header_values))

        meeting_page = open('templates/meeting.html').read()
        self.response.write(meeting_page)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        header_template = JINJA_ENVIRONMENT.get_template('templates/mainpage_header.html')
        header_values = {}
        header_values["page_title"] = "Welcome to match.me"
        header_values["link_to_stylesheet"] = "../css/mainpage.css"
        self.response.write(header_template.render(header_values))

        mainpage = open('templates/mainpage.html').read()
        self.response.write(mainpage)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/userinput', UserInputHandler),
    ('/saveuserinput', SaveUserHandler),
    ('/matches', MatchesHandler),
    ('/message', MessageHandler),
    ('/meeting', MeetingHandler),
], debug=True)
