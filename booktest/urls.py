
from django.urls import  re_path, include
from booktest import views
urlpatterns = [
    re_path(r'^index1$', views.index1),
    re_path(r'^index(.*)$',views.index),
    re_path(r'login_check$',views.login_check),
    re_path(r'^regist$',views.regist),
    re_path(r'^regist_check$',views.regist_check),
    re_path(r'^goods_check(\d+)$',views.goods_check),
    re_path(r'^buy(\d+)$',views.buy),
    re_path(r'^buy_car(\d+)$',views.buy_car),
    re_path(r'^shopping(\d+)$',views.shopping),
    re_path(r'^show_shop$',views.show_shop),
    re_path(r'^logout$',views.logout),
    re_path(r'^delete_goods(\d+)$', views.delete_goods),
    re_path(r'^find(\d*)$',views.find),
    re_path(r'^address$', views.address),
    re_path(r'^set_address$', views.set_address),
    re_path(r'^address_manage$', views.address_manage),
    re_path(r'^set_default(\d+)$', views.set_default),
    re_path(r'^detailed_info(\d+)$', views.detailed_info),
    re_path(r'^personal_homepage$',views.personal_homepage),
    re_path(r'^covid19$', views.covid19),
]
