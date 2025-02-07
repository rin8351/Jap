import random 

def ran(x):
    return random.choice(list(x.keys())) 

def lists_words_suff():
    sp = []
    for i in a:
        sp.append(jinn(i))
    for i in a_2:
        sp.append(jinn_2(i))
    return sp

a={
    '学':{
        'words': {'物理': 'ぶつり','言語':'げんご','植物':'しょくぶつ', '動物':'どうぶつ','心理':'しんり','化':'かがく','生物':'せいぶつ','歴史':'れきし','地理':'ちり','文':'ぶん','医':'い'},
        'trans':{
            '物理':'закон природы','言語':'язык','植物':'растение', '動物':'животное','心理':'психология','化':'трансформация','生物':'существо',
            '歴史':'история','地理':'география','文':'литература','医':'медицина'},
        'answer':{
            '物理学':'Физика', '言語学':'Лингвистика','植物学':'ботаника','動物学':'зоология','心理学':'психология','化学':'химия','生物学':'биология',
            '歴史学':'история','地理学':'география','文学':'литература','医学':'медицина'},
        'reading':{
            '物理学':'ぶつりがく', '言語学':'げんごがく','植物学':'しょくぶつがく','動物学':'どうぶつがく','心理学':'しんりがく','化学':'かがく','生物学':'せいぶつがく',
            '歴史学':'れきしがく','地理学':'ちりがく','文学':'ぶんがく','医学':'いがく'},
            },
    '人': {
            'words':{'日本':'にほん','ロシア':'ロシア','中国':'ちゅうごく','アメリカ':'アメリカ'},
            'trans':{'日本':'Япония','ロシア':'Россия','中国':'Китай','アメリカ':'Америка'},
            'answer':{'日本人':'японец','ロシア人':'русский','中国人':'китаец','アメリカ人':'американец'},
            'reading':{'日本人':'にほんじん','ロシア人':'ロシアじん','中国人':'ちゅうごくじん','アメリカ人':'アメリカじん'},},
    '式':{
        'words':{ '日本':'にほん','中国':'ちゅうごく','学校':'がっこう','料理':'りょうり','家庭':'かてい'},
        'trans':{'日本':'Япония','中国':'Китай','学校':'школа','料理':'кухня','家庭':'семья'},
        'answer':{'日本式':'японский стиль','中国式':'китайский стиль','学校式':'школьный стиль','料理式':'кулинарный стиль','家庭式':'семейный стиль'},
        'reading':{'日本式':'にほんしき','中国式':'ちゅうごくしき','学校式':'がっこうしき','料理式':'りょうりしき','家庭式':'かていしき'},
    },
    '先':{
        'words':{'出発':'しゅっぱつ','着地':'ちゃくち','旅行':'りょこう','勉強':'べんきょう','結婚':'けっこん','食事':'しょくじ'},
        'trans':{'出発':'отправление','着地':'прибытие','旅行':'путешествие','勉強':'учеба','結婚':'свадьба','食事':'еда'},
        'answer':{'出発先':'место отправления','着地先':'место прибытия','旅行先':'место путешествия','勉強先':'место учебы','結婚先':'место свадьбы','食事先':'место еды'},
        'reading':{'出発先':'しゅっぱつさき','着地先':'ちゃくちさき','旅行先':'りょこうさき','勉強先':'べんきょうさき','結婚先':'けっこんさき','食事先':'しょくじさき'},
        },
    '中 (じゅう)':{
        'words':{'朝':'あさ','昼間':'ひるま','夜':'よる','午前':'ごぜん','午後':'ごご','週':'しゅう','月':'つき','年':'とし'},
        'trans':{'朝':'утро','昼間':'день','夜':'вечер','午前':'утро','午後':'вечер','週':'неделя','月':'месяц','年':'год'},
        'answer':{'朝中':'всё утро','昼間中':'весь день','夜中':'всю ночь','午前中':'в течение утра','午後中':'в течение вечера','週中':'в течение недели','月中':'в течение месяца','年中':'в течение года'},
        'reading':{'朝中':'あさじゅう','昼間中':'ひるまじゅう','夜中':'よるじゅう','午前中':'ごぜんじゅう','午後中':'ごごじゅう','週中':'しゅうじゅう','月中':'つきじゅう','年中':'としじゅう'},
        },
    '中 (ちゅう)':{
        'words': {'勉強':'べんきょう', '作業':'さぎょう','食事':'しょくじ','旅行':'りょこう','睡眠':'すいみん', '旅行':'りょこう', '話':'はなし'},
        'trans':{'勉強':'учеба', '作業':'работа','食事':'еда','旅行':'путешествие','睡眠':'сон', '旅行':'путешествие', '話':'разговор'},
        'answer':{'勉強中':'во время учебы', '作業中':'во время работы','食事中':'во время еды','旅行中':'во время путешествия','睡眠中':'во время сна', '旅行中':'во время путешествия', '話中':'во время разговора'},
        'reading':{'勉強中':'べんきょうちゅう', '作業中':'さぎょうちゅう','食事中':'しょくじちゅう','旅行中':'りょこうちゅう','睡眠中':'すいみんちゅう', '旅行中':'りょこうちゅう', '話中':'はなしちゅう'},
        },
    '屋':{
        'words':{'本':'ほん','花':'はな','魚':'さかな','果物':'くだもの'},
        'trans':{'本':'книга','花':'цветок','魚':'рыба','果物':'фрукт'},
        'answer':{'本屋':'книжный магазин','花屋':'цветочный магазин','魚屋':'рыбный магазин','果物屋':'фруктовый магазин'},
        'reading':{'本屋':'ほんや','花屋':'はなや','魚屋':'さかなや','果物屋':'くだものや'},
        },
    '的':{
        'words':{'歴史':'れきし','科学': 'かがく','実用':'じつよう','国際':'こくさい','個人':'こじん','政治':'せいじ','経済':'けいざい','哲学':'てつがく','文学':'ぶんがく','法律':'ほうりつ','医学':'いがく','工学':'こうがく','経営':'けいえい','情報':'じょうほう','教育':'きょういく','美術':'びじゅつ','建築':'けんちく','料理':'りょうり','旅行':'りょこう','自然':'しぜん','宇宙':'うちゅう','社会':'しゃかい','人間':'にんげん','生活':'せいかつ','健康':'けんこう','環境':'かんきょう','日本':'にほん','ロシア':'ロシア','中国':'ちゅうごく','アメリカ':'アメリカ'},
        'trans':{'歴史':'история','科学': 'наука','実用':'практичность','国際':'международный','個人':'личный','政治':'политика','経済':'экономика','哲学':'философия','文学':'литература','法律':'право','医学':'медицина','工学':'инженерия','経営':'управление','情報':'информация','教育':'образование','美術':'живопись','建築':'архитектура','料理':'кухня','旅行':'путешествие','自然':'природа','宇宙':'космос','社会':'общество','人間':'человек','生活':'жизнь','健康':'здоровье','環境':'окружающая среда','日本':'Япония','ロシア':'Россия','中国':'Китай','アメリカ':'Америка'},
        'answer':{'歴史的':'исторический','科学的': 'научный','実用的':'практичный','国際的':'международный','個人的':'личный','政治的':'политический','経済的':'экономический','哲学的':'философский','文学的':'литературный','法律的':'правовой','医学的':'медицинский','工学的':'инженерный','経営的':'управленческий','情報的':'информационный','教育的':'образовательный','美術的':'живописный','建築的':'архитектурный','料理的':'кулинарный','旅行的':'путешественный','自然的':'естественный','宇宙的':'космический','社会的':'социальный','人間的':'человеческий','生活的':'жизненный','健康的':'здоровый','環境的':'экологический','日本的':'японский','ロシア的':'русский','中国的':'китайский','アメリカ的':'американский'},
        'reading':{'歴史的':'れきしてき','科学的': 'かがくてき','実用的':'じつようてき','国際的':'こくさいてき','個人的':'こじんてき','政治的':'せいじてき','経済的':'けいざいてき','哲学的':'てつがくてき','文学的':'ぶんがくてき','法律的':'ほうりつてき','医学的':'いがくてき','工学的':'こうがくてき','経営的':'けいえいてき','情報的':'じょうほうてき','教育的':'きょういくてき','美術的':'びじゅつてき','建築的':'けんちくてき','料理的':'りょうりてき','旅行的':'りょこうてき','自然的':'しぜんてき','宇宙的':'うちゅうてき','社会的':'しゃかいてき','人間的':'にんげんてき','生活的':'せいかつてき','健康的':'けんこうてき','環境的':'かんきょうてき','日本的':'にほんてき','ロシア的':'ロシアてき','中国的':'ちゅうごくてき','アメリカ的':'アメリカてき'},
},
    '師':{
        'words':{'教':'きょう','料理':'りょうり','旅行':'りょこう','自然':'しぜん','宇宙':'うちゅう','社会':'しゃかい','人間':'にんげん','生活':'せいかつ','健康':'けんこう','環境':'かんきょう','医':'い','美容':'びよう'},
        'trans':{'教':'учитель','料理':'кулинария','旅行':'путешествие','自然':'природа','宇宙':'космос','社会':'общество','人間':'человек','生活':'жизнь','健康':'здоровье','環境':'окружающая среда','医':'медицина','美容':'косметика'},
        'answer':{'教師':'учитель','料理師':'повар','旅行師':'путешественник','自然師':'природовед','宇宙師':'космонавт','社会師':'социолог','人間師':'антрополог','生活師':'жизненный тренер','健康師':'врач','環境師':'эколог','医師':'врач','美容師':'косметолог'},
        'reading':{'教師':'きょうし','料理師':'りょうりし','旅行師':'りょこうし','自然師':'しぜんし','宇宙師':'うちゅうし','社会師':'しゃかいし','人間師':'にんげんし','生活師':'せいかつし','健康師':'けんこうし','環境師':'かんきょうし','医師':'いし','美容師':'びようし'},
},
    'さ':{
        'words':{'広':'ひろ','べんり':'べんり','新し':'あたらし','古':'ふる','高':'たか','安':'やす','長':'なが','早':'はや','暑':'あつ','寒':'さむ','強':'つよ',},
        'trans':{'広':'широкий','べんり':'удобный','新し':'новый','古':'старый','高':'дорогой','安':'дешевый','長':'длинный','早':'быстрый','暑':'жаркий','寒':'холодный','強':'сильный',},
        'answer':{'広さ':'ширина','べんりさ':'удобство','新しさ':'новизна','古さ':'старость','高さ':'дороговизна','安さ':'дешевизна','長さ':'длина','早さ':'быстрота','暑さ':'жара','寒さ':'холод','強さ':'сила',},
        'reading':{'広さ':'ひろさ','べんりさ':'べんりさ','新しさ':'あたらしさ','古さ':'ふるさ','高さ':'たかさ','安さ':'やすさ','長さ':'ながさ','早さ':'はやさ','暑さ':'あつさ','寒さ':'さむさ','強さ':'つよさ',},
    },
    'かえる':{
        'words':{'乗る':'のる','着る':'きる','入る':'はいる','立つ':'たつ','座る':'すわる','聞く':'きく','話す':'はなす','読む':'よむ','書く':'かく','作る':'つくる'},
        'trans':{'乗る':'садиться','着る':'одеваться','入る':'входить','立つ':'ставить','座る':'садиться','聞く':'спрашивать','話す':'говорить','読む':'читать','書く':'писать','作る':'делать'},
        '2_basis':{ '乗る':'乗り','着る':'着','入る':'入り','立つ':'立ち','座る':'座り','聞く':'聞き','話す':'話し','読む':'読み','書く':'書き','作る':'作り'},
        'answer':{'乗りかえる':'пересаживаться','着かえる':'переодеваться','入りかえる':'перемещаться','立ちかえる':'переставлять','座りかえる':'пересаживаться','聞きかえる':'переспрашивать','話しかえる':'переговариваться','読みかえる':'перечитывать','書きかえる':'переписывать','作りかえる':'переделывать'},
        'reading':{'乗りかえる':'のりかえる','着かえる':'きかえる','入りかえる':'いりかえる','立ちかえる':'たちかえる','座りかえる':'すわりかえる','聞きかえる':'ききかえる','話しかえる':'はなしかえる','読みかえる':'よみかえる','書きかえる':'かきかえる','作りかえる':'つくりかえる'},
    },
    '以':{
        'words':{'上':'じょう','下':'か','後':'ご','前':'ぜん','中':'ちゅう','間':'かん','内':'ない','外':'がい','左':'ひだり','右':'みぎ'},
        'trans':{'上':'верх','下':'низ','後':'после','前':'перед','中':'внутри','間':'между','内':'внутри','外':'снаружи','左':'левый','右':'правый'},
        'answer':{'以上':'больше','以下':'меньше','以後':'после','以前':'до','以内':'внутри','以外':'снаружи','以左':'левее','以右':'правее', '以中': 'внутри','以間':'между'},
        'reading':{'以上':'いじょう','以下':'いか','以後':'いご','以前':'いぜん','以内':'いない','以外':'いがい','以左':'いひだり','以右':'いみぎ', '以中': 'いちゅう','以間':'いかん'},
                   },
    '内':{
        'words':{'国':'くに','家':'いえ','学校':'がっこう','会社':'かいしゃ','病院':'びょういん','銀行':'ぎんこう','図書館':'としょかん','公園':'こうえん','駅':'えき','空港':'くうこう'},
        'trans':{'国':'страна','家':'дом','学校':'школа','会社':'компания','病院':'больница','銀行':'банк','図書館':'библиотека','公園':'парк','駅':'станция','空港':'аэропорт'},
        'answer':{'国内':'внутри страны','家内':'внутри дома','学校内':'внутри школы','会社内':'внутри компании','病院内':'внутри больницы','銀行内':'внутри банка','図書館内':'внутри библиотеки','公園内':'внутри парка','駅内':'внутри станции','空港内':'внутри аэропорта'},
        'reading':{'国内':'こくない','家内':'かない','学校内':'がっこうない','会社内':'かいしゃない','病院内':'びょういんない','銀行内':'ぎんこうない','図書館内':'としょかんない','公園内':'こうえんない','駅内':'えきない','空港内':'くうこうない'},
    },
    '見る':{
        'words':{'行く':'いく','読む':'よむ','着る':'きる','食べる':'たべる','見る':'みる','聞く':'きく','話す':'はなす','書く':'かく','作る':'つくる','買う':'かう','売る':'うる',},
        'trans':{'行く':'идти','読む':'читать','着る':'одевать','食べる':'есть','見る':'смотреть','聞く':'спрашивать','話す':'говорить','書く':'писать','作る':'делать','買う':'покупать','売る':'продавать',},
        '2_basis':{'行く':'行って','読む':'読んで','着る':'着て','食べる':'食べて','見る':'見て','聞く':'聞いて','話す':'話して','書く':'書いて','作る':'作って','買う':'買って','売る':'売って',},
        'answer':{'行ってみる':'пойти и посмотреть','読んでみる':'попытаться посмотреть','着てみる':'примерить','食べてみる':'попробовать (еду)','見てみる':'посмотреть','聞いてみる':'попробовать спросить','話してみる':'попробовать поговорить','書いてみる':'попробовать написать','作ってみる':'попробовать сделать','買ってみる':'попробовать купить','売ってみる':'попробовать продать'},
        'reading':{'行ってみる':'いってみる','読んでみる':'よんでみる','着てみる':'きてみる','食べてみる':'たべてみる', '見てみる':'みてみる','聞いてみる':'きいてみる','話してみる':'はなしてみる','書いてみる':'かいてみる','作ってみる':'つくってみる','買ってみる':'かってみる','売ってみる':'うってみる'},
    },
    '用':{
        'words':{'冬':'ふゆ','春':'はる','夏':'なつ','秋':'あき'},
        'trans':{'冬':'зима','春':'весна','夏':'лето','秋':'осень'},
        'answer':{'冬用':'зимний','春用':'весенний','夏用':'летний','秋用':'осенний'},
        'reading':{'冬用':'ふゆよう','春用':'はるよう','夏用':'なつよう','秋用':'あきよう'},
    },
    'すぎる':{
        'words':{'小さい':'ちいさい','大きい':'おおきい','高い':'たかい','安い':'やすい','長い':'ながい','早い':'はやい','暑い':'あつい','寒い':'さむい','強い':'つよい',},
        'trans':{'小さい':'маленький','大きい':'большой','高い':'дорогой','安い':'дешевый','長い':'длинный','早い':'быстрый','暑い':'жаркий','寒い':'холодный','強い':'сильный',},
        '2_basis':{ '小さい':'小さ','大きい':'大き','高い':'高','安い':'安','長い':'長','早い':'早','暑い':'暑','寒い':'寒','強い':'強',},
        'answer':{'小さすぎる':'слишком маленький','大きすぎる':'слишком большой','高すぎる':'слишком дорогой','安すぎる':'слишком дешевый','長すぎる':'слишком длинный','早すぎる':'слишком быстрый','暑すぎる':'слишком жаркий','寒すぎる':'слишком холодный','強すぎる':'слишком сильный',},
        'reading':{'小さすぎる':'ちいさすぎる','大きすぎる':'おおきすぎる','高すぎる':'たかすぎる','安すぎる':'やすすぎる','長すぎる':'ながすぎる','早すぎる':'はやすぎる','暑すぎる':'あつすぎる','寒すぎる':'さむすぎる','強すぎる':'つよすぎる',},
    },
    'こむ':{
        'words':{'入る':'はいる','出る':'でる','上がる':'あがる','下がる':'さがる','戻る':'もどる','向かう':'むかう','進む':'すすむ','帰る':'かえる','降りる':'おりる','通る':'とおる','過ぎる':'すぎる','抜ける':'ぬける','回る':'まわる','曲がる':'まがる','止まる':'とまる','立つ':'たつ','座る':'すわる','寝る':'ねる','泳ぐ':'およぐ','飛ぶ':'とぶ','走る':'はしる','歩く':'あるく','乗る':'のる',},
        'trans':{'入る':'входить','出る':'выходить','上がる':'подниматься','下がる':'опускаться','戻る':'возвращаться','向かう':'направляться','進む':'двигаться вперёд','帰る':'возвращаться','降りる':'спускаться','通る':'проходить','過ぎる':'проходить мимо','抜ける':'проходить через','回る':'поворачивать','曲がる':'поворачивать','止まる':'останавливаться','立つ':'вставать','座る':'садиться','寝る':'лечь','泳ぐ':'плавать','飛ぶ':'летать','走る':'бежать','歩く':'идти','乗る':'садиться',},
        '2_basis':{ '入る':'入り','出る':'出','上がる':'上がり','下がる':'下がり','戻る':'戻り','向かう':'向かい','進む':'進み','帰る':'帰り','降りる':'降り','通る':'通り','過ぎる':'過ぎ','抜ける':'抜け','回る':'回り','曲がる':'曲がり','止まる':'止まり','立つ':'立ち','座る':'座り','寝る':'寝','泳ぐ':'泳ぎ','飛ぶ':'飛び','走る':'走り','歩く':'歩き','乗る':'乗り'},  
         'answer':{'入りこむ':'войти','出こむ':'выходить','上がりこむ':'подняться','下がりこむ':'опуститься','戻りこむ':'вернуться','向かいこむ':'направиться','進みこむ':'двигаться вперёд','帰りこむ':'вернуться','降りこむ':'спуститься','通りこむ':'пройти','過ぎこむ':'пройти мимо','抜けこむ':'пройти через','回りこむ':'повернуть','曲がりこむ':'повернуть','止まりこむ':'остановиться','立ちこむ':'встать','座りこむ':'сесть','寝こむ':'лечь','泳ぎこむ':'плыть','飛びこむ':'лететь','走りこむ':'бежать','歩きこむ':'идти','乗りこむ':'сесть'},
         'reading':{'入りこむ':'はいりこむ','出こむ':'でこむ','上がりこむ':'あがりこむ','下がりこむ':'さがりこむ','戻りこむ':'もどりこむ','向かいこむ':'むかいこむ','進みこむ':'すすみこむ','帰りこむ':'かえりこむ','降りこむ':'おりこむ','通りこむ':'とおりこむ','過ぎこむ':'すぎこむ','抜けこむ':'ぬけこむ','回りこむ':'まわりこむ','曲がりこむ':'まがりこむ','止まりこむ':'とまりこむ','立ちこむ':'たちこむ','座りこむ':'すわりこむ','寝こむ':'ねこむ','泳ぎこむ':'およぎこむ','飛びこむ':'とびこむ','走りこむ':'はしりこむ','歩きこむ':'あるきこむ','乗りこむ':'のりこむ'},
    },
    'した':{
        'words':{'ちょｔっと':'ちょっと','すこし':'すこし','もう少し':'もうすこし', },
        'trans':{'ちょｔっと':'немного','すこし':'немного','もう少し':'ещё немного', },
        'answer':{'ちょっとした':'незначительный','すこしした':'немного','もうすこしした':'ещё немного',},
        'reading':{'ちょっとした':'ちょっとした','すこしした':'すこしした','もうすこしした':'もうすこしした',},
    },
    '直す':{
        'words':{'建てる':'たてる','作る':'つくる','書く':'かく','読む':'よむ','話す':'はなす'},
        'trans':{'建てる':'строить','作る':'готовить','書く':'писать','読む':'читать','話す':'говорить'},
        '2_basis':{ '建て':'建て','作る':'作って','書く':'書って','読む':'読んで','話す':'話して'},
        'answer':{'建て直す':'перестроить','作り直す':'переделать','書き直す':'переписать','読み直す':'перечитать','話し直す':'переговорить'},
        'reading':{'建て直す':'たてなおす','作り直す':'つくりなおす','書き直す':'かきなおす','読み直す':'よみなおす','話し直す':'はなしなおす'},
    },
    '合う':{
        "words":{'話す':'はなす','見る':'みる','助ける':'たすける','知る':'しる','遊ぶ':'あそぶ',},
        'trans':{'話す':'разговор','見る':'видеться','助ける':'помощь','知る':'знать','遊ぶ':'играть'},
        '2_basis':{ '話す':'話し','見る':'見','助ける':'助け','知る':'知り','遊ぶ':'遊び'},
        'answer':{'話し合う':'поговорить','見合う':'встречаться','助け合う':'помогать друг другу','知り合う':'познакомиться','遊び合う':'играть вместе'},
        'reading':{'話し合う':'はなしあう','見合う':'みあう','助け合う':'たすけあう','知り合う':'しりあう','遊び合う':'あそびあう'},
    },
    'すぎる':{
        'words':{'食べる':'たべる','飲む':'のむ','寝る':'ねる','働く':'はたらく','遊ぶ':'あそぶ','泳ぐ':'およぐ',},
        'trans':{'食べる':'есть','飲む':'пить','寝る':'спать','働く':'работать','遊ぶ':'играть','泳ぐ':'плавать',},
        '2_basis':{ '食べる':'食べ','飲む':'飲み','寝る':'寝','働く':'働き','遊ぶ':'遊び','泳ぐ':'泳ぎ'},
        'answer':{'食べすぎる':'переедать','飲みすぎる':'перепить','寝すぎる':'переспать','働きすぎる':'переработать','遊びすぎる':'переиграть','泳ぎすぎる':'переплыть'},
        'reading':{'食べすぎる':'たべすぎる','飲みすぎる':'のみすぎる','寝すぎる':'ねすぎる','働きすぎる':'はたらきすぎる','遊びすぎる':'あそびすぎる','泳ぎすぎる':'およぎすぎる'},
    },
    'おき':{
        'words':{'朝':'あさ','昼':'ひる','夜':'よる','日':'ひ','月':'つき','年':'とし'},
        'trans':{'朝':'утро','昼':'день','夜':'вечер','日':'день','月':'месяц','年':'год'},
        'answer':{'朝おき':'через утро','昼おき':'через день','夜おき':'через вечер','日おき':'через день','月おき':'через месяц','年おき':'через год'},
        'reading':{'朝おき':'あさおき','昼おき':'ひるおき','夜おき':'よるおき','日おき':'ひおき','月おき':'つきおき','年おき':'としおき'},
    },
    'やすい':{
        'words':{'食べる':'たべる','飲む':'のむ','働く':'はたらく','遊ぶ':'あそぶ','泳ぐ':'およぐ',},
        'trans':{'食べる':'есть','飲む':'пить','働く':'работать','遊ぶ':'играть','泳ぐ':'плавать',},
        '2_basis':{ '食べる':'食べ','飲む':'飲み','働く':'働き','遊ぶ':'遊び','泳ぐ':'泳ぎ'},
        'answer':{'食べやすい':'легко есть','飲みやすい':'легко пить','働きやすい':'легко работать','遊びやすい':'легко играть','泳ぎやすい':'легко плавать'},
        'reading':{'食べやすい':'たべやすい','飲みやすい':'のみやすい','働きやすい':'はたらきやすい','遊びやすい':'あそびやすい','泳ぎやすい':'およぎやすい'},
    },
    '風':{
        'words':{'日本':'にほん', '西洋':'せいよう','東洋':'とうよう','アジア':'アジア','ヨーロッパ':'ヨーロッパ',},
        'trans':{'日本':'Япония','西洋':'Запад','東洋':'Восток','アジア':'Азия','ヨーロッパ':'Европа',},
        'answer':{'日本風':'японский стиль','西洋風':'западный стиль','東洋風':'восточный стиль','アジア風':'азиатский стиль','ヨーロッパ風':'европейский стиль',},
        'reading':{'日本風':'にほんふう','西洋風':'せいようふう','東洋風':'とうようふう','アジア風':'アジアふう','ヨーロッパ風':'ヨーロッパふう'},
    },
    '諸':{
        'words':{'国':'くに','家':'いえ','学校':'がっこう','会社':'かいしゃ','病院':'びょういん','銀行':'ぎんこう','図書館':'としょかん','公園':'こうえん','駅':'えき','空港':'くうこう'},
        'trans':{'国':'страна','家':'дом','学校':'школа','会社':'компания','病院':'больница','銀行':'банк','図書館':'библиотека','公園':'парк','駅':'станция','空港':'аэропорт'},
        'answer':{'諸国':'разные страны','諸家':'разные дома','諸学校':'разные школы','諸会社':'разные компании','諸病院':'разные больницы','諸銀行':'разные банки','諸図書館':'разные библиотеки','諸公園':'разные парки','諸駅':'разные станции','諸空港':'разные аэропорты'},
        'reading':{'諸国':'しょこく','諸家':'しょか','諸学校':'しょがっこう','諸会社':'しょかいしゃ','諸病院':'しょびょういん','諸銀行':'しょぎんこう','諸図書館':'しょとしょかん','諸公園':'しょこうえん','諸駅':'しょえき','諸空港':'しょくうこう'},
    },
    '各': {
        'words':{'国':'くに','家':'いえ','学校':'がっこう','会社':'かいしゃ','病院':'びょういん','銀行':'ぎんこう','図書館':'としょかん','公園':'こうえん','駅':'えき','空港':'くうこう'},
        'trans':{'国':'страна','家':'дом','学校':'школа','会社':'компания','病院':'больница','銀行':'банк','図書館':'библиотека','公園':'парк','駅':'станция','空港':'аэропорт'},
        'answer':{'各国':'каждая страна','各家':'каждый дом','各学校':'каждая школа','各会社':'каждая компания','各病院':'каждая больница','各銀行':'каждый банк','各図書館':'каждая библиотека','各公園':'каждый парк','各駅':'каждая станция','各空港':'каждый аэропорт'},
        'reading':{'各国':'かくこく','各家':'かくいえ','各学校':'かくがっこう','各会社':'かくかいしゃ','各病院':'かくびょういん','各銀行':'かくぎんこう','各図書館':'かくとしょかん','各公園':'かくこうえん','各駅':'かくえき','各空港':'かくくうこう'},
    },
    '化':{
        'words':{'近代':'きんだい','国際':'こくさい','都市':'とし','工業 ':'こうぎょう'},
        'trans':{'近代':'современность','国際':'международный','都市':'город','工業':'промышленность'},
        'answer':{'近代化':'модернизация','国際化':'интернационализация','都市化':'урбанизация','工業化':'индустриализация'},
        'reading':{'近代化':'きんだいか','国際化':'こくさいか','都市化':'としか','工業化':'こうぎょうか'},
    },
    '性':{
        'words':{'重要':'じゅうよう','可能':'かのう','必要 ':'ひつよう','安全 ':'あんぜん','柔軟 ':'じゅうなん'},
        'trans':{'重要':'важный','可能':'возможный','必要':'необходимый','安全':'безопасный','柔軟':'гибкий'},
        'answer':{'重要性':'важность','可能性':'возможность','必要性':'необходимость','安全性':'безопасность','柔軟性':'гибкость'},
        'reading':{'重要性':'じゅうようせい','可能性':'かのうせい','必要性':'ひつようせい','安全性':'あんぜんせい','柔軟性':'じゅうなんせい'},
    },
    '向け':{
        'words':{'男':'おとこ','女':'おんな','子供':'こども','学生':'がくせい','初心者':'しょしんしゃ'},
        'trans':{'男':'мужчина','女':'женщина','子供':'ребёнок','学生':'студент','初心者':'новичок'},
        'answer':{'男向け':'для мужчин','女向け':'для женщин','子供向け':'для детей','学生向け':'для студентов','初心者向け':'для новичков'},
        'reading':{'男向け':'おとこむけ','女向':'おんなむけ','子供向け':'こどもむけ','学生向け':'がくせいむけ','初心者向け':'しょしんしゃむけ'},
    },
    '不':{
        'words':{'可能':'かのう','正確':'せいかく','適切':'てきせつ','安全':'あんぜん','確実':'かくじつ'},
        'trans':{'可能':'возможный','正確':'точный','適切':'подходящий','安全':'безопасный','確実':'надёжный'},
        'answer':{'不可能':'невозможный','不正確':'неточный','不適切':'неподходящий','不安全':'небезопасный','不確実':'ненадёжный'},
        'reading':{'不可能':'ふかのう','不正確':'ふせいかく','不適切':'ふてきせつ','不安全':'ふあんぜん','不確実':'ふかくじつ'},
    },
    '主義':{
        'words':{'自由':'じゆう','平和':'へいわ','民主':'みんしゅ','社会':'しゃかい','共産':'きょうさん'},
        'trans':{'自由':'свобода','平和':'мир','民主':'демократия','社会':'общество','共産':'коммунизм'},
        'answer':{'自由主義':'либерализм','平和主義':'пацифизм','民主主義':'демократия','社会主義':'социализм','共産主義':'коммунизм'},
        'reading':{'自由主義':'じゆうしゅぎ','平和主義':'へいわしゅぎ','民主主義':'みんしゅしゅぎ','社会主義':'しゃかいしゅぎ','共産主義':'きょうさんしゅぎ'},
    },
    'ひ':{
        'words':{'影響':'えいきょう','害 ':'がい','告':'つげ','損':'そこく','災':'わざわい'},
        'trans':{'影響':'влияние','害':'вред','告':'сообщение','損':'потеря','災':'беда'},
        'answer':{'影響ひ':'подверженный влиянию','害ひ':'понесенный ущерб, урон','告ひ':'полученное сообщение','損ひ':'понесенные потери','災ひ':'понесенные бедствия'},
        'reading':{'影響ひ':'えいきょうひ','害':'がいひ','告':'つげひ','損':'そこくひ','災':'わざわいひ'},
        }
    },

