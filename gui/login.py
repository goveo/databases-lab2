import npyscreen
import redis

def sign_in(conn, username) -> int:
    user_id = conn.hget("users:", username)

    if not user_id:
        print("Current user does not exist %s" % username)
        return -1

    conn.sadd("online:", username)
    return int(user_id)


class Login(npyscreen.ActionForm):

    def create(self):
        self.value = None
        self.connection = redis.Redis(charset="utf-8", decode_responses=True)
        self.login = self.add(npyscreen.TitleText, name="Username:", value='')

    def beforeEditing(self):
        self.name = "Login"
        self.login.value = ''

    def on_ok(self):
        if self.login.value == '':
            ...
        else:
            self.parentApp.current_user_id = sign_in(self.connection, self.login.value )

            if self.parentApp.current_user_id != -1:
                self.connection.publish('users', "User %s signed in"
                                   % self.connection.hmget("user:%s" % self.parentApp.current_user_id, ["login"])[0])
                self.parentApp.switchForm("USER_MENU")
            else:
                self.spawn_notify_popup(self.login.value)

    def spawn_notify_popup(self, username):
        npyscreen.notify_confirm("User '{}' does not exist".format(username), title='Info box')

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
