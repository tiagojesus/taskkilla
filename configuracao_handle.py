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