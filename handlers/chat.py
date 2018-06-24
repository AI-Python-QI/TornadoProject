import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import uuid

from .main import AuthBaseHandler


class RoomHandler(AuthBaseHandler):
    '''
    聊天室界面

    '''
    def  get(self):
        self.render('room.html',messages = ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    '''注意此处的继承'''
    waiters = set()#集合 等待接收信息的用户
    cache = []# 存放信息的列表
    cache_size = 200  #存放信息的个数

    def get_compression_options(self):
        '''非None的返回值开启压缩  此处为重写覆盖 但是会自动调用'''
        return {}

    def open(self):
        '''新的连接打开'''
        logging.info('new connection %s'%self)
        ChatSocketHandler.waiters.add(self) #有了连接 就加入 集合

    def on_close(self):
        '''连接断开'''
        ChatSocketHandler.waiters.remove(self)#连接断开，从字典删除连接

    @classmethod  #传进来的是类本身，这就有意思了，类有一个属性cache 所有 cls.cache.append() 对cache操作
    def update_cache(cls,chat):
        '''新的信息列表，加入新的信息'''
        cls.cache.append(chat)
        if len(cls.cache)> cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]#如果信息的长度大于200，则进行切片，从后往前切200

    @classmethod
    def send_updates(cls,chat):
        '''给每一个等待接收的用户发新的消息 logging 类似于print'''
        logging.info('sending messages to %d waiters',len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)#websocket自带功能 主要的功能是 服务器发信息给客户端，
            except:
                logging.error('Error sending messages',exc_info=True)

    def on_message(self, message):
        '''websocket 服务器端接收的信息 '''
        logging.info('got messages %r',message)
        parsed = tornado.escape.json_decode(message)#解码
        chat = {
                'id':str(uuid.uuid4()),
                'body':parsed['body'],
        }
        chat['html']=tornado.escape.to_basestring(self.render_string('message.html',message=chat))



        ChatSocketHandler.update_cache(chat)#这样子写才可以访问到全局的
                                            #每个实例都有一个自己的
        ChatSocketHandler.send_updates(chat)