a_2={
        '和':{
        'words':{'食事':'しょくじ','料理':'りょうり','家庭':'かてい','生活':'せいかつ','医':'い','服':'ふく','間':'ま'},
        'trans':{'食事':'еда','料理':'кулинария','家庭':'семья','生活':'жизнь','医':'медицина','服':'одежда','間':'комната'},
        'answer':{'和食事':'японская еда','和料理':'японская кухня','和家庭':'японская семья','和生活':'японская жизнь','和医':'японская медицина','和服':'японская одежда','和間':'японская комната'},
        'reading':{'和食事':'わしょくじ','和料理':'わりょうり','和家庭':'わかてい','和生活':'わせいかつ','和医':'わい','和服':'わふく','和間':'わま'},
    },
    
    '真':{
        'words' :{'白':'しろ','赤':'あか','中':'ちゅう','黒':'くろ','青':'あお','緑':'みどり','黄色':'きいろ','茶色':'ちゃいろ'}, 
        'trans':{'白':'белый','赤':'красный','中':'средний','黒':'чёрный','青':'синий','緑':'зелёный','黄色':'жёлтый','茶色':'коричневый'},
        'answer':{'真っ白':'снежно-белый','真っ赤':'ярко-красный','真っ黒':'чёрный как смоль','真っ青':'ярко-синий','真っ緑':'ярко-зелёный','真っ黄色':'ярко-жёлтый','真っ茶色':'тёмно-коричневый','真っ中':'самый центральный'},
        'reading':{'真っ白':'まっしろ','真っ赤':'まっか','真っ黒':'まっくろ','真っ青':'まっさお','真っ緑':'まっみどり','真っ黄色':'まっきいろ','真っ茶色':'まっちゃいろい','真っ中':'まっちゅう'},
    }
}


