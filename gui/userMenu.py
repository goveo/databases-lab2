import npyscreen
import atexit
import redis

values_list = ['Send message', 'Inbox messages', 'Statistic', 'Logout']

def sign_out(conn, user_id) -> int:
    return conn.srem("online:", conn.hmget("user:%s" % user_id, ["login"])[0])


class userMenu(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(userMenu, self).__init__(*args, **keywords)
        self.name = "Main List"

    def display_value(self, vl):
        return "{:^80}".format(str(vl))


    def actionHighlighted(self, act_on_this, keypress):
        index = values_list.index(act_on_this)
        if (index == 0):
            self.parent.parentApp.getForm('SEND_MESSAGE').value = None
            self.parent.parentApp.switchForm('SEND_MESSAGE')
        if (index == 1):
            self.parent.parentApp.getForm('INBOX').value = None
            self.parent.parentApp.switchForm('INBOX')
        if (index == 2):
            self.parent.parentApp.getForm('STATISTIC').value = None
            self.parent.parentApp.switchForm('STATISTIC')
        if (index == 3):
            sign_out(self.parent.parentApp.connection, self.parent.parentApp.current_user_id)
            self.parent.parentApp.switchForm('MAIN')


def sign_out(conn, user_id) -> int:
    return conn.srem("online:", conn.hmget("user:%s" % user_id, ["login"])[0])


class userMenuDisplay(npyscreen.FormMutt):

    MAIN_WIDGET_CLASS = userMenu

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        def exit_handler():
            sign_out(self.connection, self.current_user_id)
        atexit.register(exit_handler)

        self.wMain.values = values_list
        self.wMain.display()
        self.signed_in = False
        self.current_user_id = -1
        self.connection = redis.Redis(charset="utf-8", decode_responses=True)

    def exit(self, *args, **keywords):
        self.parentApp.switchForm(None)