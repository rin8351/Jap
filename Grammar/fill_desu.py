import random 

def ran(x):
    return random.choice(list(x.keys())) 

def lists_words_desu():

    sp = []
    for i in var_desu:
        for j in var_desu[i]:
            sp.append(desu_vars(i,j))
    for i in var_pril:
        for j in var_pril[i]:
            sp.append(pril_vars(i,j))
    for i in var_glag:
        for j in var_glag[i]:
            sp.append(glag_vars(i,j))
    return sp


a = {
# Местоимения
'uno' : {'この':'этот','その':'тот','あの':'вон тот'},
# существительные и люди
'names' : {'田中':'Танака','三木':'Мики','山田':'Ямада','明子':'Акико',},
'names_hir':{'田中':'たなか','三木':'みき','山田':'やまだ','明子':'あきこ',},
'family' : {'お父さん':'отец','お母さん':'мама','おにいさん':'брат','おねえさん':'сестра','いもうと':'младшая сестра','おとうと':'младший брат','友だち':'друг'},
'family_hur':{'お父さん':'おとうさん','お母さん':'おかあさん','おにいさん':'おにいさん','おねえさん':'おねえさん','いもうと':'いもうと','おとうと':'おとうと','友だち':'ともだち'},
'end_family' : {'お父さん':'отца','お母さん':'матери','おねえさん':'брата','おねえさん':'сестры','いもうと':'младшей сестры','おとうと':'младшего брата','友だち':'друга'},
'end_names':{'田中':'Танаки','三木':'Мики','山田':'Ямады','明子':'Акико',},
'profession':{'先生':'преподаватель','大学生':'студент ',},
'profession_hir':{'先生':'せんせい','大学生':'だいがくせい',},
'profession_many':{'先生':'учителя','大学生':'студенты ',},
'end_profession':{'先生':'учителем','大学生':'студентом ',},
'end_profession_many':{'先生':'учителями','大学生':'студентами',},
'small object':{'ざっし':'журнал','はこ':'короб','辞書':'словарь','本':'книга'},
'small object_hir':{'ざっし':'ざっし','はこ':'はこ','本':'ほん','辞書':'じしょ'},
'adj_for_small_object':{
    'ざっし': {'新し':'новый', '古':'старый','おもしろ':'интересный', '高':'дорогой','安':'дешевый'},
    'はこ': {'大き':'большой', '小さ':'маленький',  '赤':'красный','青':'синий','黄色':'желтый','白':'белый','黒':'черный','茶色':'коричневый'},
    'かばん': {'新し':'новый', '古':'старый','赤':'красный','青':'синий','黄色':'желтый','白':'белый','黒':'черный','茶色':'коричневый'},
    '辞書':{'高':'дорогой','安':'дешевый'},
    '本':{ 'おもしろ':'интересная', '高':'дорогая','安':'дешевая'}
},
'adj_for_small_object_hir':{
    'ざっし': {'新し':'あたらし', '古':'ふる','おもしろ':'おもしろ', '高':'たか','安':'やす'},
    'はこ': {'大き':'おおき', '小さ':'ちいさ', '赤':'あか','青':'あお','黄色':'きいろ','白':'しろ','黒':'くろ','茶色':'ちゃいろ'},
    'かばん': {'新し':'あたらし', '古':'ふる','赤':'あか','青':'あお','黄色':'きいろ','白':'しろ','黒':'くろ','茶色':'ちゃいろ'},
    '辞書':{'高':'たか','安':'やす',},
    '本':{ 'おもしろ':'おもしろ', '高':'たか','安':'やす'},
},
'adj_for_Proff':{
    '先生':{'日本語':'японского языка','英語':'английского языка'},
    '大学生':{'東京の大学':'Токийского университета','文学部':'факультета литературы','歴史部':'факультета истории','医学部':'медицинского факультета'},
},
'adj_for_Proff_hir':{
    '先生':{'日本語':'にほんご','英語':'えいご'},
    '大学生':{'東京の大学':'とうきょうのだいがく','文学部':'ぶんがくぶ','歴史部':'れきしぶ','医学部':'いがくぶ'},
},

# Суффиксы
'suff':{'さん':'-сан','くん':'-кун'},
'suff_no':{'さん':'-сана','くん':'-куна'},

# Места
'buildings' : {'学校':'школа','駅':'станция','家':'дом','公園':'парк','図書館':'библиотека','大学':'университет','デパート':'универмаг','喫茶店':'кафе','店':'магазин','本屋':'книжный магазин','花屋':'цветочный магазин','魚屋':'рыбный магазин','果物屋':'фруктовый магазин',},
'buildings_hir': {'学校': 'がっこう', '駅': 'えき', '家': '公園', 'こうえん': 'こうえん', '図書館': 'としょかん', '大学': 'だいがく',   'デパート': 'デパート','喫茶店':'きっさてん','店':'みせ','本屋':'ほんや','花屋':'はなや','魚屋':'さかなや','果物屋':'くだものや',},

'end_build2' : {'学校':'в школу','駅':'на станцию','家':'домой','公園':'в парк','図書館':'в библиотеку','大学':'в университет','デパート':'в универмаг','喫茶店':'в кафе','店':'в магазин','本屋':'в книжный магазин','花屋':'в цветочный магазин','魚屋':'в рыбный магазин','果物屋':'в фруктовый магазин'},
# Глаголы и их формы

'glagol': {'行': "い", '帰': 'かえ', '歩': 'ある',},
}


