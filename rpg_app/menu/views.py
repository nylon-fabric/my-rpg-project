from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Account, Character, Items, Setting, ItemData, Monster

from .forms import AccountForm, CharacterForm, NameForm
from random import randint
import re



def index(request):
    data = Account.objects.all()
    params = {
            'title': 'データ画面',
            'msg' : '',
            'data': data
            }
        
    if Account.objects.all().count() == 0:
        params['msg'] = 'アカウントデータがありません'
    
    return render(request, 'menu/index.html', params)

def select_choice(request, num):
    """セレクト画面"""
    data = Account.objects.get(id=num)
    chara = data.character_set.all()
    
    params = {
            'title': 'ベース',
            'msg':'',
            'data':data,
            }
    if (request.method == 'POST'):
        
        if chara.count() == 0:
            params['msg'] = 'キャラクターがいません'
        else:
            go = '/menu/donjon/' + str(num)
            return redirect(to=go)
    return render(request, 'menu/select_choice.html', params)



def chara_datas(request, num):
    """キャラクター一覧"""
    
    data = Account.objects.get(id=num)
    chara = data.character_set.all()
    chara_num = chara.count()
    params = {
            'title': 'キャラクターシート',
            'msg': '現在:' + str(chara_num) +'人',
            'data': data,
            'chara': chara,
            }
    if chara_num == 0:
        params['msg'] = 'キャラクターがいません'
    return render(request, 'menu/chara_datas.html', params)


def chara_status(request, num1, num2):
    
    data = Account.objects.get(id=num1)
    chara = Character.objects.get(id=num2)
    params = {
            'title': 'ステータス',
            'msg':'',
            'data':data,
            'chara': chara,
            }
    return render(request, 'menu/chara_status.html', params)


def chara_create(request, num):
    """キャラクター作成"""
    data = Account.objects.get(id=num)
    chara = data.character_set.all()
    params = {
            'title': 'キャラクター作成',
            'msg':'名前を決めてください',
            'data': data,
            'chara': chara,
            'form': CharacterForm(),
            }
    if (request.method == 'POST'):
        if chara.count() == 3:
            params['msg'] = '登録できるのは3人までです'
        else:
            name = request.POST['name']
            job = request.POST['job']
            
            go = '/menu/chara_create_next/' + str(num) + '/' + \
            str(name) + '/' + str(job)
            return redirect(to=go)
            
    return render(request, 'menu/chara_create.html', params)


def dice3D6():
    
    lists = []
    for num in range(4):
        d = 0
        for n in range(3):
            d += randint(3, 6)
        lists.append(d)
            
    return lists


def chara_create_next(request, num, name, job):
    """キャラクターステータスの作成"""
    data = Account.objects.get(id=num)
    jobs = job.split('.')
    
    if (request.method == 'POST'):
        sets = data.setting_set.first()

        if 'create' in request.POST:
            
            data.character_set.create(name=name, job=job[:2], lv=1, \
                                  CON=sets.CON, \
                                  STR=sets.STR, \
                                  DEX=sets.DEX, \
                                  POW=sets.INT, \
                                  INT=sets.INT, \
                                  HP=sets.CON)
            
            go = '/menu/chara_datas/' + str(num)
            return redirect(to=go)
    
    s = dice3D6()
    
    if jobs == '戦士':
        s[1] += 3
    elif jobs == '魔術師':
        s[2] += 3
    elif jobs == '盗賊':
        s[3] += 3
    elif jobs == '商人':
        s[0] += 3
    
    params = {
            'title': 'ステータス作成',
            'msg': name + ' のステータスを作成',
            'data': data,
            'chara': {'name': name, 'job': jobs[0],},
            'form': CharacterForm(),
            'status': {
                    'com': s[0],
                    'str': s[1],
                    'int': s[2],
                    'dex': s[3],
                    }
            }
            
    if data.setting_set.all().count() != 0:
        data.setting_set.all().delete()
    data.setting_set.create(CON=s[0], STR=s[1], DEX=s[3], INT=s[2])
        
    return render(request, 'menu/chara_create_next.html', params)


