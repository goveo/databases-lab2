import npyscreen
import redis

class Inbox(npyscreen.ActionForm):

    def create(self):
        self.value = None
        # self.recipient = self.add(npyscreen.TitleText, name="Recipient:", value='')
        # self.message = self.add(npyscreen.TitleText, name="Message:", value='')
        self.inbox = self.add(npyscreen.TitleMultiLine,
                                 name="Inbox:",
                                 values=[])

    def beforeEditing(self):
        self.name = "Inbox"
        self.inbox.values = []
        self.print_messages(self.parentApp.connection, self.parentApp.current_user_id)


    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def print_messages(self, connection, user_id):
        messages = connection.smembers("sentto:%s" % user_id)
        for message_id in messages:
            message = connection.hmget("message:%s" % message_id, ["sender_id", "text", "status"])
            sender_id = message[0]
            self.inbox.values.append("%s: %s" % (connection.hmget("user:%s" % sender_id, ["login"])[0], message[1]))
            if message[2] != "delivered":
                pipeline = connection.pipeline(True)
                pipeline.hset("message:%s" % message_id, "status", "delivered")
                pipeline.hincrby("user:%s" % sender_id, "sent", -1)
                pipeline.hincrby("user:%s" % sender_id, "delivered", 1)
                pipeline.execute()