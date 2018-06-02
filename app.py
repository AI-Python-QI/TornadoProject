import tornado.ioloop
import  tornado.options
import tornado.web
from tornado.options import define,options

from handlers import main

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

        ]
        settings = dict(
            debug = True,
            template_path = 'templates',
            static_path = 'static'
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
