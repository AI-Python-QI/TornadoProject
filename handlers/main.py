import tornado.web
import os
from pycket.session import SessionMixin

from utils import photo
from utils.account import add_post_for,get_post_for,get_all_posts,get_post,get_user,get_like_posts,get_like_users,get_count_like




class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):

    def get_current_user(self):
        return self.session.get('tudo_user_info')

class IndexHandler(AuthBaseHandler):
    ''' 网页家目录 index.html'''
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        #images_path = os.path.join(self.settings.get('static_path'),'upload')
        #images = photo.get_images(images_path)
        #image_urls = photo.get_images('./static/upload/images')
        posts = get_all_posts()
        self.render('index.html',posts=posts)#posts已经通过该定义闯入到index.html页面了，网页需要什么变量都需要这么传递
        #例如 拿到 ！！！static_url handler 这些变量不需要传递，会自动传递到这里，可以直接调用


class ExploreHandler(AuthBaseHandler):
    ''' explore.html'''

    @tornado.web.authenticated
    def get(self,*args,**kwargs):


        #thumb_images = photo.get_images('./static/upload/images/thumb_images/')
        posts = get_all_posts()
        #posts = get_post_for(self.current_user)
        self.render('explore.html',posts=posts)

class MysaveHandler(AuthBaseHandler):
    '''我的收藏页面'''
    @tornado.web.authenticated
    def get(self):
        #thumb_images = photo.get_images('./static/upload/images/')
        posts =get_post_for(self.current_user)
        #这个定义为什么要这样子？ 通过self.current_user 这个是拿到的用户名 ，这个用户名传递给了 get_post_for
        #这个定义的函数，这个函数会进行调用查询，返回 user ,然后通过user.post 调用 post数据库
        self.render('my save.html',posts= posts)


class PostHandler(AuthBaseHandler):
    ''' post  照片详情页'''
    #def get(self,*args,**kwargs):
        #self.render('post.html',post_id=kwargs['post_id'])
        #self.render('post.html',post_id=post_id)
    def get(self,post_id):
        post = get_post(int(post_id))
        like_users = get_like_users(post)#拿到喜欢这张图片的用户
        like_user = get_count_like(post)#拿到喜欢这张图片用户的数量
        self.render('post.html',post=post,users=like_users)# 为什么这么定义呢？因为 post_id 已经传入到了 post.html了 向网页内传递变量的方式


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


class ProfileHandler(AuthBaseHandler):
    '''
    显示用户上传的图片和喜欢的图片
    '''
    @tornado.web.authenticated
    def get(self):
        user = get_user(self.current_user)
        like_posts = get_like_posts(user)
        self.render('profile.html',user=user,like_posts=like_posts)




