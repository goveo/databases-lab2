import npyscreen
import redis

def register(conn, username):
    if conn.hget('users:', username):
        return None

    user_id = conn.incr('user:id:')

    pipeline = conn.pipeline(True)

    pipeline.hset('users:', username, user_id)

    pipeline.hmset('user:%s' % user_id, {
        'login': username,
        'id': user_id,
        'queue': 0,
        'checking': 0,
        'blocked': 0,
        'sent': 0,
        'delivered': 0
    })
    pipeline.execute()
    return user_id


class Register(npyscreen.ActionForm):

    def create(self):
        self.value = None
        self.connection = redis.Redis(charset="utf-8", decode_responses=True)
        self.wgText = self.add(npyscreen.TitleText, name="Username:", value='')
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.name = "Register"
        self.wgText.value = ''

    def on_ok(self):
        if self.wgText.value == '':
            ...
        else:
            register(self.connection, self.wgText.value)
            self.parentApp.switchForm("MAIN")


    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()