def jinn(suff):
    rand = ran(a[suff]['words'])
    rand_origin = rand
    if suff=='中 (じゅう)' or suff=='中 (ちゅう)':
        suff1 = '中'
    else:
        suff1=suff
    if suff == '見る':
        suff1 = 'みる'
    if suff == 'かえる' or suff == '見る' or suff == 'すぎる':
        rand = a[suff]['2_basis'][rand]
    rand2 = rand + suff1
    if suff == '以':
        rand2 = suff + rand
    hir = a[suff]['reading'][rand2]
    jap = rand +suff1+ '   ( '+ rand+ ' - '+ a[suff]['trans'][rand_origin]+' )'
    if suff =='和' or suff == '以':
        rand = suff + rand
    elif suff == '真':
        rand = suff+ 'っ' +rand
    else:
        rand=rand+suff1
    rus = a[suff]['answer'][rand]
    return jap,hir,rus

def jinn_2(suff):
    rand = ran(a_2[suff]['words'])
    if suff == '真':
        rand2 = suff+ 'っ' +rand
    else:
        rand2 = suff+rand
    hir = a_2[suff]['reading'][rand2]
    jap = rand2 + '   ( '+ rand+ ' - '+ a_2[suff]['trans'][rand]+' )'     
    rus = a_2[suff]['answer'][rand2]
    return jap,hir,rus