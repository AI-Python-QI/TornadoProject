import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo

class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):

    def get_current_user(self):
        return self.session.get('tudo_user_info')

class IndexHandler(AuthBaseHandler):
    ''' 网页家目录 index.html'''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        #images_path = os.path.join(self.settings.get('static_path'),'upload')
        #images = photo.get_images(images_path)
        image_urls = photo.get_images('./static/upload/images')
        self.render('index.html',images = image_urls)


class ExploreHandler(AuthBaseHandler):
    ''' explore.html'''
    def get(self,*args,**kwargs):


        thumb_images = photo.get_images('./static/upload/thumb_images/')
        self.render('explore.html',images=thumb_images)

class PostHandler(AuthBaseHandler):
    ''' post  照片详情页'''
    #def get(self,*args,**kwargs):
        #self.render('post.html',post_id=kwargs['post_id'])
        #self.render('post.html',post_id=post_id)
    def get(self,post_id):
        self.render('post.html',post_id=post_id)


class UploadHanlder(AuthBaseHandler):
    '''接收图片文件上传'''

    def get(self,*args,**kwargs):
        self.render('upload.html')

    def post(self,*args,**kwargs):
        img_files = self.request.files.get('newing',None)
        if img_files:
            for img_file in img_files:
                with open ('./static/upload/images/'+img_file['filename'],'wb') as f:
                    f.write(img_file['body'])
                photo.make_thumb('./static/upload/images/'+img_file['filename'])

        else:
            self.write('不好意思，发生错误辣！')
        self.write({'msg':'got file :{}'.format(img_files[0]['filename'])})
        self.write('恭喜您，完成提交！')
        self.redirect('explore')

class LogoutHandler(AuthBaseHandler):

    def get(self,*args,**kwargs):
        self.session.set('tudo_user_info','')
        self.redirect('/login')

class IndexxHandler(AuthBaseHandler):

    def get(self):
        self.render('indexx.html')