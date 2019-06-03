import npyscreen
import redis

class SendMessage(npyscreen.ActionForm):

    def create(self):
        self.value = None
        self.recipient = self.add(npyscreen.TitleText, name="Recipient:", value='')
        self.message = self.add(npyscreen.TitleText, name="Message:", value='')

    def beforeEditing(self):
        self.name = "Login"
        self.recipient.value = ''
        self.message.value = ''

    def on_ok(self):
        if self.message.value != '' and self.recipient.value != '':
            self.create_message(self.parentApp.connection,
                                self.message.value,
                                self.parentApp.current_user_id,
                                self.recipient.value)
            self.parentApp.switchFormPrevious()


    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()

    def create_message(self, conn, message_text, sender_id, consumer):
        message_id = int(conn.incr('message:id:'))
        consumer_id = int(conn.hget("users:", consumer))

        if not consumer_id:
            # print("Current user does not exist %s, unable to send message" % consumer)
            return -1

        pipeline = conn.pipeline(True)

        pipeline.hmset('message:%s' % message_id, {
            'text': message_text,
            'id': message_id,
            'sender_id': sender_id,
            'consumer_id': consumer_id,
            'status': "created"
        })
        pipeline.lpush("queue:", message_id)
        pipeline.hmset('message:%s' % message_id, {
            'status': 'queue'
        })
        pipeline.zincrby("sent:", 1, "user:%s" % conn.hmget("user:%s" % sender_id, ["login"])[0])
        pipeline.hincrby("user:%s" % sender_id, "queue", 1)
        pipeline.execute()

        return message_id
