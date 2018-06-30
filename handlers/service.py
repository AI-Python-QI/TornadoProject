import  tornado.gen
from datetime import  datetime
import uuid
import tornado.escape
import tornado.httpclient

from .main import AuthBaseHandler
from utils import photo,account
from .chat import ChatSocketHandler






class ImageHandler(AuthBaseHandler):
    '''异步编程 拿到图片的 类 /save'''
    '''3者一起才能组成异步编程 1. AsyncHTTPclient 2. yield 3. @tornado.gen.coroutine'''
    @tornado.gen.coroutine
    def get(self):
        '''图片处理上传'''
        url = self.get_argument('url',None)# 取？url= 的值
        post_user = self.get_argument('user',None)
        is_room = self.get_argument('from',None) == 'room'

        print('---时间：{}  fetch :{}'.format(datetime.now(),url))
        if not (post_user and is_room):
            print('no user and room')
            return

        resp = yield self.fetch_images(url)
        if not resp.body:
            self.write('error data empty')
            return

        img_saver = photo.ImageSave(self.settings['static_path'],'x.jpg')
        img_saver.save_upload(resp.body)
        img_saver.make_thumb()
        post = account.add_post_for(post_user,img_saver.upload_url,img_saver.thumb_url)
        #添加到数据库，拿到post实例
        print('--{} -end fetch:#{}'.format(datetime.now(),post.id))

        chat = {
            'id': str(uuid.uuid4()),
            'sent_by': 'admin',
            'body': '{} post:{}'.format(post_user,
    'http://192.168.31.128:8080/post/{}'.format(post.id)),
            'img': post.thumb_url,
        }

        chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', message=chat))


        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
        print('message sent !')
        #self.redirect('/post/{}'.format(post.id))

    @tornado.gen.coroutine
    def fetch_images(self,url):
        '''拿到图片的方法 使用内部客户端进行 图片的下载'''

        client = tornado.httpclient.AsyncHTTPClient()
        '''这一步的作用是？'''
        print('---时间：{} going to fetch :{}'.format(datetime.now(),url))
        resp = yield client.fetch(url)
        return resp










class SyncImageHandler(AuthBaseHandler):
    '''同步编程 拿到图片的 类'''
    def get(self):
        '''图片处理上传'''
        resp = self.fetch_images()
        if not resp.body:
            self.write('error data empty')
            return

        img_saver = photo.ImageSave(self.settings['static_path'],'x.jpg')
        ''' 保存路径 和文件名称'''
        img_saver.save_upload(resp.body)
        '''保存 文件 body 是tornado自带的特殊功能。存放的是文件的二进制字符'''
        img_saver.make_thumb()
        '''制作图片 调用的是 原来写的方法函数，隶属于ImageSave 类下的方法'''
        post = account.add_post_for(self.current_user,img_saver.upload_url,img_saver.thumb_url)
        '''把信息添加进入数据库 img_saver.upload_url 为ImageSave的方法，在此处进行了调用 '''

        self.redirect('/post/{}'.format(post.id))
        '''把得到的post.id传入进去'''








    def fetch_images(self):
        '''拿到图片的方法 使用内部客户端进行 图片的下载'''
        url = self.get_argument('url',None)
        client = tornado.httpclient.HTTPClient()
        '''这一步的作用是？'''
        print('---going to fetch :{}'.format(url))
        resp = client.fetch(url)
        return resp

