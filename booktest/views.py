import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from booktest import models
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math
# Create your views here.

def index(request,login=''):

    # 验证码
    # 随机字母:
    def rndChar():
        return chr(random.randint(65, 90))

    # 随机颜色1:
    def rndColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    list = []
    for t in range(4):
        str = rndChar()
        list.append(str)
        draw.text((60 * t + 10, 10), str, font=font, fill=rndColor2())

    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save(r'C:\Users\TL\jd\static\image\code.jpg', 'jpeg')

    # 结果
    pwd = (''.join(list))

    try:
        str = request.COOKIES['un']
    except:
        str = '请输入用户名'
    try:
        false = request.COOKIES['false'].encode('latin-1').decode('utf-8')
    except:
        false = ''

    # try:
    #     info = request.COOKIES['info'].encode('latin-1').decode('utf-8')
    # except:
    #     info = '注册失败!'

    response = render(request, 'login/index.html', {'str': str, 'false': false, 'login': login, 'code': pwd})
    response.set_cookie('code',pwd)
    return response

def index1(request):
    # cat = models.goods.objects.get(id = 1)
    # name = cat.goods_name
    # price = cat.goods_price
    # goods_photo = cat.goods_photo

    # # 获取所有的类型
    # all_type = models.type.objects.all()

    # 所有商品
    all = models.goods.objects.all()

    # 猫类型的商品
    cat = models.goods.objects.filter(goods_type = 'cat')

    # 狗类型的商品
    dog = models.goods.objects.filter(goods_type = 'dog')

    # 水獭类型的商品
    otter = models.goods.objects.filter(goods_type = 'otter')


    # 获取一共的数量
    sum = math.ceil(len(all)/5)*433
    # {'name': name, 'price': price, 'goods_photo': goods_photo}
    return render(request,'login/index1.html',{'all':all,'sum':sum,'cat':cat,'dog':dog,'otter':otter})


def login_check(request):
    in_username = request.POST.get('username')
    in_password = request.POST.get('password')
    check = request.POST.get('check')
    in_code = request.POST.get('code')
    try:
        user = models.people.objects.get(username = in_username)
        code = request.COOKIES['code']
    except:
        false = HttpResponseRedirect('index')
        false.set_cookie('false',('账号或密码或验证码错误').encode("utf-8").decode("latin1"),max_age=3)
        return false

    if in_username == user.username and in_password == user.password and in_code == code:
        if check == 'on':
            response = HttpResponseRedirect('index1')
            response.set_cookie('id', user.id)
            response.set_cookie('name', user.username)
            response.set_cookie('un',in_username,max_age=10*10*10)
            response.set_cookie('false','',max_age=3)
            return response
        response = HttpResponseRedirect('index1')
        response.set_cookie('id', user.id)
        response.set_cookie('name', user.username)
        return response
    false = HttpResponseRedirect('index')
    false.set_cookie('false', '账号或密码或验证码错误'.encode("utf-8").decode("latin1"), max_age=3)
    return false

def regist(request):
    try:
        info = request.COOKIES['info'].encode('latin-1').decode('utf-8')
    except:
        info = ''
    return render(request,'login/regist.html',{'info':info})

def regist_check(request):
    username = request.POST.get('new_username')
    password = request.POST.get('new_password')

    user = models.people()
    try:
        user.username = username
        user.password = password
        user.save()
    except:
        response = HttpResponseRedirect('regist')
        response.set_cookie('info','用户名已存在'.encode("utf-8").decode("latin1"),max_age=1)
        return response
    response = HttpResponseRedirect('index')
    response.set_cookie('info','ok'.encode("utf-8").decode("latin1"),max_age=1)
    return response

def goods_check(request,num):
    buy = request.POST.get('buy') # 点击后值是 领养(value的值)  未点击是 None
    # add = request.POST.get('add')
    if buy == '领养':
        return HttpResponseRedirect('buy'+str(num))
    else:
        return HttpResponseRedirect('buy_car'+num)

def buy(request,num):
    try:
        cat = models.goods.objects.get(id = num)
    except:
        cat = models.buy_car.objects.get(id = num)
    try:
        user_id = request.COOKIES['id']
    except:
        return HttpResponseRedirect('index'+'请登录')
    try:
        default = models.user_address.objects.get(address_id=user_id, user_default_address=1)
    except:
        return HttpResponseRedirect('/address_manage')
    return render(request,'login/buy.html',{'cat':cat,'i':default})

