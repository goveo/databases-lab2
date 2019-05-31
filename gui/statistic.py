import npyscreen

class Statistic(npyscreen.ActionForm):

    def create(self):
        self.value = None
        self.statistic = self.add(npyscreen.TitleMultiLine,
                                 name="Statistic:",
                                 values=[])

    def beforeEditing(self):
        self.name = "Inbox"
        self.statistic.values = []
        self.print_statistic(self.parentApp.connection, self.parentApp.current_user_id)

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def print_statistic(self, connection, user_id):
        user = connection.hmget("user:%s" % user_id,
                                        ['queue', 'checking', 'blocked', 'sent', 'delivered'])
        # print("In queue: %s\nChecking: %s\nBlocked: %s\nSent: %s\nDelivered: %s" % tuple(user))
        l = ("In queue: %s\nChecking: %s\nBlocked: %s\nSent: %s\nDelivered: %s" % tuple(user)).split("\n")
        self.statistic.values.extend(l)