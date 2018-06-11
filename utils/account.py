import hashlib
from datetime import datetime


from models.account import User,session,Post



'''代码端数据 -- 密码验证函数 -- 代码版的验证函数 -- 验证用户是否存在 '''




def hash_it(password):
    '''加密 密码'''
    return hashlib.md5(password.encode('utf8')).hexdigest()


def authenticate(username,password):
    '''密码验证  防止用户 输入空 密码'''
    if username and password:
        hash_password =User.get_pass(username)
        if hash_password and hash_it(password)== hash_password:

            return True
    return False




def login(username):
    '''查询'''
    t = datetime.now()
    print('user:{}login at {} '.format(username,t))

    session.query(User).filter_by(name=username).update({User.last_login})
    session.commit()


def register(username,password,email):
    '''验证用户是否存在 ，不存在就添加到数据库'''
    if User.is_exists(username):
        return {'msg':'username already exits'}

    hash_pass = hash_it(password)
    User.add_user(username,hash_pass,email)
    return {'msg':'ok'}


def add_post_for(username, image_url, thumb_url):
    '''保存图片对应的用户信息和存储信息'''
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, user=user, thumb_url=thumb_url)
    session.add(post)
    session.commit()
    return post.id


def get_post_for(username):
    user = session.query(User).filter_by(name=username).first()
    posts = session.query(Post).filter_by(user=user)
    return posts
