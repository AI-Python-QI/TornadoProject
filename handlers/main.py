import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    ''' 网页家目录 index.html'''
    def get(self,*args,**kwargs):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    ''' explore.html'''
    def get(self,*args,**kwargs):
        self.render('explore.html')

class PostHandler(tornado.web.RequestHandler):
    ''' post  照片详情页'''
    #def get(self,*args,**kwargs):
        #self.render('post.html',post_id=kwargs['post_id'])
        #self.render('post.html',post_id=post_id)
    def get(self,post_id):
        self.render('post.html',post_id=post_id)