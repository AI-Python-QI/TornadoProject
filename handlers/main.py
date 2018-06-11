import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo
from utils.account import add_post_for,get_post_for



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

    @tornado.web.authenticated
    def get(self,*args,**kwargs):


        thumb_images = photo.get_images('./static/upload/images/thumb_images/')
        self.render('explore.html',images=thumb_images)

class PostHandler(AuthBaseHandler):
    ''' post  照片详情页'''
    #def get(self,*args,**kwargs):
        #self.render('post.html',post_id=kwargs['post_id'])
        #self.render('post.html',post_id=post_id)
    def get(self,post_id):
        self.render('post.html',post_id=post_id)


class UploadHandler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        next = self.get_argument('next', '')
        self.render('upload.html', next=next)

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newing', None)
        for img in img_files:
            saver = photo.ImageSave(self.settings['static_path'], img['filename'])
            saver.save_upload(img['body'])
            saver.make_thumb()

            add_post_for(self.current_user, saver.upload_url, saver.thumb_url)
            print('save to {}'.format(saver.upload_path))
            self.redirect('/')

        self.render('upload.html')

        # self.write({'msg':'got file :{}'.format(img_files[0]['filename'])})
        self.write('恭喜您，完成提交！')
        self.redirect('explore')