def buy_car(request,num):
    cat = models.goods.objects.get(id=num)
    add_shop = models.buy_car()
    try:
        user_id = request.COOKIES['id']
    except:
        return HttpResponseRedirect('/index'+'请登录')
    else:
        people = models.people.objects.get(id = user_id)
        buy_car = models.buy_car.objects.filter(p_id = user_id)
        for i in buy_car:
            if cat.id == i.g_id:
                response = HttpResponseRedirect('/index1')
                response.set_cookie('info', '领养车已存在该商品'.encode('utf-8').decode('latin1'), max_age=1)
                return response
        add_shop.g_id = cat.id
        add_shop.goods_photo = cat.goods_photo
        add_shop.goods_name = cat.goods_name
        add_shop.goods_price = cat.goods_price
        add_shop.goods_type = cat.goods_type
        add_shop.p_id = people
        # add_shop.objects.create(id=cat.id,goods_photo = cat.goods_photo,goods_name = cat.goods_name,goods_price = cat.goods_price,goods_type = cat.goods_type,g_id = people)
        add_shop.save()

    all_shop = models.buy_car.objects.filter(p_id = user_id)

    #总价格
    sum = 0
    for i in all_shop:
        sum += i.goods_price

    cat = models.buy_car.objects.all()
    # 获取一共的数量
    height = math.ceil(len(cat)/5)*480

    return render(request,'login/buy_car.html',{'all_shop':all_shop,'sum':sum,'height':height})

def shopping(request,sum):
    try:
        user_id = request.COOKIES['id']
    except:
        return HttpResponseRedirect('index'+'请登录')
    try:
        default = models.user_address.objects.get(address_id=user_id, user_default_address=1)
    except:
        return HttpResponseRedirect('/address_manage')
    return render(request,'login/shopping.html',{'sum':sum,'i':default})

def show_shop(request):
    try:
        user_id = request.COOKIES['id']
    except:
        return HttpResponseRedirect('/index'+'请登录')
    all_shop = models.buy_car.objects.filter(p_id = user_id)
    # 总价格
    sum = 0
    for i in all_shop:
        sum += i.goods_price

    cat = models.buy_car.objects.all()
    # 获取一共的数量
    height = math.ceil(len(cat)/5)*480

    return render(request,'login/show_buy_car.html',{'all_shop':all_shop,'sum':sum,'height':height})

# 注销
def logout(request):
    response = HttpResponseRedirect('/index')
    response.delete_cookie('id')
    response.delete_cookie('name')
    return response


# 移出购物车
def delete_goods(request,num):
    goods = models.buy_car.objects.get(id = num)
    goods.delete()
    return HttpResponseRedirect('show_shop')

# 搜索
from django.core.paginator import Paginator
def find(request,pindex):
    '''搜索内容显示'''
    infomation = request.POST.get('info')
    if infomation is None:
        infomation  = request.COOKIES['infomation'].encode('latin1').decode('utf-8')

    find_goods = models.goods.objects.filter(goods_name__icontains = infomation)

    # 查找结果条数
    sum = len(find_goods)

    ''' 分页 '''
    # 每页显示10条记录
    pagiator = Paginator(find_goods,5)

    # 默认为第一页
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)

    # 获取第pindex页的内容
    page = pagiator.page(pindex)

    # 设置一个cookie来保存infomation的值，防止分页之后infomation值不存在了
    response = render(request, 'login/find.html', {'find_goods': page,'info':infomation,'sum':sum})
    response.set_cookie('infomation',infomation.encode('utf-8').decode('latin1'))

    return response

def address(request):
    '''地址设置页面'''

    # 获取省
    sheng = models.city.objects.filter(type = 1)

    # 获取市
    shi = models.city.objects.filter(type = 2)

    # 获取县
    xian = models.city.objects.filter(type = 3)

    return render(request,'login/address.html',{'sheng':sheng,'shi':shi,'xian':xian})

# 设置地址到数据库
def set_address(request):

    # 获取输入的值
    input_name = request.GET.get('name')
    input_phone = request.GET.get('phone')
    input_sheng = request.GET.get('sheng')
    input_shi = request.GET.get('shi')
    input_xian = request.GET.get('xian')
    input_address = request.GET.get('address')
    try:
        id = request.COOKIES['id']
        people = models.people.objects.get(id = id)
    except:
        return HttpResponseRedirect('/index'+'请登录')
    else:
        # 获取里面的地址数量  如果数量为零  则将接下来添加的地址设置为默认地址
        all_address_num = models.user_address.objects.filter(address_id = id)
        # 将用户输入的地址信息插入数据库
        ud = models.user_address()
        ud.user_name = input_name
        ud.user_phone = input_phone
        ud.user_sheng = input_sheng
        ud.user_shi = input_shi
        ud.user_xian = input_xian
        ud.user_deAddress = input_address
        ud.address_id = people
        if len(all_address_num) == 0:
            ud.user_default_address = 1
        ud.save()
    return HttpResponseRedirect('/index1')

