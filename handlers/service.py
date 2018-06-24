import  tornado.gen

from .main import AuthBaseHandler
from utils import photo,account




class ImageHandler(AuthBaseHandler):
    '''异步编程 拿到图片的 类'''
    '''3者一起才能组成异步编程 1. AsyncHTTPclient 2. yield 3. @tornado.gen.coroutine'''
    @tornado.gen.coroutine

    def get(self):
        '''图片处理上传'''
        resp = yield self.fetch_images()
        if not resp.body:
            self.write('error data empty')
            return

        img_saver = photo.ImageSave(self.settings['static_path'],'x.jpg')
        img_saver.save_upload(resp.body)
        img_saver.make_thumb()
        post = account.add_post_for(self.current_user,img_saver.upload_url,img_saver.thumb_url)
        self.redirect('/post/{}'.format(post.id))


    def fetch_images(self):
        '''拿到图片的方法 使用内部客户端进行 图片的下载'''
        url = self.get_argument('url',None)
        client = tornado.httpclient.AsyncHTTPClient()
        '''这一步的作用是？'''
        print('---going to fetch :{}'.format(url))
        resp = client.fetch(url)
        return resp










class SyncImageHandler(AuthBaseHandler):
    '''同步编程 拿到图片的 类'''
    def get(self):
        '''图片处理上传'''
        resp = yield self.fetch_images()
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

