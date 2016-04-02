from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
import os


class Connected(Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()


class TextInput(TextInput):
    pass


class ScreenManagement(ScreenManager):
    pass





class Login(Screen):

    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        if loginText == "admin" and passwordText == "admin":
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'adminpanel'
        elif loginText == "oispa" and passwordText == "kaljaa":
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'connected'
        else:

            app.config.read(app.get_application_config())
            app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""


class Koti(Screen):
    def koti(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'koti'
        self.manager.get_screen('koti')


class Makuuhuone(Screen, TabbedPanel):
    def makuuhuone(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'makuuhuone'
        self.manager.get_screen('makuuhuone')


class Olohuone(Screen, TabbedPanel):
    def olohuone(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'olohuone'
        self.manager.get_screen('olohuone')


class Adminpanel(Screen):
    def adminpanel(self):
        self.manager.transition = FadeTransition
        self.manager.current = 'adminpanel'
        self.managet.get_screen('adminpanel')


class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(Koti(name='koti'))
        manager.add_widget(Makuuhuone(name='makuuhuone'))
        manager.add_widget(Olohuone(name='olohuone'))
        manager.add_widget(Adminpanel(name='adminpanel'))


        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    LoginApp().run()






