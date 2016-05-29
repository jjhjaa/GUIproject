from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
import MySQLdb
import os

#  Luodaan yhteys SQL tietokantaan

db = MySQLdb.connect(host="Localhost",
                     user="root",
                     passwd="",
                     db="housedb")

##   Nimetaan cursori kaytettavaampaan muotoon

query = db.cursor()

class Connected(Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()


#  Kivy vaatii luokan textinputille seka screenmanagementille joilla myohemmin hallinnoidaan Screeneja seka textinputtien dataa

class TextInput(TextInput):
    pass


class ScreenManagement(ScreenManager):
    pass


#  Kirjautumis Screeni haetaan kivun puolelta textinputteihin tullut data ja tarkistetaan SQL tietokannasta kyselylla matchaako tiedot

class Login(Screen):

    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        if(query.execute("SELECT * FROM `USERS` WHERE `username`='" + app.username + "' AND `password`='" + app.password + "'")):
            db.commit()
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'connected'
        elif loginText == "admin" and passwordText == "admin":
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'adminpanel'
        else:
            app.config.read(app.get_application_config())
            app.config.write()

    #  ylhaalla kaytetaan resetFormia jolla tyhjataan syottokentat

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""


# Luodaan luokat jokaiselle Screenille erikseen ja asetetaan toivottuja parametreja
class Koti(Screen):
    def koti(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'koti'
        self.manager.get_screen('koti')


class Huvila(Screen, TabbedPanel):
    def huvila(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'huvila'
        self.manager.get_screen('huvila')


class Makuuhuone(Screen, TabbedPanel):
    def makuuhuone(self):
        self.manager.transition = SlideTransition(direction="right")
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
        self.manager.get_screen('adminpanel')

#  Luodaan luokka uuden kayttajan syottamisella, kivy puolella kutsutaan do_insert luokkaa joka kayttaa SQL kyselya textinputista saatujen tietojen siirtamiseen tietkantaan
class Insert(Screen):
    def do_insert(self, do_username, do_password):

        try:
            query.execute("INSERT INTO `users`(`username`, `password`) VALUES ('{}','{}')".format(do_username, do_password))
            db.commit()
            self.resetForm()

        except MySQLdb.Error as e:
            print("Error {}".format(e))

    def resetForm(self):
        self.ids['username'].text = ""
        self.ids['password'].text = ""

# Luodaan luokka salasanan vaihdolle, kivy puolelta kutsutaan do_change metodia joka pyorayttaa taas SQL kyselyn salasanan paivittamiselle, mikali username on oikein.
class Changepw(Screen):
    def do_change(self, do_username, do_newpassword):

        try:
            print(do_newpassword)
            query.execute("UPDATE `users` SET `password`=('{}') WHERE `username`=('{}')".format(do_newpassword, do_username))
            db.commit()
            self.resetForm()

        except MySQLdb.Error as e:
            print("Error {}".format(e))


    def resetForm(self):
        self.ids['username'].text = ""
        self.ids['newpassword'].text = ""


        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'changepw'
        self.manager.get_screen('changepw')

# Luodaan loginappi joka alustaa login id:den ominaisuuden

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)
    do_username = StringProperty(None)
    do_password = StringProperty(None)
    do_newpassword = StringProperty(None)

#  metodi widgeteille ja screenmanagerille, joka tarvitaan kivy puolen toimintaan mennessa screenista toiseen.
    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(Koti(name='koti'))
        manager.add_widget(Makuuhuone(name='makuuhuone'))
        manager.add_widget(Olohuone(name='olohuone'))
        manager.add_widget(Adminpanel(name='adminpanel'))
        manager.add_widget(Huvila(name="huvila"))
        manager.add_widget(Insert(name="insert"))
        manager.add_widget(Changepw(name="changepw"))

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






