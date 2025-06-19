from django.db import models
from django.core.validators import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class Monster(models.Model):
    """モンスターの種類"""
    name = models.CharField(null=True, max_length=10)
    CON = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#体力
    STR = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#筋力
    DEX = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#俊敏さ
    POW = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#魔力
    INT = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#賢さ
    HP = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#ヒットポイント
    item = models.CharField(blank=True, null=True, max_length=10)#持っているアイテム
    image = models.ImageField(verbose_name='モンスター画像', \
                              blank=True, null=True)
    
    def __str__(self):
        return 'ID:' + str(self.id) + ' name:' + str(self.name) + \
               ' <' + ' CON:' + str(self.CON) + ' STR:' + str(self.STR) + \
               ' DEX:' + str(self.DEX) + ' POW:' + str(self.POW) + \
               ' INT:' + str(self.INT) + ' HP:' + str(self.HP) + '> ' + \
               ' アイテム:' + str(self.item) + ' 画像：' + str(self.image)


class ItemData(models.Model):
    """アイテムの種類"""
    name = models.CharField(null=True, max_length=10)
    lv = models.IntegerField(default=0, validators=[MinValueValidator(0), \
                                                         MaxValueValidator(50)])
    type = models.CharField(null=True, max_length=10)
    num = models.IntegerField(default=0, validators=[MinValueValidator(0),\
                                                          MaxValueValidator(50)])
    comment = models.CharField(null=True, max_length=20)
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return 'ID:' + str(self.id) + '　' + str(self.name) + \
               ' Lv' + str(self.lv) + ' typy:' + str(self.type) + \
                str(self.num) + ' ' + str(self.price) + '円　' +str(self.comment)


class Account(models.Model):
    """"プレイヤーアカウントの内容
    名前　テキスト値
    お金　整数"""
    
    name = models.CharField(null=True, max_length=20)
    money = models.IntegerField(default=0)
    
    def __str__(self):
        return '<account:ID =' + str(self.id) + \
               ' name = ' + str(self.name) + \
               ' money = ' + str(self.money) + '円>'

               
class Character(models.Model):
    """"アカウントの従テーブル キャラクター"""
       
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    name = models.CharField(null=True, max_length=10)
    job = models.CharField(null=True, max_length=10)
    equip = models.CharField(null=True, max_length=10)#装備品
    #技能値
    lv = models.IntegerField(\
                             default=1, \
                             validators=[MinValueValidator(0), \
                                         MaxValueValidator(100)])
    CON = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#体力
    STR = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#筋力
    DEX = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#俊敏さ器用さ
    POW = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#魔力
    INT = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#賢さ
    
    HP = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#ヒットポイント
    
    def __str__(self):
        
        return '<ID:' + str(self.id) + ' name:' + str(self.name) + \
               ' LV:' + str(self.lv) + ' Job:' + str(self.job) + \
               ' HP:' + str(self.HP) + '　' + ' con:' +  str(self.CON) + \
               ' str:' + str(self.STR) + ' dex:'+ str(self.DEX) + \
               ' pow:' + str(self.POW) + ' int:' + str(self.INT) + '>'
               
               
class Setting(models.Model):
    """プレイヤー別、仮設定のモデル置き場"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
        
    CON = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#体力
    STR = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#筋力
    DEX = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#俊敏さ器用さ
    INT = models.IntegerField(\
                              default=0, \
                              validators=[MinValueValidator(0), \
                                          MaxValueValidator(99)])#賢さ
    
    def __str__(self):
        return 'CON:' + str(self.CON) + \
               ' STR:' + str(self.STR) + \
               ' DEX:' + str(self.DEX) + \
               ' INT:' + str(self.INT)
               
               
class Items(models.Model):
    """アカウントの従テーブル アイテム"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    item_name = models.CharField(null=True, max_length=10)
    item_lv = models.IntegerField(default=0, validators=[MinValueValidator(0), \
                                                         MaxValueValidator(50)])
    item_type = models.CharField(null=True, max_length=10)
    item_num = models.IntegerField(default=0, validators=[MinValueValidator(0),\
                                                          MaxValueValidator(50)])
    item_comment = models.CharField(null=True, max_length=20)
    
    def __str__(self):
        return 'ID:' + str(self.id) + '　' + str(self.item_name) + \
               ' Lv' + str(self.item_lv) + ' typy:' + str(self.item_type) + \
               str(self.item_num) + str(self.item_comment)

#
##class Skil(models.Model):
##    """"アカウント→キャラクタ→の従テーブル スキル"""
##    character = models.ForeignKey(Character, on_delete=models.CASCADE)
##    
##    skil_name = models.CharField(null=True, max_length=10)
##    skil_lv = models.IntegerField(default=0,  validators=[MinValueValidator(0), \
##                                                          MaxValueValidator(50)])
##    skil_type = models.CharField(null=True, max_length=10)
##    skil_num = models.IntegerField(default=0, validators=[MinValueValidator(0),\
##                                                          MaxValueValidator(50)])
##    skil_comment = models.CharField(null=True, max_length=20)
##    
##    def __str__(self):
##        return str(self.skil_name) + 'Lv' + str(self.skil_lv) + \
##               str(self.skil_comment)
#               
