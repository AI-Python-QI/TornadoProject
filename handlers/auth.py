import tornado.web
import time

from .main import AuthBaseHandler
from utils.account import authenticate,register,login,hash_it,User

'''用于注册登陆 的  Handler 函数  loginHandler signupHandler '''


class LoginHandler(AuthBaseHandler):
    '''接收用户名和密码，并且验证cookie'''

    def get(self,*args,**kwargs):
        if self.current_user:
            self.redirect('/')
        next = self.get_argument('next','/')

        self.render('login.html',next=next)

    def post(self,*args,**kwargs):
        username = self.get_argument('username',None)
        password = self.get_argument('password',None)

        passed = authenticate(username,password)
        print(username,password,hash_it(password))
        print(User.get_pass(username))

        if passed:
            self.session.set('tudo_user_info',username)

            '''更新登陆时间'''
            self.redirect('/')
        else:
            self.write('用户名或者密码错误！！！请重新输入！')
            self.render('login.html')
class LogoutHandler(AuthBaseHandler):
    '''登出函数'''
    def get(self,*args,**kwargs):
        self.session.set('tudo_user_info','')
        self.redirect('/login')

class SignupHandler(AuthBaseHandler):
    '''注册函数'''

    def get(self,*args,**kwargs):
        self.render('signup.html',msg ='')

    def post(self):

        username = self.get_argument('username','')
        email = self.get_argument('email','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')
        print(username,password1,email,password2)

        if username and password1 and password2:
            if password1 != password2:
                self.write('两次输入的密码不匹配！！！')
            else:
                ret = register(username,password1,email)
                if ret['msg'] == 'ok':
                    self.session.set('tudo_user_info',username)
                    self.redirect('/')

                else:
                    self.write(ret)
        else:
            self.render('signup.html',msg={'register fail'})







