import glob,uuid
from PIL import Image
import os

from models.account import User,session,Post


def get_images(path):
    images = []
    for file in glob.glob(path+'/*.jpg'):
        images.append(file)
    return images

#def make_thumb(path):
    #'''进行缩略图处理'''
    # file,ext = os.path.splitext(os.path.basename(path))
    # im = Image.open(path)
    # im.thumbnail((260,260))
    # im.save('./static/upload/thumb_images/{}_{}x{}.jpg'.format(file,200,200),'JPEG')

    # dirname = os.path.dirname(path)  # 路径 制作  保存
    # file, ext = os.path.splitext(os.path.basename(path))
    #
    # im = Image.open(dirname)
    # size=(200,200)
    # im.thumbnail(size)
    # save_thumb_to = os.path.join(dirname,'upload','thumb_imgages','{}_{}_{}.jpg'.format(file,*size))
    # im.save(save_thumb_to,'JPEG')
    #return save_thumb

class ImageSave(object):
    upload_dir = 'upload/images'
    thumb_dir = 'thumb_images'
    size = (200, 200)

    def __init__(self, static_path, old_name):
        '''
        记录保存图片的路径
        :param static_path: app settings static_path (图片保存服务器的路径)
        :param name: 图片名字
        '''
        self.static_path = static_path
        self.old_name = old_name
        self.new_name = self.gen_name()

    def gen_name(self):
        '''
        生成随记字符串的文件名 并 加上后缀名
        :return:
        '''
        _,ext = os.path.splitext(self.old_name)
        return uuid.uuid4().hex +ext


    @property
    def upload_url(self):  #给web服务器的路径 保存的是相对路径
        return os.path.join(self.upload_dir, self.new_name)  # uploads/images/*jpg     (用于保存数据库是用的路径)

    @property
    def upload_path(self):# 给文件系统的路径，保存的是文件的绝对路径
        return os.path.join(self.static_path, self.upload_url)  # static/uploads/images/*.jpg

    def save_upload(self, content):
        with open(self.upload_path, 'wb') as f:
            f.write(content)

    @property
    def thumb_url(self):
        base, _ = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}.jpg'.format(base, self.size[0], self.size[1])
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)  # uploads/images/thumbnails_200x200/{}_{}_{}.jpg

    def make_thumb(self):
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        im.save(os.path.join(self.static_path, self.thumb_url), 'JPEG')






