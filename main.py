import redis
import npyscreen
from gui import mainList
from gui import register as registerForm
from gui import login
from gui import userMenu
from gui import sendMessage
from gui import inbox
from gui import statistic


class App(npyscreen.NPSAppManaged):
    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)

    def onStart(self):
        self.signed_in = False
        self.current_user_id = -1
        self.connection = redis.Redis(charset="utf-8", decode_responses=True)

        # self.connection.flushall()

        self.addForm("MAIN", mainList.MainListDisplay, title='Main menu')
        self.addForm("REGISTER", registerForm.Register, title='Register')
        self.addForm("LOGIN", login.Login, title='Login')
        self.addForm("USER_MENU", userMenu.userMenuDisplay, title='User menu')
        self.addForm("SEND_MESSAGE", sendMessage.SendMessage, title='Send message')
        self.addForm("INBOX", inbox.Inbox, title='Inbox')
        self.addForm("STATISTIC", statistic.Statistic, title='Statistic')

    def onCleanExit(self):
        ...

if __name__ == '__main__':
    MyApp = App()
    MyApp.run()