def chara_name_change(request, num1, num2):
    """名前の変更"""
    data = Account.objects.get(id=num1)
    chara = Character.objects.get(id=num2)
    params = {
            'title': 'キャラクター名変更',
            'msg':'名前を決めてください',
            'data': data,
            'chara': chara,
            'form': NameForm(),
            }
    if(request.method == 'POST'):
        name = request.POST['name']
        chara.name = name
        chara.save()
        
        go = '/menu/chara_datas/' + str(num1)
        return redirect(to=go)
        
    return render(request, 'menu/chara_name_change.html', params)


def chara_delete(request, num1, num2):
    """キャラの削除"""
    data = Account.objects.get(id=num1)
    chara = Character.objects.get(id=num2)
    params = {
            'title': 'キャラクター削除',
            'msg':'本当に 「' + chara.name + '」 を削除しますか？',
            'data': data,
            'chara': chara,
            }
    if(request.method == 'POST'):
        Character.objects.filter(id=num2).delete()
        go = '/menu/chara_datas/' + str(num1)
        return redirect(to=go)
    
    
    return render(request, 'menu/chara_delete.html', params)


def item_datas(request, num):
    """アイテム倉庫"""
    
    data = Account.objects.get(id=num)
    num = data.items_set.all().count()
    m = '現在アイテム数：' + str(num) + '個' + '　最大数量：15個'
    params = {
            'title': 'アイテム',
            'msg': m,
            'data': data,
            }
    
    return render(request, 'menu/item_datas.html', params)


def item_discard(request, num1, num2):
    """アイテムを捨てる"""
    data = Account.objects.get(id=num2)
    item = Items.objects.get(id=num1)
    params = {
            'title': 'アイテム',
            'msg':'本当に、このアイテムを捨てますか？',
            'data':data,
            'item': item,
            }
    if(request.method == 'POST'):
        Items.objects.filter(id=num1).delete()
        go = '/menu/item_datas/' + str(num2)

        return redirect(to=go)
    
    return render(request, 'menu/item_discard.html', params)


def i_use_delete(item, chara, num):
    """アイテムを使用したときの効果処理と削除"""
    item_num = item.item_num
    
    if str(item.item_type) == '回復':
        recovery(chara, item_num)#回復呼び出し
        Items.objects.filter(id=num).delete()
    
    elif str(item.item_type) == 'Lvアップ':
        chara.lv = chara.lv + 1
        chara.CON = chara.CON + randint(0, 2)
        chara.STR = chara.STR + randint(0, 2)
        chara.DEX = chara.DEX + randint(0, 2)
        chara.POW = chara.POW + randint(0, 2)
        chara.INT = chara.INT + randint(0, 2)
        chara.save()
        Items.objects.filter(id=num).delete()


def item_use(request, num1, num2):
    """アイテムの使用、選択"""
    item = Items.objects.get(id=num1)
    data = Account.objects.get(id=num2)
    params = {
            'title': 'アイテム',
            'msg': '誰に使用しますか？',
            'data': data,
            'item': item,
            }
    if(request.method == 'POST'):
        
        ids = str(request.POST)
        id_num = re.split('[\':"]', ids)
        chara_id = id_num[-5]
        chara = Character.objects.get(id=chara_id)
       
        i_use_delete(item, chara, num1)#アイテムの処理
        
        go='/menu/item_datas/' + str(num2)
        return redirect(to=go)
        
    return render(request, 'menu/item_use.html', params)


def account_create(request):
    """アカウント作成"""
    if(request.method == 'POST'):
        name = request.POST['name']
        money = request.POST['money']
        accounts = Account(name=name, money=money)
        accounts.save()
        
        return redirect(to='/menu')
    
    params = {
            'title': 'アカウント作成画面',
            'msg': 'プレイヤーの名前を入力してください',
            'form': AccountForm(),
            }
        
    return render(request, 'menu/account_create.html', params)


