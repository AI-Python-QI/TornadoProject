import os
import tornado.ioloop
import  tornado.options
import tornado.web
from tornado.options import define,options

from handlers import main,auth,chat,service
define('port',default='8080',help='Listening port ',type=int)

class Application(tornado.web.Application):
    '''
    重新定义Application的 __init__方法
    '''
    def  __init__(self):
        handlers = [
            (r'/',main.IndexHandler),
            (r'/explore',main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)',main.PostHandler),
            (r'/upload',main.UploadHandler),
            (r'/login',auth.LoginHandler),
            (r'/logout',auth.LogoutHandler),
            (r'/signup',auth.SignupHandler),
            (r'/mysave',main.MysaveHandler),
            (r'/room',chat.RoomHandler),
            (r'/ws',chat.ChatSocketHandler),
            (r'/save',service.SyncImageHandler),
            (r'/saves',service.ImageHandler),



        ]
        settings = dict(
            debug = True,
            template_path = 'templates',
            static_path = 'static',
            login_url = '/login',
            #static_path = os.path.join(os.path.dirname(__file__),'static'),
            cookie_secret = '1235429845dasdf',
            pycket ={
                'engine':'redis',
                'storage':{
                    'host':'192.168.31.128',
                    'port':6379,
                    'db_sessions':5,
                    'db_notifications':11,
                    'max_connections':2**31,
                },
                'cookies':{
                    'expires_days':30,
                },
            }
        )
        super(Application, self).__init__(handlers,**settings)


application = Application()
'''调用函数'''

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print('Server start on port {}'.format(str(options.port)))
    print('success!')
    tornado.ioloop.IOLoop.current().start()
