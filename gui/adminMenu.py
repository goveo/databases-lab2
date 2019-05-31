import npyscreen
import atexit
import redis

values_list = ['Online users', 'Top senders', 'Top spamers', 'Exit']

def sign_out(conn, user_id) -> int:
    return conn.srem("online:", conn.hmget("user:%s" % user_id, ["login"])[0])


class adminMenu(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(adminMenu, self).__init__(*args, **keywords)
        self.name = "Admin menu"

    def display_value(self,  vl):
        return "{:^80}".format(str(vl))


    def actionHighlighted(self, act_on_this, keypress):
        select = values_list.index(act_on_this)
        if (select == 0):
            online_users = self.parent.parentApp.connection.smembers("online:")
            users = ""
            for user in online_users:
                users += "{}\n".format(user)
            self.spawn_online_users_popup(users)

        if (select == 1):
            senders = self.parent.parentApp.connection.zrange("sent:", 0, 10 - 1, desc=True, withscores=True)
            result = ""
            for i, sender in enumerate(senders):
                result += "{}. {} - {} messages\n".format(i + 1, sender[0], int(sender[1]))
            self.spawn_top_senders_popup(result)

        if (select == 2):
            spamers = self.parent.parentApp.connection.zrange("spam:", 0, 10 - 1, desc=True, withscores=True)
            result = ""
            for i, spamer in enumerate(spamers):
                result += "{}. {} - {} spam messages\n".format(i + 1, spamer[0], int(spamer[1]))
            self.spawn_top_spamers_popup(result)

        if (select == 3):
            sign_out(self.parent.parentApp.connection, self.parent.parentApp.current_user_id)
            self.parent.parentApp.switchForm(None)

    def spawn_online_users_popup(self, users_string):
        npyscreen.notify_confirm(users_string, title='Users online')

    def spawn_top_senders_popup(self, senders_string):
            npyscreen.notify_confirm(senders_string, title='Top 10 senders')

    def spawn_top_spamers_popup(self, spamers_string):
            npyscreen.notify_confirm(spamers_string, title='Top 10 spamers')



def sign_out(conn, user_id) -> int:
    return conn.srem("online:", conn.hmget("user:%s" % user_id, ["login"])[0])


class adminMenuDisplay(npyscreen.FormMutt):

    MAIN_WIDGET_CLASS = adminMenu

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