def account_remove(request, num):
    """アカウント削除"""
    data = Account.objects.get(id=num)
    
    params = {
            'title': 'アカウント削除',
            'msg': 'こちらのアカウントを削除しますか？',
            'data': data,
            }
    if(request.method == 'POST'):
        data.delete()
        return redirect(to='/menu')
    
    return render(request, 'menu/account_remove.html', params)


def account_name_change(request, num):
    """アカウントの名前変更"""
    
    data = Account.objects.get(id=num)
    params = {
            'title': '名変更',
            'msg':'名前を決めてください',
            'data': data,
            'form': NameForm(),
            }
    if(request.method == 'POST'):
        name = request.POST['name']
        data.name = name
        data.save()
        
        return redirect(to='/menu')
    
    return render(request, 'menu/account_name_change.html', params)


def item_shop(request, num):
    """アイテムショップメイン画面"""
    data = Account.objects.get(id=num)
    
    params = {
            'title': 'アイテムショップ',
            'msg': 'ヘイッいらっしゃい！',
            'data' : data,
            }
    if(request.method == 'POST'):
        obj = Items.objects.all().count()
        if obj == 0:
            params['msg'] = 'お客さん、何も持ってないよ・・・'
        else:
            go = '/menu/shop_sell/'+ str(num)
            return redirect(to=go)
    return render(request, 'menu/item_shop.html', params)


def pay(wallet, price, data):
    """清算"""
    result = wallet - price
    data.money = result
    data.save()

    
def buy(price, data, item, lvs, typ, num, comm, wallet):
    """アイテム購入による変更"""
    
    pay(wallet, price, data)
    
    name = item
    lv = lvs
    types = typ
    nums = num
    com = comm
    data.items_set.create(item_name = name, item_lv = lv, \
                          item_type = types, item_num = nums, \
                          item_comment = com)


def shop_buy(request, num):
    """アイテムショップ購入画面"""
    data = Account.objects.get(id=num)
    
    params = {
            'title': 'アイテム購入',
            'msg': '何にいたしましょう？',
            'data': data,
            }
    if(request.method == 'POST'):
        wallet = data.money
        if wallet == 0:
            params['msg'] = 'お客さん、お金がないよ'
            
        elif Items.objects.all().count() == 15:
            params['msg'] = '荷物がいっぱいだよ'
            
        else:
            if 'apple' in request.POST:
                if wallet >= 100 :
                    price = 100
                    name = 'リンゴ'
                    lv = 1
                    typ = '回復'
                    num = 5
                    com = 'おいしいリンゴ'
                    buy(price, data, name, lv, typ, num, com, wallet)
                    params['msg'] = 'まいど！！'
                else:
                    params['msg'] = 'お客さん、お金が足りないよ'
                    
            elif 'bread' in request.POST:
                if wallet >= 180:
                    price = 180
                    name = 'パン'
                    lv = 1
                    typ = '回復'
                    num = 10
                    com = '日持ちする固めのパン'
                    buy(price, data, name, lv, typ, num, com, wallet)
                    params['msg'] = 'まいど！！'
                else:
                    params['msg'] = 'お客さん、お金が足りないよ'
                    
            elif 'cheese' in request.POST:
                if wallet >= 350:
                    price = 350
                    name = 'チーズ'
                    lv = 1
                    typ = '回復'
                    num = 20
                    com = '手作りチーズ、ちょっと臭い'
                    buy(price, data, name, lv, typ, num, com, wallet)
                    params['msg'] = 'まいど！！'
                else:
                    params['msg'] = 'お客さん、お金が足りないよ'
            
                
    return render(request, 'menu/shop_buy.html', params)


