from datetime import datetime
from sqlalchemy import (Column,Integer,String,DateTime,ForeignKey)
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship

from models.db import Base,DBSession

'''建表 -- 查询是否存在 -- 添加到数据库操作'''

session = DBSession()
'''初始化'''

class User(Base):
    '''建立user表'''
    __tablename__ = 'users'

    id =Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(150),unique=True,nullable=False)
    password = Column(String(150),nullable=False)
    created = Column(DateTime,default=datetime.now)
    '''此处的datetiem.now 为什么不需要执行，因为是传这个参数进去'''
    email = Column(String(150))
    last_login = Column(DateTime)


    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id,self.name)

    '''验证用户是否存在'''
    @classmethod
    def is_exists(cls,username):
        return session.query(exists().where(User.name==username)).scalar()

    '''执行添加到数据库的操作函数'''
    @classmethod
    def add_user(cls,username,password,email=''):
        user = User(name=username,password = password,email=email,last_login=datetime.now())
        '''此处的datetiem.now() 是需要执行的，在数据库中的定义不需要执行'''
        '''为什么要执行？因为要生成一个实例'''
        session.add(user)
        session.commit()

    '''查询数据库有没有密码'''
    @classmethod
    def get_pass(cls,username):
        user = session.query(cls).filter_by(name = username).first()
        if user:
            return user.password
        else:
            return ''

class Post(Base):
    '''图片地址存储信息'''

    __tablename__ = 'posts'

    id  = Column(Integer,primary_key=True,autoincrement=True)
    '''自增长的id值'''
    image_url = Column(String(150))
    thumb_url = Column(String(150))
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',backref='posts',cascade='all' ,uselist=False)
    created = Column(DateTime,default=datetime.now)

    def __repr__(self):
        return '<Post(#{}:{})>'.format(self.image_url, self.id)




class Like(Base):
    '''增加用户关注的图片列表'''
    __tablename__ = 'likes'

    post_id =  Column(Integer,ForeignKey('posts.id'),nullable=False,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False,primary_key=True)
#     @classmethod
#     def add_likes(cls,post_id,user_id):
#         '''往likes数据库 进行添加喜欢的图片的记录
#             做一个提交的表单进行添加记录 简化版：通过命令进行添加删除
#             做一个删除的表单进行删除的记录
#
#         '''
#         likes = cls(post_id=post_id, user_id=user_id)
#         session.add(likes)
#         session.commit()
# Like.add_likes(post_id=9,user_id=9)

if __name__ == '__main__':
    Base.metadata.create_all()
