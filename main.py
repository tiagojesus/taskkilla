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
import json
from google.appengine.ext import ndb
import webapp2


class Task(ndb.Model):
    name = ndb.StringProperty()
    done = ndb.StringProperty()
    xp = ndb.IntegerProperty()
    questKey = ndb.KeyProperty()
    userKey = ndb.KeyProperty()

    def to_dct(self):
        dct = self.to_dict()
        del dct['questKey']
        dct['id'] = self.key.id()

        return dct

    #temUsers


class Quest(ndb.Model):
    progress = ndb.IntegerProperty()
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    xp = ndb.IntegerProperty()
    deadline = ndb.StringProperty()
    projectKey = ndb.KeyProperty()

    def get_tasks(self):
        return Task.query(Task.questKey==self.key).fetch()
    #tasks
    #temAttachment
    def to_dct(self):
        dct = self.to_dict()
        dct['id'] = self.key.id()
        del dct['projectKey']

        tasks = self.get_tasks()
        dct['tasks'] = [q.to_dct() for q in tasks]

        return dct



class Project(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    xp = ndb.IntegerProperty()
    progress = ndb.IntegerProperty()

    def get_quests(self):
        return Quest.query(Quest.projectKey==self.key).fetch()
    #temQuests
    #temUser

    #temComments

    def to_dct(self):
        dct = self.to_dict()
        dct['id'] = self.key.id()

        quests = self.get_quests()
        dct['quests'] = [q.to_dct() for q in quests]

        return dct

class User(ndb.Model):
    name = ndb.StringProperty()
    picturePath = ndb.StringProperty()



class Attachment(ndb.Model):
    title = ndb.StringProperty()
    name = ndb.StringProperty()
    when = ndb.StringProperty()
    type = ndb.StringProperty()



class Comment(ndb.Model):
    content = ndb.StringProperty()
    when = ndb.StringProperty()




class MainHandler(webapp2.RequestHandler):
    def get(self):

        #self.response.write(json.dumps(project.to_dct()))
        self.response.write("Hello")



class ProjectCreateHandle(webapp2.RequestHandler):
    def post(self):
        project = Project(
            name=self.request.post('name'),
            description=self.request.post('done'),
            xp=self.request.post('xp'),
        )
        project.put()


class ProjectListHandler(webapp2.RequestHandler):
    def get(self):
        query = Project.query().order(Project.progress)
        projetos = query.fetch()
        projetos = [p.to_dct() for p in projetos]
        self.response.write(json.dumps(projetos))



class CreateEntitiesHandler(webapp2.RequestHandler):
    def get(self):
        ndb.delete_multi(
            Project.query().fetch(keys_only=True)
        )
        ndb.delete_multi(
            Quest.query().fetch(keys_only=True)
        )
        ndb.delete_multi(
            Task.query().fetch(keys_only=True)
        )

        project = Project(name="project 01", progress=10,
                          description="descricao", xp=100)
        project.put()

        quest = Quest(name="quest 01", description="description",
                      xp=30, deadline="2013-11-21",
                      progress=10, projectKey=project.key)
        quest.put()

        task = Task(name="task", done="true", questKey=quest.key)
        task.put()

        self.response.write("ok")



app = webapp2.WSGIApplication([
        ('/', MainHandler),
        ('/init', CreateEntitiesHandler),
        ('/project/list', ProjectListHandler),
        ('/project/create', ProjectCreateHandle)

    ], debug=True)