def shop_sell(request, num):
    """アイテムを売る"""
    item_db = ItemData.objects.all()
    data = Account.objects.get(id=num)
    num = data.items_set.all().count()
    
    m = '何を売ってくれますか？' 
    params = {
            'title': 'アイテム',
            'msg': m,
            'data': data,
            'item_db': item_db,
            'var': 2
            }
    if(request.method == 'POST'):

        for x in item_db:
            
            ids = str(request.POST)
            id_num = re.split('[\':"]', ids)
            
            if x.name == id_num[-6]:
                m = int(data.money)
                p = int(x.price)
                wallet = m + p
                
                data.money = wallet
                data.save()
        
        ac_id = id_num[-5]
        Items.objects.filter(id=ac_id).delete()

    return render(request, 'menu/shop_sell.html', params)


def recovery(chara, item):
    """回復"""
        
    set_hp = chara.HP + item
            
    if chara.CON <= set_hp:
        chara.HP = chara.CON
        chara.save()
    else:
        chara.HP = set_hp
        chara.save() 


def hotel(request, num):
    """宿"""
    data = Account.objects.get(id=num)
    chara = data.character_set.all()
    chara_num = data.character_set.count()
    c_price = 300
    h_price = 1000
    c_p = c_price * chara_num
    h_p = h_price * chara_num
    
    params = {
            'title': '宿屋',
            'msg': 'いらっしゃいませ　'+ str(chara_num) + '名様でいらっしゃいますね',
            'data': data,
            'num': {'c_price':c_p,
                    'h_price':h_p},
            }
    if(request.method == 'POST'):
        if 'cheap' in request.POST:
            if data.money <= c_p:
                params['msg'] = 'お金が足りないようですが・・・'
            else:
                for i in chara:
                    recovery(i, 15)
                params['msg'] = 'ごゆっくり'
                pay(data.money, c_price, data)
            
        elif 'high' in request.POST:
            if data.money <= h_p:
                params['msg'] = 'お金が足りないようですが・・・'
            else:
                for i in chara:
                    recovery(i, 100)
                params['msg'] = 'あー、よいよい！！'
                pay(data.money, h_price, data)

    return render(request, 'menu/hotel.html', params)


def donjon(request, num):
    """ダンジョン"""
    data = Account.objects.get(id=num)
    
    params = {
            'title': 'ダンジョン',
            'msg': '',
            'data': data,
            }
    if(request.method == 'POST'):
        if 'item' in request.POST:
            go = '/menu/donjon_item/' + str(num)
            return redirect(to=go)
        
        else:
            dice = randint(0,5)
#            dice = 1#テスト用
            
            if dice == 0:
                m_num = Monster.objects.all().count()
                dice = randint(1, m_num)#DBのモンスターランダム決定
                
                mons = Monster.objects.get(id=dice)
                mons.HP = mons.CON#念のためモンスターの回復
                mons.save()
                go = '/menu/battle/' + str(num) + '/' + str(mons.id)
                return redirect(to=go)

    return render(request, 'menu/donjon.html', params)


def donjon_item(request, num):
    """ダンジョンでアイテム画面"""
    data = Account.objects.get(id=num)
    num = data.items_set.all().count()
    m = '現在アイテム数：' + str(num) + '個' + '　最大数量：15個'
    
    if (request.method == 'POST'):#捨てる処理
        ids = str(request.POST)
        id_num = re.split('[\':"]', ids)
        i_id = id_num[-5]
        Items.objects.filter(id=i_id).delete()
    
    params = {
            'title': 'アイテム',
            'msg': m,
            'data': data,
            }
    return render(request, 'menu/donjon_item.html', params)


def donjon_item_use(request, num1, num2):
    """ダンジョン内アイテム使用画面"""
    item = Items.objects.get(id=num1)
    data = Account.objects.get(id=num2)
    
    if(request.method == 'POST'):
        
        ids = str(request.POST)
        id_num = re.split('[\':"]', ids)
        chara_id = id_num[-5]
        chara = Character.objects.get(id=chara_id)
       
        i_use_delete(item, chara, num1)#アイテムの処理
        
        go='/menu/donjon_item/' + str(num2)
        return redirect(to=go)
    
    params = {
            'title': 'アイテム',
            'msg': '誰に使用しますか？',
            'data': data,
            'item': item,
            }
        
    return render(request, 'menu/donjon_item_use.html', params)