var_glag = {
    'yes':{
        'form_pres':{'jap':{ '行':'き','帰':'り','歩':'き'},
                    'rus':{'行':'идёт','帰':'возвращается','歩':'идёт пешком'},
                    'des':'ます',
                    'dob':' - формально',
                    },
        'form_past':{'jap':{ '行':'き','帰':'り','歩':'き'},
                    'rus':{'行':'пришёл', '帰':'вернулся', '歩':'пришёл пешком'},
                    'des':'ました',
                    'dob':' - формально'},
        'fri_pres':{'jap':{ '行':'く','帰':'る','歩':'く'},
                    'rus':{'行':'идёт','帰':'возвращается','歩':'идёт пешком'},
                    'des':'',
                    'dob':' - фамильярно'},
        'fri_past':{'jap':{ '行':'った','帰':'った','歩':'いた'},
                    'rus':{'行':'пришёл', '帰':'вернулся', '歩':'пришёл пешком'},
                    'des':'',
                    'dob':'- фамильярно'},
        'form_desyou':{'jap':{ '行':'く','帰':'る','歩':'く'},
                    'rus':{'行':'наверное, идёт', '帰':'наверное, возвращается', '歩':'наверное, идёт пешком'},
                    'des':'でしょう',
                    'dob':' - формально'},
        'fri_desyou':{'jap':{ '行':'く','帰':'る','歩':'く'},
                    'rus':{'行':'наверное, идёт','帰':'наверное,возвращается','歩':'наверное, идёт пешком'},
                    'des':'だろう',
                    'dob':' - фамильярно'},
        'deepr':{'jap':{ '行':'って','帰':'って','歩':'いて'},
                    'rus':{'行':'идя','帰':'возвращаясь','歩':'идя пешком'},
                    'des':'',
                    'dob':''},
        },
    'no':{
        'form_pres':{'jap':{ '行':'き','帰':'り','歩':'き'},
                    'rus':{'行':'не идёт','帰':'не возвращается','歩':'не идёт пешком'},
                    'des':'ません',
                    'dob':' - формально',
                    },
        'form_past':{'jap':{ '行':'き','帰':'り','歩':'き'},
                    'rus':{'行':'не пришёл', '帰':'не вернулся', '歩':'не пришёл пешком'},
                    'des':'ませんでした',
                    'dob':' - формально'},
        'fri_pres':{'jap':{ '行':'か','帰':'ら','歩':'か'},
                    'rus':{'行':'не идёт','帰':'не возвращается','歩':'не идёт пешком'},
                    'des':'ない',
                    'dob':' - фамильярно'},
        'fri_past':{'jap':{ '行':'か','帰':'ら','歩':'か'},
                    'rus':{'行':'не пришёл', '帰':'не вернулся', '歩':'не пришёл пешком'},
                    'des':'かった',
                    'dob':'- фамильярно'},
        'form_desyou':{'jap':{ '行':'か','帰':'ら','歩':'か'},
                    'rus':{'行':'наверное, не идёт', '帰':'наверное, не возвращается', '歩':'наверное, не идёт пешком'},
                    'des':'ないでしょう',
                    'dob':' - формально'},
        'fri_desyou':{'jap':{ '行':'か','帰':'ら','歩':'か'},
                    'rus':{'行':'наверное, не идёт','帰':'наверное, не возвращается','歩':'наверное,не идёт пешком'},
                    'des':'ないだろう',
                    'dob':' - фамильярно'},
        'deepr':{'jap':{ '行':'かないで','帰':'らないで','歩':'かないで'},
                    'rus':{'行':'не идя','帰':'не возвращаясь','歩':'не идя пешком'},
                    'des':'',
                    'dob':''},
        },
}

