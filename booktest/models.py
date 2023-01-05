from django.db import models
import datetime,time
# Create your models here.

# 账号
class people(models.Model):

    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)

    # 账号创建时间
    create_time = models.DateField(default = datetime.date.today())

    # 获取时间戳
    time_stamp = models.FloatField(default = time.time())

    objects = models.Manager()

    def __str__(self):
        return self.username

# 商品列表
class goods(models.Model):

    # 商品名称
    goods_name = models.CharField(max_length=30)
    # 商品价格
    goods_price = models.IntegerField()
    # 商品分类
    goods_type = models.CharField(max_length=30,default='all')
    # 商品图片路径
    goods_photo = models.CharField(max_length=80)
    # 商品管理对象
    objects = models.Manager()
    # 介绍内容
    info = models.TextField(default='商品暂无介绍信息')

    def __str__(self):
        return self.goods_name

# 购物车商品列表模型
class buy_car(models.Model):
     '''购物车商品列表模型'''
     # 商品名称
     goods_name = models.CharField(max_length=30)
     # 商品价格
     goods_price = models.IntegerField()
     # 商品分类
     goods_type = models.CharField(max_length=30,default='all')
     # 商品图片路径
     goods_photo = models.CharField(max_length=80)
     # 商品管理对象
     objects = models.Manager()
     # 外键对应账号表
     p_id = models.ForeignKey('people',on_delete=models.CASCADE,default='')
     #  外键对应商品表
     g_id = models.IntegerField()

     def __str__(self):
         return self.goods_name

# 商品种类表
class type(models.Model):
    '''商品种类表'''
    # 种类名称
    type_name = models.CharField(max_length=30)

    objects = models.Manager()


# 所有省市县
# CREATE TABLE `city` (
#   `id` int(11) NOT NULL DEFAULT '0',
#   `pid` int(11) DEFAULT NULL,
#   `cityname` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
#   `type` int(11) DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

class city(models.Model):
    '''所有省市县'''
    pid = models.IntegerField(default='null')
    cityname = models.CharField(max_length=255,default='null')
    type = models.IntegerField(default='null')

    objects = models.Manager()


# 用户地址模块
class user_address(models.Model):
    '''用户地址'''

    # 收件人姓名
    user_name = models.CharField(max_length=255,default='')
    # 收件人电话号码
    user_phone = models.CharField(max_length=22,default='')
    # 收件人省份
    user_sheng = models.CharField(max_length=60,default='')
    # 收件人市区
    user_shi = models.CharField(max_length=60,default='')
    # 收件人县城
    user_xian = models.CharField(max_length=60,default='')
    # 收件人详细地址
    user_deAddress = models.CharField(max_length=60,default='')
    # 设置默认收货地址  1为默认
    user_default_address = models.IntegerField(default=0)
    # 收件人对应的用户id
    address_id = models.ForeignKey('people',on_delete=models.CASCADE)

    objects = models.Manager()

# 该表已经迁移至商品表
# # 商品介绍信息 对应商品表
# class goods_intriduce(models.Model):
#     '''商品介绍'''
#
#     # 介绍内容
#     info = models.TextField(default='商品暂无介绍信息')
#
#     # 外键对应商品
#     info_id = models.ForeignKey('goods',on_delete=models.CASCADE)

