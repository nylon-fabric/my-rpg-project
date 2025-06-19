from django.urls import path
from . import views


urlpatterns = [
        path('', views.index, name='index'),
        path('chara_datas/<int:num>', views.chara_datas, name='chara_datas'),
        path('chara_status/<int:num1>/<int:num2>', views.chara_status, \
             name='chara_status'),
        path('chara_create/<int:num>', views.chara_create, \
             name='chara_create'),
        path('chara_create_next/<int:num>/<str:name>/<str:job>',\
             views.chara_create_next, name='chara_create_next'),
        path('chara_name_change/<int:num1>/<int:num2>', \
             views.chara_name_change, name='chara_name_change'),
        path('chara_delete/<int:num1>/<int:num2>', views.chara_delete, \
             name='chara_delete'),
        path('select_choice/<int:num>', views.select_choice, \
             name='select_choice'),
        path('item_datas/<int:num>', views.item_datas, name='item_datas'),
        path('item_discard/<int:num1>/<int:num2>', views.item_discard, \
             name='item_discard'),
        path('item_use/<int:num1>/<int:num2>', views.item_use, name='item_use'),
        path('account_create/', views.account_create, name='account_create'),
        path('account_remove/<int:num>', views.account_remove, \
             name='account_remove'),
        path('account_name_change/<int:num>', views.account_name_change, \
             name="account_name_change"),
        path('item_shop/<int:num>', views.item_shop, name='item_shop'),
        path('shop_buy/<int:num>', views.shop_buy, name='shop_buy'),
        path('shop_sell/<int:num>', views.shop_sell, name='shop_sell'),
        path('hotel/<int:num>', views.hotel, name='hotel'),
        path('donjon/<int:num>', views.donjon, name='donjon'),
        path('donjon_item/<int:num>', views.donjon_item, name='donjon_item'),
        path('donjon_item_use/<int:num1>/<int:num2>', \
             views.donjon_item_use, name='donjon_item_use'),
        path('donjon_item_next/<int:num>', views.donjon_item_next, \
             name='donjon_item_next'),
        path('battle/<int:num1>/<int:num2>', views.battle, name='battle'),
        ]
