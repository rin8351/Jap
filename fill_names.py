def lists_words_names():
    sp = []
    for i in names:
        sp.append(names_jap(i))
    return sp

names= {'大田':'Оода','本山': 'Мотояма','三田': 'Кида','山本': 'Ямамото','室木':'Муроки','山部':'Ямабе',
            '大友': 'Оотомо',
    '友部': 'Томобе',
    '大高': 'Оотака',
    '小山': 'Коояма',
    '小室': 'Комуро',
    '近田': 'Чикада',
    '高木': 'Такаги',
    '新山': 'Ниияма',
    '大月': 'Ооцуки',
    '高月': 'Такацуки',
    '百田': 'Момота',
    '白山': 'Хакуяма',
    '明本': 'Акимото',
        '前山': 'Маэяма',
    '前田': 'Маэда',
    '金田': 'Канэда',
    '堂本': 'Домото',
    '白金': 'Сирокане',
    '時田': 'Токита',
    '大前': 'Оомаэ',
    '金木': 'Канэки',
    '時山': 'Токияма',
        '上山': 'Камияма',
    '今上': 'Имагами',
    '松田': 'Мацуда',
    '高松': 'Такамацу',
    '宅前': 'Такумаэ',
    '池上': 'Икегами',
    '田所': 'Тадокоро',
    '水上': 'Мидзуками',
    '近松': 'Тикамацу',
    '大下': 'Оосита',
    '山下': 'Ямасита',
    '三上': 'Миками',
    '松本': 'Мацумото',
    '上田': 'Камида',
    '小松': 'Коматцу',
    '小池': 'Коикэ',
    '松下': 'Мацусита',
    '木下': 'Киносита',
        '出水': 'Идзуми',
    '会田': 'Аида',
    '見上': 'Мигами',
    '小見山': 'Комияма',
    '朝日': 'Асахи',
    '入山': 'Ирияма',
    '飯山': 'Иияма',
    '三好': 'Миёси',
    '物部': 'Монобэ',
        '山名': 'Ямана',
    '半田': 'Ханда',
    '多田': 'Тада',
    '多木': 'Таки',
    '多門': 'Тамон',
    '名高': 'Надака',
        '大花': 'Оохана',
    '大鳥': 'Оотори',
    '大野': 'Ооно',
    '山野': 'Ямано',
    '今園': 'Имазоно',
    '水野': 'Мидзуно',
    '小野': 'Оно',
    '安田': 'Ясуда',
    '安池': 'Ясуике',
    '花園': 'Ханазоно',
    '野上': 'Ногами',
    '野部': 'Нобе',
    '鳥屋': 'Торияa',
    '立野': 'Татэно',
    '白鳥': 'Сиратори',
    '小園': 'Кодзоно',
    '国松': 'Куниматцу',
    '中黒': 'Накагуро',
    '目黒': 'Мэгуро',
    '服部': 'Хаттори',
    '和田': 'Вада',
    '広田': 'Хирота',
    '田口': 'Тагути',
    '川上': 'Каваками',
    '天川': 'Амакава',
    '天本': 'Амамото',
    '早川': 'Хаякава',
    '早出': 'Хаядэ',
    '早見': 'Хаями',
    '遠山': 'Тояма',
    '小川': 'Огава',
    '室口': 'Мурогути',
    '寺田': 'Тэрада',
    '平田': 'Хирата',
    '寒川': 'Самукава',
    '足立': 'Адати',
    '熱田': 'Ацута',
    '房野': 'Фусано'
        }

names_hir = {'大田':'おおだ', '本山':'もとやま','三田': 'きだ','山本': 'やまもと','室木':'むろき','山部':'やまべ',
                 '大友': 'おおとも',
    '友部': 'ともべ',
    '大高': 'おおたか',
    '小山': 'こやま',
    '小室': 'こむろ',
    '近田': 'ちかだ',
    '高木': 'たかぎ',
    '新山': 'にいやま',
    '大月': 'おおつき',
    '高月': 'たかつき',
    '百田': 'ももた',
    '白山': 'はくやま',
    '明本': 'あきもと',
        '前山': 'まえやま',
    '前田': 'まえだ',
    '金田': 'かねだ',
    '堂本': 'どうもと',
    '白金': 'しろかね',
    '時田': 'ときた',
    '大前': 'おおまえ',
    '金木': 'かねき',
    '時山': 'ときやま',
     '上山': 'かみやま',
    '今上': 'いまがみ',
    '松田': 'まつだ',
    '高松': 'たかまつ',
    '宅前': 'たくまえ',
    '池上': 'いけがみ',
    '田所': 'たどころ',
    '水上': 'みずかみ',
    '近松': 'ちかまつ',
    '大下': 'おおした',
    '山下': 'やました',
    '三上': 'みかみ',
    '松本': 'まつもと',
    '上田': 'かみだ',
    '小松': 'こまつ',
    '小池': 'こいけ',
    '松下': 'まつした',
    '木下': 'きのした',
        '出水': 'いずみ',
    '会田': 'あいだ',
    '見上': 'みがみ',
    '小見山': 'こみやま',
    '朝日': 'あさひ',
    '入山': 'いりやま',
    '飯山': 'いいやま',
    '三好': 'みよし',
    '物部': 'ものべ',
        '山名': 'やまな',
    '半田': 'はんだ',
    '多田': 'ただ',
    '多木': 'たき',
    '多門': 'たもん',
    '名高': 'なだか',
        '大花': 'おおはな',
    '大鳥': 'おおとり',
    '大野': 'おおの',
    '山野': 'やまの',
    '今園': 'いまぞの',
    '水野': 'みずの',
    '小野': 'おの',
    '安田': 'やすだ',
    '安池': 'やすいけ',
    '花園': 'はなぞの',
    '野上': 'のがみ',
    '野部': 'のべ',
    '鳥屋': 'とりや',
    '立野': 'たての',
    '白鳥': 'しらとり',
    '小園': 'こぞの',
    '国松': 'くにまつ',
    '中黒': 'なかぐろ',
    '目黒': 'めぐろ',
    '服部': 'はっとり',
    '和田': 'わだ',
    '広田': 'ひろた',
    '田口': 'たぐち',
    '川上': 'かわかみ',
    '天川': 'あまかわ',
    '天本': 'あまもと',
    '早川': 'はやかわ',
    '早出': 'はやで',
    '早見': 'はやみ',
    '遠山': 'とおやま',
    '小川': 'おがわ',
    '室口': 'むろぐち',
    '寺田': 'てらだ',
    '平田': 'ひらた',
    '寒川': 'さむかわ',
    '足立': 'あだち',
    '熱田': 'あつた',
    '房野': 'ふさの',
    }

a = ['大友','友部','大高','小山','小室','近田','高木','新山','大月','高月','百田',
                '白山','明本']

def names_jap(i):
    jap =i
    hir = names_hir[jap]
    rus = names[jap]
    return jap,hir,rus
