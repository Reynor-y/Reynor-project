from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

#如果想要给默认的User拓展字段，可以创建一个model使用一对一外键与User连接起来


class ImageInfo(models.Model):
    #表情包数据表结构
    # 设置浏览器访问路径
    # MEDIA_URL = '/image/'
    # 指定文件上传存储目录
    # MEDIA_ROOT = os.path.join(BASE_DIR, 'image')
    # null=True blank=True 设置可以为空，默认值为False upload_to参数可选，如果设置则上传到MEDIA_ROOT + upload_to
    #postman会使MEDIA_ROOT失效
    src = models.ImageField(verbose_name='表情包存储路径',default='',upload_to="meme_image/",unique=True)
    
    #DateTimeField 存储日期和时间的字段
    #参数：auto_now 数据保存时自动记录当前时间，调用.save()时才会更新，.updatea()不会更新
    #auto_now_add 数据第一次被储存进去时自动记录当前时间
    upload_date = models.DateTimeField(verbose_name='上传时间',default=datetime.now)
    
    #外链链接的model如果是已经定义过的可以直接使用对象，如果没有定义可以使用字符串类型的model名称
    upload_user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='上传用户')
    
    likes = models.IntegerField(verbose_name='点赞数',default='0')
    #储存评论的字段，TextField采用varchar，变长储存，在无需修改的情况下可以节省空间
    # comments = models.TextField(max_length=120,verbose_name='评论',null=True,blank=True,default='')
    # created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    '''
    自定义表名需要使用class Mate中的db_table参数
    class Mate:
       db_table = 'imageinfo'
    '''
    class Mate:
       db_table = 'imageinfo'
       verbose_name='图片信息'
       verbose_name_plural=verbose_name
       ordering=['-order_date']
class Tags(models.Model):
    #表情包标签数据表结构，以供分类、推荐及检索
    #与表情包为多对多关系
    tag_name = models.CharField(max_length=8,default='',unique=True)
    images = models.ManyToManyField(ImageInfo)

class UserExtension(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='extension')
    liked_tags = models.ForeignKey(Tags,on_delete=models.CASCADE,verbose_name='喜欢的标签')
# class ImageInfoAndTags(models.Model):
#     #表情包信息和标签关系表
#     relation_id = models.AutoField(primary_key=True)
#     image = models.ForeignKey(ImageInfo,on_delete=models.DO_NOTHING)
#     tag = models.ForeignKey(Tags,on_delete=models.DO_NOTHING)
    '''
    on_delete参数
    CASCADE:这就是默认的选项，级联删除，你无需显性指定它。
    PROTECT: 保护模式，如果采用该选项，删除的时候，会抛出ProtectedError错误。
    SET_NULL: 置空模式，删除的时候，外键字段被设置为空，前提就是blank=True, null=True,定义该字段的时候，允许为空。
    SET_DEFAULT: 置默认值，删除的时候，外键字段设置为默认值，所以定义外键的时候注意加上一个默认值。
    SET(): 自定义一个值，该值当然只能是对应的实体了
    DO_NOTHING
    '''