def glag_vars(yn,var):
    ran_glag = ran(a['glagol'])
    glag_jap = ran_glag + var_glag[yn][var]['jap'][ran_glag]
    glag_hir = a['glagol'][ran_glag] + var_glag[yn][var]['jap'][ran_glag]
    glag_rus = var_glag[yn][var]['rus'][ran_glag]
    dob = var_glag[yn][var]['dob']
    desu = var_glag[yn][var]['des']
    build = ran(a['buildings'])
    build_hir = a['buildings_hir'][build]
    build_end = a['end_build2' ][build]
    jap = [build,'へ',glag_jap,desu]
    hir = ' '.join([build_hir,'へ',glag_hir,desu])
    rus = ' '.join([glag_rus,build_end,dob])
    jap = ' '.join(jap)
    return jap,hir,rus

def who_f(end,suff): # выбор имени/человека 
    list_who = random.choice((a['names'],a['family']))
    who = ran(list_who)
    if who in a['names']:
        jap_suff = ran(a['suff'])
        rus_who = a['names'][who]+a[suff][jap_suff]
        hir_who = a['names_hir'][who]+jap_suff
        who= who+jap_suff
    else:
        rus_who=a[end][who]
        hir_who = a['family_hur'][who]
    return who, hir_who,rus_who

var_desu = {
    'yes':{
    'form_pres':{'jap':'です','rus':' - формально','ne':''},
    'form_past':{'jap':'でした','rus':' - формально','ne':''},
    'fri_pres':{'jap':'だ','rus':' - фамильярно','ne':''},
    'fri_past':{'jap':'だった','rus':'- фамильярно','ne':''},
    'form_desyou':{'jap':'でしょう','rus':' - формально','ne':', наверное, '},
    'fri_desyou':{'jap':'だろう','rus':' - фамильярно','ne':', наверное,'},
    'deepr':{'jap':'で','rus':' - перечисление','ne':''},
    },
    'no':{
    'form_pres':{'jap':'ではありません','rus':' - формально','ne':' не '},
    'form_past':{'jap':'ではありませんでした','rus':' - формально','ne':' не '},
    'fri_pres':{'jap':'ではない','rus':' - фамильярно','ne':' не '},
    'fri_past':{'jap':'ではなかった','rus':'- фамильярно','ne':' не '},
    'form_desyou':{'jap':'ではないでしょう','rus':' - формально','ne':', наверное, не'},
    'fri_desyou':{'jap':'ではないだろう','rus':' - фамильярно','ne':', наверное, не'},
    'deepr':{'jap':'ではないで','rus':' - перечисление','ne':'не'},
    }
}

