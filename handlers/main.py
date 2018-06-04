import tornado.web
import os

from utils import photo

class IndexHandler(tornado.web.RequestHandler):
    ''' 网页家目录 index.html'''
    def get(self,*args,**kwargs):
        images_path = os.path.join(self.settings.get('static_path'),'upload')
        images = photo.get_images(images_path)
        self.render('index.html',images = images)


class ExploreHandler(tornado.web.RequestHandler):
    ''' explore.html'''
    def get(self,*args,**kwargs):
        thumb_images = photo.get_images()
        self.render('explore.html',images=thumb_images)

class PostHandler(tornado.web.RequestHandler):
    ''' post  照片详情页'''
    #def get(self,*args,**kwargs):
        #self.render('post.html',post_id=kwargs['post_id'])
        #self.render('post.html',post_id=post_id)
    def get(self,post_id):
        self.render('post.html',post_id=post_id)


class UploadHanlder(tornado.web.RequestHandler):
    '''接收图片文件上传'''

    def get(self,*args,**kwargs):
        self.render('upload.html')

    def post(self,*args,**kwargs):
        img_files = self.request.files.get('newing',None)
        if img_files:
            for img_file in img_files:
                with open ('./static/upload/images/'+img_file['filename'],'wb') as f:
                    f.write(img_file['body'])
        else:
            self.write('不好意思，发生错误辣！')
        self.write({'msg':'got file :{}'.format(img_files[0]['filename'])})
        self.write('恭喜您，完成提交！')