def donjon_item_next(request, num):
    """画面リロード対策用ダンジョン画面"""
    data = Account.objects.get(id=num)
    
    params = {
            'title': 'ダンジョン',
            'msg': '',
            'data': data,
            }
    if(request.method == 'POST'):
        if 'item' in request.POST:
            go = '/menu/donjon_item/' + str(num)
            return redirect(to=go)
        
        else:
            dice = randint(0,5)
            
            if dice == 0:
                m_num = Monster.objects.all().count()
                mons = Monster.objects.get(id=m_num)
                mons.HP = mons.CON#モンスターの回復
                mons.save()
                go = '/menu/battle/' + str(num) + '/' + str(mons.id)
                return redirect(to=go)
            
        go = '/menu/donjon/' + str(num)
        return redirect(to=go)

    return render(request, 'menu/donjon_item_next.html', params)


def chara_act_attack(i, mons):
    """戦うのダメージ計算"""
    rate = 50 + (i.STR - mons.CON) * 5
    if rate <= 0:
        d_max = int(i.STR) - int(rate // -10)
        mini = d_max * 2 // 3
        d_dice = randint(mini, d_max)
        damage = d_dice
        
    else:
        mini = int(i.STR) * 2 // 3#攻撃の最低値
        d_dice = randint(mini , int(i.STR))
        damage = d_dice
        
    if damage <= 1:
        damage = 1
        
    return damage


def chara_act_block(i, mons):
    """守るのダメージ処理"""

    damage = enemy_attack(mons, i)
    
    rate = 50 + (mons.STR - i.CON) * 5
    block = int(i.STR) - int(rate // -10)
    damage -= block
    if damage <= 0:
        damage = 0
        
    d = f'{str(i.name)}に{str(damage)}のダメージ'
    lost = i.HP - damage
    if 1 <= lost:
        i.HP = lost
        i.save()
    else:
        i.delete()
        d = d + f'{str(i.name)}は倒れた'
        
    return d


def enemy_attack(mons, i):
    """敵の攻撃"""
    rate = 50 + (mons.STR - i.CON) * 5
    if rate <= 0:
        d_max = int(mons.STR) - int(rate // -10)
        mini = d_max * 2 // 3
        d_dice = randint(mini, d_max)
        damage = d_dice
    else:
        mini = int(mons.STR) * 2 // 3
        d_dice = randint(mini, int(mons.STR))
        damage = d_dice
        
    if damage <= 1:
        damage = 1
        
    return damage


def chara_second_attack(mons, c, give_d, data):
    """後攻になった味方の処理"""
    lost_m = mons.HP - give_d
    give_msg = f'{give_d}のダメージを与えた'
                    
    if 1 <= lost_m:#まだ敵が生きているときの処理
        mons.HP = lost_m
        c.save()
    else:#敵が倒れた場合の処理
        mons.HP = 0
        mons.save()
        get_msg = item_luck(mons, data)
        give_msg = give_msg + ' ' + f'{mons.name}を倒した' + get_msg
        
    return give_msg


def item_luck(mons, data):
    """モンスターからアイテムを入手できるか"""
    m = ' '
    
    bring_up = str(mons.item)
    if bring_up != '':#アイテム入手の処理

        take = list(bring_up.split(','))
        
        dice = randint(1, len(take) * 2)
        if dice <= len(take):

            i_name = take[dice - 1]
            get_i = ItemData.objects.get(name=i_name)
            m = '\n' + i_name + 'を手に入れた！'

            name = get_i.name
            lv = get_i.lv
            types = get_i.type
            nums = get_i.num
            com = get_i.comment
        
            if data.items_set.all().count() >= 15:
                m = '\n' + i_name + 'を手に入れたが 荷物がいっぱい'
        
            elif data.items_set.all().count() <= 15:
                data.items_set.create(item_name = name, item_lv = lv, \
                                      item_type = types, item_num = nums, \
                                      item_comment = com)
            
    return m


def battle(request, num1, num2):
    """バトル画面"""
    data = Account.objects.get(id=num1)
    chara = data.character_set.all()
    mons = Monster.objects.get(id=num2)
    c_num = chara.count()
    flag = False
    
    msg = 'モンスターが現れた\n　'
    
    if(request.method == 'POST'):
        
        if c_num == 0:#全滅時の処理
            go = '/menu/select_choice/' + str(num1)
            return redirect(to=go)
        
        elif mons.HP == 0:#倒した処理
            
            mons.HP = mons.CON#モンスターHPをもとに戻しておく
            mons.save()
            go = '/menu/donjon/' + str(num1)
            return redirect(to=go)
        
        elif '逃げる' in request.POST:
            dexs = 0
            for d in chara:
                dexs += d.DEX
                
            mean_dex = dexs // c_num#平均
            
            if mons.DEX <= mean_dex:
                mons.HP = mons.CON
                go = '/menu/donjon/' + str(num1)
                return redirect(to=go)
            else:
                msg = '逃げられない！'
        
        else:#戦闘の処理はここから
            id_c = [c.id for c in chara]
            dice = randint(0, len(id_c) - 1)
            
            enemy_target = id_c[dice]#攻撃対象のID決定
            
            lost_msg =''
            give_msg = ''
            
            dexs = 0
            give_d = 0
            for i in chara:
                act = request.POST[str(i.id)]#プレイヤーの選択別処理
                if act == '守る'and i.id == enemy_target:
                    lost_msg = chara_act_block(i, mons)
                    flag = True

                elif act == '戦う':#戦うを選択
                    damage = chara_act_attack(i, mons)
                    give_d += damage
                    
                dexs += int(i.DEX)
            
            mean_dex = dexs // c_num#プレイヤーの速さの平均
            c = Character.objects.get(id=enemy_target)
            
            if mons.DEX <= mean_dex:#プレイヤーが先行の処理
                lost_m = mons.HP - give_d
                give_msg = f'合計 {give_d}のダメージを与えた'
                
                if 1 <= lost_m:#まだ敵が生きているときの処理
                    mons.HP = lost_m
                    mons.save()
                    
                    if act != '守る':#守るにした味方に当たらなかった場合
                        
                        damage = enemy_attack(mons, c)
                        lost_hp = c.HP - damage
                        lost_msg = f'{c.name}に{damage}のダメージ!'
                        
                        if 1 <= lost_hp:#まだ味方が生きている処理
                            c.HP = lost_hp
                            c.save()
                            
                        elif lost_hp <= 0:#見方が倒れたときの処理
                            c.delete()
                            lost_msg = lost_msg + ' ' + f'{c.name}は倒れた'
                    
                else:#敵が倒れた場合の処理
                    mons.HP = 0
                    mons.save()
                    get_msg = item_luck(mons, data)
                    give_msg = give_msg + ' ' + f'{mons.name}を倒した' + str(get_msg)
                    
                if flag == True:
                    msg = lost_msg + '\n' + give_msg
                else:
                    msg = give_msg + '\n' + lost_msg
                
            else:#敵が先行の処理
                if act != '守る':#守るにした味方に当たらなかった場合
                    damage = enemy_attack(mons, c)
                    lost_hp = c.HP - damage
                    lost_msg = f'{c.name}に{damage}のダメージ'
                    
                    if 1 <= lost_hp:#まだ味方が生きている処理
                        c.HP = lost_hp
                        c.save()
                        
                        give_msg = chara_second_attack(mons, c, give_d, data)#後攻になった味方の処理
                        
                    else:#見方が倒れたときの処理
                        c.delete()
                        lost_msg = lost_msg + ' ' + f'{c.name}は倒れた'
                else:
                    give_msg = chara_second_attack(mons, c, give_d, data)#後攻になった味方の処理
                    
                msg = lost_msg + '\n' + give_msg
                
                
    params = {
              'title': '戦闘',
              'msg': msg,
              'data': data,
              'chara': data.character_set.all(),
              'mons': mons,
             }
        
        
    return render(request, 'menu/battle.html', params)