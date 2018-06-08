import tornado.web
import time

from .main import AuthBaseHandler
from utils.account import authenticate

class LoginHandler(AuthBaseHandler):
    '''接收用户名和密码，并且验证cookie'''

    def get(self,*args,**kwargs):
        self.render('login.html')

    def post(self,*args,**kwargs):
        username = self.get_argument('username',None)
        password = self.get_argument('password',None)

        passed = authenticate(username,password)

        if passed:
            self.session.set('tudo_user_info',username)
            self.redirect('/')
        else:
            self.write('您的用户名或者密码错误！')

class SignupHandler(AuthBaseHandler):

    def get(self,*args,**kwargs):
        self.render('signup.html')

    def post(self,*args,**kwargs):

        username = self.get_argument('username','')
        email = self.get_argument('email','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')

        if username and password1 and password2:
            if password1 != password2:
                self.write('两次输入的密码不匹配！')
            else:
                pass







