import npyscreen
import atexit
import redis

values_list = ['Register', 'Login', 'Exit']


class MainList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(MainList, self).__init__(*args, **keywords)
        self.name = "Main List"

    def display_value(self, vl):
        return "{:^80}".format(str(vl))


    def actionHighlighted(self, act_on_this, keypress):
        index = values_list.index(act_on_this)
        if (index == 0):
            self.parent.parentApp.getForm('REGISTER').value = None
            self.parent.parentApp.switchForm('REGISTER')
        if (index == 1):
            self.parent.parentApp.getForm('LOGIN').value = None
            self.parent.parentApp.switchForm('LOGIN')
            ... #login
        if (index == 2):
            self.sign_out()
            self.parent.parentApp.switchForm(None)


def sign_out(conn, user_id) -> int:
    return conn.srem("online:", conn.hmget("user:%s" % user_id, ["login"])[0])


class MainListDisplay(npyscreen.FormMutt):

    MAIN_WIDGET_CLASS = MainList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        def exit_handler():
            sign_out(self.parentApp.connection, self.parentApp.current_user_id)
        atexit.register(exit_handler)

        self.wMain.values = values_list
        self.wMain.display()

    def exit(self, *args, **keywords):
        self.parentApp.switchForm(None)