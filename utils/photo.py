import glob
from PIL import Image
import os


def get_images(path):
    images = []
    for file in glob.glob(path+'/*.jpg'):
        images.append(file)
    return images

def make_thumb(path):
    '''进行缩略图处理'''
    file,ext = os.path.splitext(os.path.basename(path))
    im = Image.open(path)
    im.thumbnail((260,260))
    im.save('./static/upload/thumb_images/{}_{}x{}.jpg'.format(file,200,200),'JPEG')