# 管理收货地址
def address_manage(request):
    # 获取用户id 如果没有登录则会提取失败并且跳转到登陆页面
    try:
        id = request.COOKIES['id']
    except:
        return HttpResponseRedirect('/index'+'请登录')
    # 获取用户对应的收获地址
    address = models.user_address.objects.filter(address_id = id)

    return render(request,'login/address_manage.html',{'address':address})

# 设置默认收货地址
def set_default(request,num):
    # 获取用户id 如果没有登录则会提取失败并且跳转到登陆页面
    try:
        id = request.COOKIES['id']
    except:
        return HttpResponseRedirect('/index'+'请登录')

    # 判断用户点击的是删除还是设为默认
    if request.GET.get('set_to_default'):
        # 获取所有地址  并将其默认收货地址id设置为0
        all_address = models.user_address.objects.filter(address_id=id)
        for i in all_address:
            i.user_default_address = 0
            i.save()
        # 再将需要设置为默认地址的id设置为1
        set_default_address = models.user_address.objects.get(id=num)
        set_default_address.user_default_address = 1
        set_default_address.save()
    else:
        delete_address = models.user_address.objects.get(id = num)
        delete_address.delete()

    return HttpResponseRedirect('/address_manage')

# 商品详细信息展示页面
def detailed_info(request,num):
    # 获取展示商品的信息
    picture = models.goods.objects.get(id = num)

    return render(request,'login/detailed_info.html', {'show': picture})

import time,math
# 个人主页
def personal_homepage(request):
    '''个人主页'''
    # 获取用户id 如果没有登录则会提取失败并且跳转到登陆页面
    try:
        user_id = request.COOKIES['id']
    except:
        return HttpResponseRedirect('/index'+'请登录')

    # 根据id获取用户
    user = models.people.objects.get(id = user_id)

    # 获取创建时的时间戳
    create_time_stamp = user.time_stamp

    # 获取当前时间戳
    ts = time.time()

    # 间隔时间
    interval_time = ts - create_time_stamp

    # 转换成天数
    day = 1 if interval_time / (24*3600) < 1 else math.ceil(interval_time / (24*3600))

    return render(request,'login/personal_homepage.html',{'day':day,'user':user})


# 疫情接口
import requests,jsonpath,pandas as pd
def covid19(request):
    '''疫情'''
    url = "https://2019ncov.chinacdc.cn/JKZX/yq_20221205.json"

    headers = {
        'Accept-Ranges': 'bytes',
        'Content-Length': '420283',
        'Content-Type': 'application/json',
        'Date': 'Tue,06Dec202214:34:40GMT',
        'ETag': '"638ea110-669bb"',
        'Last-Modified': 'Tue,06Dec202201:55:28GMT',
        'Server': 'nginx/1.20.2',
    }

    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    result = response.text
    city_name = jsonpath.jsonpath(obj=result, expr='$.features..properties.name')
    新增疑似 = jsonpath.jsonpath(obj=result, expr='$.features..properties.新增疑似')
    累计疑似 = jsonpath.jsonpath(obj=result, expr='$.features..properties.累计疑似')
    新增确诊 = jsonpath.jsonpath(obj=result, expr='$.features..properties.新增确诊')
    累计确诊 = jsonpath.jsonpath(obj=result, expr='$.features..properties.累计确诊')
    累计死亡 = jsonpath.jsonpath(obj=result, expr='$.features..properties.累计死亡')
    新增死亡 = jsonpath.jsonpath(obj=result, expr='$.features..properties.新增死亡')
    dataframe = pd.DataFrame([city_name, 新增疑似, 累计疑似, 新增确诊, 累计确诊, 累计死亡, 新增死亡]).T
    list = []
    for i in range(dataframe.shape[0]):
        test = []
        for j in dataframe:
            test.append(dataframe.loc[i, j])
        list.append(test)

    return render(request,'login/covid19.html',context={'info':list})
