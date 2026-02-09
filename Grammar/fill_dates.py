import random 
from Grammar.dictions_words import a

def ran(x):
    return random.choice(list(x.keys())) 

def lists_words_dates():
    sp = []
    for i in range(5):
        sp.append(date_year())
    for i in range(5):
        sp.append(date_year_wareki())
    for i in range(5):
        sp.append(date_month_day())
    return sp


def date_year():
    year = random.randint(1980, 2024)
    years = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '10': '十', '0': '〇'}
    year_jap = ''.join(years[digit] for digit in str(year))
     # Формирование написания года хираганой
    year_hir = ''
    year_str = str(year)
    # Тысячи
    if year_str[0] != '1':
        year_hir += a['numbers2'][year_str[0]]
    year_hir += 'せん'
    # Сотни
    if year_str[1] != '0':
        year_hir += a['numbers2'][year_str[1]] + 'ひゃく'
    # Десятки
    if year_str[2] != '0':
        if year_str[2] == '1':
            year_hir += 'じゅう'
        else:
            year_hir += a['numbers2'][year_str[2]] + 'じゅう'
    # Единицы
    if year_str[3] != '0':
        year_hir += a['numbers2'][year_str[3]]
    jap= year_jap+'年' 
    hir = year_hir + 'ねん' 
    rus =  str(year)+' год'
    return jap, hir, rus


# Эры японского летоисчисления (с 1930 года): 昭和 1926–1988, 平成 1989–2018, 令和 2019–
_ERA = {
    '昭和': ('しょうわ', 'Сёва', 1925),   # год эры = western_year - 1925
    '平成': ('へいせい', 'Хэйсэй', 1988),  # год эры = western_year - 1988
    '令和': ('れいわ', 'Рэйва', 2018),     # год эры = western_year - 2018
}
_years_kanji = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}


def _era_year_to_japanese(n):
    """Число 1–99 в кандзи и хирагане для года эры (например 5 → 五, ご)."""
    if n < 1 or n > 99:
        raise ValueError('год эры должен быть от 1 до 99')
    if n == 10:
        return '十', 'じゅう'
    if n < 10:
        return _years_kanji[str(n)], a['numbers2'][str(n)]
    tens, units = n // 10, n % 10
    if tens == 1:
        kanji = '十' + (_years_kanji[str(units)] if units > 0 else '')
        hir = 'じゅう' + (a['numbers2'][str(units)] if units > 0 else '')
    else:
        kanji = _years_kanji[str(tens)] + '十' + (_years_kanji[str(units)] if units > 0 else '')
        hir = a['numbers2'][str(tens)] + 'じゅう' + (a['numbers2'][str(units)] if units > 0 else '')
    return kanji, hir


def date_year_wareki():
    """
    Случайный год по японскому летоисчислению (начиная с 1930).
    Возвращает (кандзи + 年, хирагана + ねん, русский: «N год эры Хэйсэй» и т.п.).
    """
    year = random.randint(1930, 2024)
    era_kanji, (era_hir, era_rus) = None, (None, None)
    for name, (reading, rus_name, offset) in _ERA.items():
        if year > offset and (era_kanji is None or offset > _ERA[era_kanji][2]):
            era_kanji = name
            era_hir, era_rus = reading, rus_name
    if era_kanji is None:
        era_kanji = '昭和'
        era_hir, era_rus = _ERA['昭和'][0], _ERA['昭和'][1]
    offset = _ERA[era_kanji][2]
    era_year_num = year - offset
    year_kanji, year_hir = _era_year_to_japanese(era_year_num)
    jap = era_kanji + year_kanji + '年'
    hir = era_hir + year_hir + 'ねん'
    rus = f'{year} год ({era_year_num}-й год эры {era_rus})'
    return jap, hir, rus


# Максимальное число дней в месяце (февраль без високосного)
_DAYS_IN_MONTH = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

nums = { 
    '月':{
        'read':{'1':'いちがつ','2':'にがつ','3':'さんがつ','4':'よんがつ','5':'ごがつ','6':'ろくがつ','7':'しちがつ','8':'はちがつ','9':'くがつ','10':'じゅうがつ','11':'じゅういちがつ','12':'じゅうにがつ'},
        'ending':{'1':'января', '2':'февраля', '3':'марта', '4':'апреля', '5':'мая', '6':'июня', '7':'июля', '8':'августа', '9':'сентября', '10':'октября', '11':'ноября', '12':'декабря'}, },
    '日':{
        'read':{'1':'ついたち','2':'ふつか','3':'みっか','4':'よっか','5':'いつか','6':'むいか','7':'なのか','8':'ようか','9':'ここのか','10':'とおか','11':'じゅういちにち','12':'じゅうににち','13':'じゅうさんにち','14':'じゅうよっか','15':'じゅうごにち','16':'じゅうろくにち','17':'じゅうしちにち','18':'じゅうはちにち','19':'じゅうくにち','20':'はつか','21':'にじゅういちにち','22':'にじゅうににち','23':'にじゅうさんにち','24':'にじゅうよっか','25':'にじゅうごにち','26':'にじゅうろくにち','27':'にじゅうしちにち','28':'にじゅうはちにち','29':'にじゅうくにち','30':'さんじゅうにち','31':'さんじゅういちにち'},
        'ending2':{'1':'первое', '2':'второе', '3':'третье', '4':'четвертое', '5':'пятое', '6':'шестое', '7':'седьмое', '8':'восьмое', '9':'девятое', '10':'десятое', '11':'одиннадцатое', '12':'двенадцатое', '13':'тринадцатое', '14':'четырнадцатое', '15':'пятнадцатое', '16':'шестнадцатое', '17':'семнадцатое', '18':'восемнадцатое', '19':'девятнадцатое', '20':'двадцатое', '21':'двадцать первое', '22':'двадцать второе', '23':'двадцать третье', '24':'двадцать четвертое', '25':'двадцать пятое', '26':'двадцать шестое', '27':'двадцать седьмое', '28':'двадцать восьмое', '29':'двадцать девятое', '30':'тридцатое', '31':'тридцать первое'}, },
    }


def date_month_day():
    """
    Случайная дата: месяц + день в формате 1月2日.
    Возвращает (кандзи 月/日, хирагана чтение, русский: «15 марта»).
    """
    month = random.randint(1, 12)
    day = random.randint(1, _DAYS_IN_MONTH[month])
    month_s, day_s = str(month), str(day)
    jap = f'{month}月{day}日'
    hir = nums['月']['read'][month_s] + nums['日']['read'][day_s]
    rus = f'{day} {nums["月"]["ending"][month_s]}'
    return jap, hir, rus