var_pril = {
    'yes':{
    'form_pres':{'jap':'いです','rus':' - формально','ne':''},
    'form_past':{'jap':'かったです','rus':' - формально','ne':'был'},
    'form_pres':{'jap':'い','rus':' -  фамильярно','ne':''},
    'form_past':{'jap':'かった','rus':' - фамильярно','ne':'был'},
    'form_desyou':{'jap':'いでしょう','rus':' -　формально','ne':', наверное,'},
    'fri_desyou':{'jap':'かったとでしょう','rus':' - фамильярно','ne':', наверное,'},
    'deepr':{'jap':'くて','rus':' - перечисление','ne':''},
    },
    'no':{
    'form_pres':{'jap':'くありません','rus':' - формально','ne':' не '},
    'form_past':{'jap':'くなかったです','rus':' - формально','ne':' не был'},
    'form_pres':{'jap':'くない','rus':' - фамильярно','ne':' не '},
    'form_past':{'jap':'くなかった','rus':' - фамильярно','ne':' не был'},
    'form_desyou':{'jap':'くないでしょう','rus':' - формально','ne':', наверное, не'},
    'fri_desyou':{'jap':'くなかったとでしょう','rus':' - фамильярно','ne':', наверное, не'},
    'deepr':{'jap':'くなくて','rus':' - перечисление','ne':'не'},
    }
}

def desu_vars(yn,var):
    des_jap = var_desu[yn][var]['jap']
    des_rus = var_desu[yn][var]['rus']
    ne = var_desu[yn][var]['ne']
    if random.randint(0,1)==0:
        jap_podl, jap_podl_hir, jap_podl_rus = who_f('family','suff')
        count = 'one'
        who = ran(a['profession'])
    else:
        jap_podl, jap_podl_hir, jap_podl_rus = ('この人','このひと','он')
        count = 'many'
        who = ran(a['profession_many'])
    who_hir = a['profession_hir'][who]
    if jap_podl in a['family']:
        dop1 = ran(a['names'])
        dop1_hir = a['names_hir'][dop1]+'さん'+'の'
        dop1_rus = a['end_names'][dop1]+'-сан'
        dop1=dop1+'さん'+'の'
    else:
        dop1,dop1_hir,dop1_rus = ['','','']
    prop_jap = ran(a['adj_for_Proff'][who])
    prop_hir = a['adj_for_Proff_hir'][who][prop_jap]+ 'の'
    prop_rus = a['adj_for_Proff'][who][prop_jap]
    prop_jap = prop_jap + 'の'
    if var=='form_past' or var=='fri_past':
        if count =='one':
            end = 'end_profession'
            ha = ' был '
        else:
            end = 'end_profession_many'
            ha = ' были '
    else:
        if count =='one':
            end = 'profession'
            ha = ' - '
        else:
            end = 'profession_many'
            ha = ' - '
    jap = [dop1,jap_podl,'は',prop_jap,who,des_jap]
    hir = ' '.join([dop1_hir,jap_podl_hir,'は',prop_hir,who_hir,des_jap])
    rus = ' '.join([jap_podl_rus,dop1_rus,ha,ne,a[end][who],prop_rus, des_rus])
    jap = ' '.join(jap)
    return jap,hir,rus

def pril_vars(yn, var):
    des_jap = var_pril[yn][var]['jap']
    des_rus = var_pril[yn][var]['rus']
    ne = var_pril[yn][var]['ne']
    un = ran(a['uno'])
    un_rus = a['uno'][un]
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['small object'][obj]
    pril_jap = ran(a['adj_for_small_object'][obj])
    pril_hir = a['adj_for_small_object_hir'][obj][pril_jap]
    pril_rus = a['adj_for_small_object'][obj][pril_jap]
    jap = [un,obj,'は',pril_jap,des_jap]
    hir = ' '.join([un,obj_hir,'は',pril_hir,des_jap])
    rus = ' '.join([un_rus,obj_rus,ne,pril_rus,des_rus])
    jap = ' '.join(jap)
    return jap,hir,rus