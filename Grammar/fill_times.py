import random 

def ran(x):
    return random.choice(list(x.keys())) 

def lists_words_times():
    sp = []
    sp.append(one())
    sp.append(one_variant())
    sp.append(two())
    sp.append(took_time_to_finish())
    sp.append(finished_reading_time_ago())
    sp.append(already_reading_for_duration())
    sp.append(started_years_ago_and_still())
    sp.append(will_start_reading_soon())
    sp.append(will_start_reading_at_time())
    sp.append(reading_since_time())
    sp.append(used_to_read_often())
    sp.append(frequency_per_week())
    sp.append(while_reading_simultaneous())
    sp.append(noun_no_toki())
    sp.append(during_period())
    sp.append(before_reading())
    sp.append(after_reading())
    sp.append(time_of_day_duration())
    sp.append(still_reading())
    sp.append(no_longer_reading())
    sp.append(usually_reading())
    sp.append(reading_time_of_day_habit())
    sp.append(always_never_reading())
    sp.append(as_soon_as_reading())
    sp.append(since_reading())
    sp.append(until_reading())
    sp.append(immediately_after_reading())
    sp.append(will_have_time_to_read())
    sp.append(toki_movement_dict_main_dict())
    sp.append(toki_movement_dict_main_dict_habit())
    sp.append(toki_movement_past_main_past())
    sp.append(toki_movement_dict_main_past())
    sp.append(toki_movement_past_main_dict())
    return sp

# словарь для дней недели
days_of_week = {
    '日曜日': 'воскресенье',
    '月曜日': 'понедельник',
    '火曜日': 'вторник',
    '水曜日': 'среду',
    '木曜日': 'четверг',
    '金曜日': 'пятницу',
    '土曜日': 'субботу',
}

days_of_week_2 = {
    '日曜日': 'воскресеньям',
    '月曜日': 'понедельникам',
    '火曜日': 'вторникам',
    '水曜日': 'средам',
    '木曜日': 'четвергам',
    '金曜日': 'пятницам',
    '土曜日': 'субботам',
}
days_of_week_hir = {
    '日曜日': 'にちようび',
    '月曜日': 'げつようび',
    '火曜日': 'かようび',
    '水曜日': 'すいようび',
    '木曜日': 'もくようび',
    '金曜日': 'きんようび',
    '土曜日': 'どようび',
}

# словарь для времени (часы)
hours = {
    '１時': {'hir': 'いちじ', 'ru_v': '1 час', 'ru_s': '1 часа'},
    '２時': {'hir': 'にじ', 'ru_v': '2 часа', 'ru_s': '2 часов'},
    '３時': {'hir': 'さんじ', 'ru_v': '3 часа', 'ru_s': '3 часов'},
    '４時': {'hir': 'よじ', 'ru_v': '4 часа', 'ru_s': '4 часов'},
    '５時': {'hir': 'ごじ', 'ru_v': '5 часов', 'ru_s': '5 часов'},
    '６時': {'hir': 'ろくじ', 'ru_v': '6 часов', 'ru_s': '6 часов'},
    '７時': {'hir': 'しちじ', 'ru_v': '7 часов', 'ru_s': '7 часов'},
    '８時': {'hir': 'はちじ', 'ru_v': '8 часов', 'ru_s': '8 часов'},
    '９時': {'hir': 'くじ', 'ru_v': '9 часов', 'ru_s': '9 часов'},
    '１０時': {'hir': 'じゅうじ', 'ru_v': '10 часов', 'ru_s': '10 часов'},
    '１１時': {'hir': 'じゅういちじ', 'ru_v': '11 часов', 'ru_s': '11 часов'},
    '１２時': {'hir': 'じゅうにじ', 'ru_v': '12 часов', 'ru_s': '12 часов'},
}

# часы с уточнением "дня/вечера" (午後)
hours_pm = {
    '午後１時': {'hir': 'ごごいちじ', 'ru_v': '1 час дня', 'ru_s': '1 часа дня'},
    '午後２時': {'hir': 'ごごにじ', 'ru_v': '2 часа дня', 'ru_s': '2 часов дня'},
    '午後３時': {'hir': 'ごごさんじ', 'ru_v': '3 часа дня', 'ru_s': '3 часов дня'},
    '午後４時': {'hir': 'ごごよじ', 'ru_v': '4 часа дня', 'ru_s': '4 часов дня'},
    '午後５時': {'hir': 'ごごごじ', 'ru_v': '5 часов дня', 'ru_s': '5 часов дня'},
    '午後６時': {'hir': 'ごごろくじ', 'ru_v': '6 часов дня', 'ru_s': '6 часов дня'},
    '午後７時': {'hir': 'ごごしちじ', 'ru_v': '7 часов вечера', 'ru_s': '7 часов вечера'},
    '午後８時': {'hir': 'ごごはちじ', 'ru_v': '8 часов вечера', 'ru_s': '8 часов вечера'},
    '午後９時': {'hir': 'ごごくじ', 'ru_v': '9 часов вечера', 'ru_s': '9 часов вечера'},
}

# словарь для длительности (сколько минут/часов)
durations = {
    '１５分': {'hir': 'じゅうごふん', 'ru': '15 минут'},
    '３０分': {'hir': 'さんじゅっぷん', 'ru': '30 минут'},
    '１時間': {'hir': 'いちじかん', 'ru': '1 час'},
    '２時間': {'hir': 'にじかん', 'ru': '2 часа'},
    '３時間': {'hir': 'さんじかん', 'ru': '3 часа'},
    '４時間': {'hir': 'よじかん', 'ru': '4 часа'},
}

# "X лет назад" (старт в прошлом; сейчас продолжается)
years_ago = {
    '１年前': {'hir': 'いちねんまえ', 'ru': '1 год назад'},
    '２年前': {'hir': 'にねんまえ', 'ru': '2 года назад'},
    '３年前': {'hir': 'さんねんまえ', 'ru': '3 года назад'},
    '４年前': {'hir': 'よねんまえ', 'ru': '4 года назад'},
    '５年前': {'hir': 'ごねんまえ', 'ru': '5 лет назад'},
    '６年前': {'hir': 'ろくねんまえ', 'ru': '6 лет назад'},
    '７年前': {'hir': 'しちねんまえ', 'ru': '7 лет назад'},
    '８年前': {'hir': 'はちねんまえ', 'ru': '8 лет назад'},
    '９年前': {'hir': 'きゅうねんまえ', 'ru': '9 лет назад'},
    '１０年前': {'hir': 'じゅうねんまえ', 'ru': '10 лет назад'},
}

# словарь для частоты (сколько раз)
frequency_times = {
    '１回': {'hir': 'いっかい', 'ru': '1 раз'},
    '２回': {'hir': 'にかい', 'ru': '2 раза'},
    '３回': {'hir': 'さんかい', 'ru': '3 раза'},
    '４回': {'hir': 'よんかい', 'ru': '4 раза'},
    '５回': {'hir': 'ごかい', 'ru': '5 раз'},
}

# словарь для периодов (в неделю, в месяц)
periods = {
    '週': {'hir': 'しゅう', 'ru': 'неделю'},
    '月': {'hir': 'つき', 'ru': 'месяц'},
}

# словарь для периодов времени (каникулы, отпуск и т.д.)
time_periods = {
    '休み': {'hir': 'やすみ', 'ru': 'каникул'},
    '夏休み': {'hir': 'なつやすみ', 'ru': 'летних каникул'},
    '冬休み': {'hir': 'ふゆやすみ', 'ru': 'зимних каникул'},
    '春休み': {'hir': 'はるやすみ', 'ru': 'весенних каникул'},
}

# ситуации/события (существительные) для конструкции Nの時(に)
# Пример: 旅行の時(に)、本を読みます。= "когда я в поездке / во время поездки читаю книгу"
situations_no_toki = {
    '旅行': {'hir': 'りょこう', 'ru': 'в поездке/в путешествии'},
    '休み': {'hir': 'やすみ', 'ru': 'на каникулах/в отпуске'},
    '試験': {'hir': 'しけん', 'ru': 'во время экзамена'},
    '仕事': {'hir': 'しごと', 'ru': 'на работе'},
}

# словарь для времени суток (без конкретного времени, без падежа)
time_of_day = {
    '朝': {'hir': 'あさ', 'ru': 'утром'},
    '昼': {'hir': 'ひる', 'ru': 'днем'},
    '夕方': {'hir': 'ゆうがた', 'ru': 'вечером'},
    '夜': {'hir': 'よる', 'ru': 'ночью'},
}

# Русские формы именно для "по утрам/по вечерам/по ночам"
time_of_day_habit_ru = {
    '朝': 'по утрам',
    '夕方': 'по вечерам',
    '夜': 'по ночам',
    '昼': 'днем',
}

# словарь для длительности (долго/мало)
duration_long_short = {
    '長い間': {'hir': 'ながいあいだ', 'ru': 'долго'},
    '少し': {'hir': 'すこし', 'ru': 'мало'},
    '短い間': {'hir': 'みじかいあいだ', 'ru': 'недолго'},
}

# 時 с глаголами движения: придаточное (движение) + главное (действие)
# Форма глагола перед 時 и в главном предложении задаёт смысл (до/после, будущее/прошлое)
movement_toki = {
    '日本へ行く': {'hir_dict': 'にほんへいく', 'hir_past': 'にほんへいった', 'ru': 'в Японию'},
    '駅へ行く': {'hir_dict': 'えきへいく', 'hir_past': 'えきへいった', 'ru': 'на станцию'},
    '家に帰る': {'hir_dict': 'いえにかえる', 'hir_past': 'いえにかえった', 'ru': 'домой'},
    '学校へ行く': {'hir_dict': 'がっこうへいく', 'hir_past': 'がっこうへいった', 'ru': 'в школу'},
}
main_action_toki = {
    '本を買う': {'hir_dict': 'ほんをかう', 'hir_past': 'ほんをかった', 'hir_masu': 'ほんをかいます', 'hir_neg': 'ほんをかいません', 'ru_pres': 'покупаю книгу', 'ru_past': 'купил книгу', 'ru_neg': 'не покупаю книгу'},
    '本を読む': {'hir_dict': 'ほんをよむ', 'hir_past': 'ほんをよんだ', 'hir_masu': 'ほんをよみます', 'hir_neg': 'ほんをよみません', 'ru_pres': 'читаю книгу', 'ru_past': 'прочитал книгу', 'ru_neg': 'не читаю книгу'},
    '写真を撮る': {'hir_dict': 'しゃしんをとる', 'hir_past': 'しゃしんをとった', 'hir_masu': 'しゃしんをとります', 'hir_neg': 'しゃしんをとりません', 'ru_pres': 'делаю фото', 'ru_past': 'сделал фото', 'ru_neg': 'не делаю фото'},
}
# Маркер будущего для намерения: "в следующий раз когда поеду..."
toki_future_marker = {
    '今度': {'hir': 'こんど', 'ru': 'в следующий раз'},
    '次': {'hir': 'つぎ', 'ru': 'в следующий раз'},
}
# Наречия для привычки (обычно, часто, иногда, редко)
toki_habit_adverb = {
    'よく': {'hir': 'よく', 'ru': 'часто'},
    '時々': {'hir': 'ときどき', 'ru': 'иногда'},
    'いつも': {'hir': 'いつも', 'ru': 'всегда'},
}


def one():
    # Регулярность: "по понедельникам" / "каждый понедельник"
    day_of_week = ran(days_of_week_2)
    day_of_week_hir = days_of_week_hir[day_of_week]
    jap = '私は' + day_of_week + 'は本を読みます。'
    hir = 'わたしは' + day_of_week_hir + 'はほんをよみます。'
    rus = ' '.join(['по', days_of_week_2[day_of_week], 'я', 'читаю', 'книгу', '(регулярно)'])

    return jap, hir, rus, one.__name__


def one_variant():
    # Регулярность (явно): "каждую неделю по понедельникам"
    day_of_week = ran(days_of_week_2)
    day_of_week_hir = days_of_week_hir[day_of_week]
    jap = '私は毎週' + day_of_week + 'に本を読みます。'
    hir = 'わたしはまいしゅう' + day_of_week_hir + 'にほんをよみます。'
    rus = ' '.join(['каждую неделю', 'по', days_of_week_2[day_of_week], 'я', 'читаю', 'книгу', '(регулярно)'])

    return jap, hir, rus, one_variant.__name__


def two():
    # Конкретный (ближайший/следующий) день недели
    # `今度の + 曜日 + に` = "в следующий (ближайший) понедельник"
    day_of_week = ran(days_of_week)  # тут days_of_week: 月曜日 -> "понедельник"
    day_of_week_hir = days_of_week_hir[day_of_week]
    day_ru = days_of_week[day_of_week]
    if random.randint(0, 1) == 1:
        goro_jap, goro_hir, goro_ru = 'ごろ', 'ごろ', 'около '
        day_ru = goro_ru + day_ru
    else:
        goro_jap, goro_hir = '', ''
    jap = '私は今度の' + day_of_week + goro_jap + 'に本を読みます。'
    hir = 'わたしはこんどの' + day_of_week_hir + goro_hir + 'にほんをよみます。'
    rus = ' '.join(['в следующий', day_ru, 'я', 'буду читать', 'книгу'])

    return jap, hir, rus, two.__name__


def took_time_to_finish():
    # Сколько времени занимает/занял процесс (сколько потребовалось): "прочитал(а) за полчаса"
    dur = ran(durations)
    dur_hir = durations[dur]['hir']
    dur_ru = durations[dur]['ru']
    if random.randint(0, 1) == 1:
        gurai_jap, gurai_hir, gurai_ru = 'ぐらい', 'ぐらい', 'примерно '
        dur_ru = gurai_ru + dur_ru
    else:
        gurai_jap, gurai_hir = '', ''
    jap = [dur, gurai_jap, 'で', '私', 'は', '本', 'を', '読みました', '。']
    hir = ''.join([dur_hir, gurai_hir, 'で', 'わたし', 'は', 'ほん', 'を', 'よみました', '。'])
    rus = ' '.join(['я', 'прочитал(а)', 'книгу', 'за', dur_ru, '(сколько заняло времени)'])
    jap = ''.join(jap)
    return jap, hir, rus, took_time_to_finish.__name__


def finished_reading_time_ago():
    # "3 часа назад закончила читать"
    # Это НЕ `読む前に` (перед тем как), а "X времени назад" = `X時間前(に)`
    dur = ran(durations)
    dur_hir = durations[dur]['hir']
    dur_ru = durations[dur]['ru']

    use_ni = random.randint(0, 1) == 0
    mae = '前に' if use_ni else '前'
    mae_hir = 'まえに' if use_ni else 'まえ'

    if random.randint(0, 1) == 1:
        gurai_jap, gurai_hir, gurai_ru = 'ぐらい', 'ぐらい', 'примерно '
        dur_ru = gurai_ru + dur_ru
    else:
        gurai_jap, gurai_hir = '', ''

    jap = ''.join([dur, gurai_jap, mae, '私', 'は', '本', 'を', '読み終えました', '。'])
    hir = ''.join([dur_hir, gurai_hir, mae_hir, 'わたし', 'は', 'ほん', 'を', 'よみあえました', '。'])
    rus = ' '.join([dur_ru, 'назад', 'я', 'закончила', 'читать', 'книгу', '(завершение в прошлом)'])
    return jap, hir, rus, finished_reading_time_ago.__name__


def already_reading_for_duration():
    # Сколько уже длится процесс: "3 часа читаю"
    dur = ran(durations)
    dur_hir = durations[dur]['hir']
    dur_ru = durations[dur]['ru']
    if random.randint(0, 1) == 1:
        gurai_jap, gurai_hir, gurai_ru = 'ぐらい', 'ぐらい', 'примерно '
        dur_ru = gurai_ru + dur_ru
    else:
        gurai_jap, gurai_hir = '', ''
    jap = ['もう', dur, gurai_jap, '本', 'を', '読んでいます', '。']
    hir = ''.join(['もう', dur_hir, gurai_hir, 'ほん', 'を', 'よんでいます', '。'])
    rus = ' '.join(['я', 'читаю', 'уже', dur_ru, '(сколько длится)'])
    jap = ''.join(jap)
    return jap, hir, rus, already_reading_for_duration.__name__


def started_years_ago_and_still():
    # "3 года назад начала читать" (факт начала в прошлом; без "до сих пор")
    # Шаблон: X年前に V始めました
    y = ran(years_ago)
    y_hir = years_ago[y]['hir']
    y_ru = years_ago[y]['ru']
    jap = ''.join([y, 'に', '本', 'を', '読み始めました', '。'])
    hir = ''.join([y_hir, 'に', 'ほん', 'を', 'よみはじめました', '。'])
    rus = ' '.join([y_ru, 'я', 'начала', 'читать', 'книгу', '(начало в прошлом)'])
    return jap, hir, rus, started_years_ago_and_still.__name__

def will_start_reading_soon():
    # "В ближайшее время/скоро начну читать"
    # Типовые маркеры: もうすぐ (скоро), まもなく (вскоре), 近いうちに (в ближайшее время)
    markers = [
        ('もうすぐ', 'もうすぐ', 'скоро'),
        ('まもなく', 'まもなく', 'вскоре'),
        ('近いうちに', 'ちかいうちに', 'в ближайшее время'),
    ]
    m_jap, m_hir, m_ru = random.choice(markers)

    jap = ''.join([m_jap, '私', 'は', '本', 'を', '読み始めます', '。'])
    hir = ''.join([m_hir, 'わたし', 'は', 'ほん', 'を', 'よみはじめます', '。'])
    rus = ' '.join(['я', m_ru, 'начну', 'читать', 'книгу', '(скоро/в ближайшее время)'])
    return jap, hir, rus, will_start_reading_soon.__name__

def will_start_reading_at_time():
    # Начну читать в 3 часа (конкретное время начала)
    t = ran(hours)
    t_hir = hours[t]['hir']
    t_ru_v = hours[t]['ru_v']
    if random.randint(0, 1) == 1:
        goro_jap, goro_hir, goro_ru = 'ごろ', 'ごろ', 'около '
        t_ru_v = goro_ru + t_ru_v
    else:
        goro_jap, goro_hir = '', ''
    jap = [t, goro_jap, 'に', '私', 'は', '本', 'を', '読み始めます', '。']
    hir = ''.join([t_hir, goro_hir, 'に', 'わたし', 'は', 'ほん', 'を', 'よみはじめます', '。'])
    rus = ' '.join(['я', 'начну', 'читать', 'в', t_ru_v, '(время начала)'])
    jap = ''.join(jap)
    return jap, hir, rus, will_start_reading_at_time.__name__

def reading_since_time():
    # С какого времени уже читаю: "с 3 часов дня читаю"
    t = ran(hours_pm)
    t_hir = hours_pm[t]['hir']
    t_ru_s = hours_pm[t]['ru_s']
    if random.randint(0, 1) == 1:
        goro_jap, goro_hir, goro_ru = 'ごろ', 'ごろ', 'около '
        t_ru_s = goro_ru + t_ru_s
    else:
        goro_jap, goro_hir = '', ''
    jap = [t, goro_jap, 'から', '本', 'を', '読んでいます', '。']
    hir = ''.join([t_hir, goro_hir, 'から', 'ほん', 'を', 'よんでいます', '。'])
    rus = ' '.join(['я', 'читаю', 'с', t_ru_s, '(с какого времени)'])
    jap = ''.join(jap)
    return jap, hir, rus, reading_since_time.__name__

def used_to_read_often():
    # Раньше я читала часто: "以前はよく本を読みました"
    jap = ['前は', 'よく', '私', 'は', '本', 'を', '読みました', '。']
    hir = ''.join(['まえは', 'よく', 'わたし', 'は', 'ほん', 'を', 'よみました', '。'])
    rus = ' '.join(['раньше', 'я', 'часто', 'читала', 'книгу', '(прошлое + частота)'])
    jap = ''.join(jap)
    return jap, hir, rus, used_to_read_often.__name__

def frequency_per_week():
    # Я читаю 3 раза в неделю: "週に３回本を読みます"
    freq = ran(frequency_times)
    freq_hir = frequency_times[freq]['hir']
    freq_ru = frequency_times[freq]['ru']
    period = ran(periods)
    period_hir = periods[period]['hir']
    period_ru = periods[period]['ru']
    jap = [period, 'に', freq, '本', 'を', '読みます', '。']
    hir = ''.join([period_hir, 'に', freq_hir, 'ほん', 'を', 'よみます', '。'])
    rus = ' '.join(['я', 'читаю', freq_ru, 'в', period_ru, '(частота в период)'])
    jap = ''.join(jap)
    return jap, hir, rus, frequency_per_week.__name__               

def while_reading_simultaneous():
    # Во время чтения я слушаю музыку: "本を読んでいる時、音楽を聞きます" или "本を読みながら、音楽を聞きます"
    rand = random.randint(0, 1)
    if rand == 0:
        # Вариант с ～ている時
        jap = ['本', 'を', '読んでいる時、', '私', 'は', '音楽', 'を', '聞きます', '。']
        hir = ''.join(['ほん', 'を', 'よんでいるとき、', 'わたし', 'は', 'おんがく', 'を', 'ききます', '。'])
        rus = ' '.join(['во время чтения', 'я', 'слушаю', 'музыку', '(когда/во время того как)'])
    else:
        # Вариант с ながら
        jap = ['本', 'を', '読みながら、', '私', 'は', '音楽', 'を', '聞きます', '。']
        hir = ''.join(['ほん', 'を', 'よみながら、', 'わたし', 'は', 'おんがく', 'を', 'ききます', '。'])
        rus = ' '.join(['читая книгу', 'я', 'слушаю', 'музыку', '(одновременность действия)'])
    jap = ''.join(jap)
    return jap, hir, rus, while_reading_simultaneous.__name__

def noun_no_toki():
    # Вариант "ситуация/событие (существительное) + の時(に)": 旅行の時(に)...
    # `に` тут НЕ обязательно: и `Nの時、...`, и `Nの時に、...` нормальные.
    # Чуть грубо: `...時に` чаще звучит как "в тот момент/когда наступает время", `...時` — более нейтрально.
    n = ran(situations_no_toki)
    n_hir = situations_no_toki[n]['hir']
    n_ru = situations_no_toki[n]['ru']
    use_ni = random.randint(0, 1) == 0
    toki = 'の時に、' if use_ni else 'の時、'
    toki_hir = 'のときに、' if use_ni else 'のとき、'

    jap = ''.join([n, toki, '私', 'は', '本', 'を', '読みます', '。'])
    hir = ''.join([n_hir, toki_hir, 'わたし', 'は', 'ほん', 'を', 'よみます', '。'])
    # Русская подсказка — по смыслу (без спойлера про частицу/конструкцию)
    rus = ' '.join([n_ru + ',', 'я', 'читаю', 'книгу', '(когда/в ситуации. не обязательно ВЕСЬ период)'])
    return jap, hir, rus, noun_no_toki.__name__

def during_period():
    # Во время каникул буду читать: "休みの間、本を読みます" (～の間 - для периодов)
    period = ran(time_periods)
    period_hir = time_periods[period]['hir']
    period_ru = time_periods[period]['ru']
    period = period + 'の間'
    period_hir = period_hir + 'のあいだ'
    jap = [period, '私', 'は', '本', 'を', '読みます', '。']
    hir = ''.join([period_hir,  'わたし', 'は', 'ほん', 'を', 'よみます', '。'])
    rus = ' '.join(['во время', period_ru, 'я', 'буду читать', 'книгу', '(в течение всего периода)'])
    jap = ''.join(jap)
    return jap, hir, rus, during_period.__name__

def before_reading():
    # До того как начать читать: "本を読む前に、音楽を聞きます"
    jap = ['本', 'を', '読む前に、', '私', 'は', '音楽', 'を', '聞きます', '。']
    hir = ''.join(['ほん', 'を', 'よむまえに、', 'わたし', 'は', 'おんがく', 'を', 'ききます', '。'])
    rus = ' '.join(['до того как начать читать', 'я', 'слушаю', 'музыку'])
    jap = ''.join(jap)
    return jap, hir, rus, before_reading.__name__

def after_reading():
    # После того как прочитал: "本を読んだ後で、音楽を聞きます"
    jap = ['本', 'を', '読んだ後で、', '私', 'は', '音楽', 'を', '聞きます', '。']
    hir = ''.join(['ほん', 'を', 'よんだあとで、', 'わたし', 'は', 'おんがく', 'を', 'ききます', '。'])
    rus = ' '.join(['после того как прочитал', 'я', 'слушаю', 'музыку'])
    jap = ''.join(jap)
    return jap, hir, rus, after_reading.__name__

def time_of_day_duration():
    # Утром я читала долго/мало: "朝、長い間本を読みました" (без падежа, так как нет конкретного времени)
    time = ran(time_of_day)
    time_hir = time_of_day[time]['hir']
    time_ru = time_of_day[time]['ru']
    dur = ran(duration_long_short)
    dur_hir = duration_long_short[dur]['hir']
    dur_ru = duration_long_short[dur]['ru']
    jap = [time, '、', dur, '本', 'を', '読みました', '。']
    hir = ''.join([time_hir, '、', dur_hir, 'ほん', 'を', 'よみました', '。'])
    rus = ' '.join([time_ru, 'я', 'читала', dur_ru, 'книгу', '(время суток + длительность)'])
    jap = ''.join(jap)
    return jap, hir, rus, still_reading.__name__

def still_reading():
    # Все еще читаю: "まだ本を読んでいます"
    jap = ['まだ', '私', 'は', '本', 'を', '読んでいます', '。']
    hir = ''.join(['まだ', 'わたし', 'は', 'ほん', 'を', 'よんでいます', '。'])
    rus = ' '.join(['я', 'все еще', 'читаю', 'книгу'])
    jap = ''.join(jap)
    return jap, hir, rus, time_of_day_duration.__name__

def no_longer_reading():
    # Уже не читаю: "もう本を読みません"
    jap = ['もう', '私', 'は', '本', 'を', '読みません', '。']
    hir = ''.join(['もう', 'わたし', 'は', 'ほん', 'を', 'よみません', '。'])
    rus = ' '.join(['я', 'уже не', 'читаю', 'книгу'])
    jap = ''.join(jap)
    return jap, hir, rus, no_longer_reading.__name__

def usually_reading():
    # Обычно читаю утром: "普通は朝本を読みます"
    time = ran(time_of_day)
    time_hir = time_of_day[time]['hir']
    time_ru = time_of_day[time]['ru']
    jap = ['ふつうは', time, '本', 'を', '読みます', '。']
    hir = ''.join(['ふつうは', time_hir, 'ほん', 'を', 'よみます', '。'])
    rus = ' '.join(['обычно', time_ru, 'я', 'читаю', 'книгу'])
    jap = ''.join(jap)
    return jap, hir, rus, usually_reading.__name__

def reading_time_of_day_habit():
    # Регулярная привычка: "я по утрам (вечерам, ночам) читаю"
    # Естественный японский вариант для привычки: `朝は本を読みます` / `夜は本を読みます`
    time = ran(time_of_day)
    time_hir = time_of_day[time]['hir']
    time_ru = time_of_day_habit_ru.get(time, time_of_day[time]['ru'])

    jap = ''.join([time, 'は', '私', 'は', '本', 'を', '読みます', '。'])
    hir = ''.join([time_hir, 'は', 'わたし', 'は', 'ほん', 'を', 'よみます', '。'])
    rus = ' '.join([time_ru, 'я', 'читаю', 'книгу', '(привычка/регулярно)'])
    return jap, hir, rus, reading_time_of_day_habit.__name__


def always_never_reading():
    # Всегда/никогда читаю: "いつも本を読みます" / "決して本を読みません"
    jap = ['いつも', '私', 'は', '本', 'を', '読みます', '。']
    hir = ''.join(['いつも', 'わたし', 'は', 'ほん', 'を', 'よみます', '。'])
    rus = ' '.join(['я', 'всегда', 'читаю', 'книгу'])
    jap = ''.join(jap)
    return jap, hir, rus, always_never_reading.__name__

def will_have_time_to_read():
    # У меня будет время почитать книгу утром: "朝、本を読む時間があります"
    time = ran(time_of_day)
    time_hir = time_of_day[time]['hir']
    time_ru = time_of_day[time]['ru']
    jap = [time, '、', '本', 'を', '読む時間', 'が', 'あります', '。']
    hir = ''.join([time_hir, '、', 'ほん', 'を', 'よむじかん', 'が', 'あります', '。'])
    rus = ' '.join([time_ru, 'у меня будет время', 'почитать книгу'])
    jap = ''.join(jap)
    return jap, hir, rus

def as_soon_as_reading():
    # Как только прочитаю: "本を読むとすぐ、音楽を聞きます"
    jap = ['本', 'を', '読んだから、', '私', 'は', 'すぐ音楽', 'を', '聞きます', '。']
    hir = ''.join(['ほん', 'を', 'よんだから、', 'わたし', 'は', 'すぐおんがく', 'を', 'ききます', '。'])
    rus = ' '.join(['как только прочитаю', 'я', 'слушаю', 'музыку (после окончания первого процесса начну новый)'])
    jap = ''.join(jap)
    return jap, hir, rus, as_soon_as_reading.__name__

def since_reading():
    # С тех пор как начала читать: "本を読み始めてからずっと、音楽を聞いています"
    jap = ['本', 'を', '読み始めてからずっと、', '私', 'は', '音楽', 'を', '聞いています', '。']
    hir = ''.join(['ほん', 'を', 'よみはじめてからずっと、', 'わたし', 'は', 'おんがく', 'を', 'きいています', '。'])
    rus = ' '.join(['с тех пор как начала читать', 'я', 'слушаю', 'музыку (все это время)'])
    jap = ''.join(jap)
    return jap, hir, rus, since_reading.__name__

def until_reading():
    # До тех пор пока не прочитаю: "本を読むまで、音楽を聞きません"
    jap = ['本', 'を', '読むまで、', '私', 'は', '音楽', 'を', '聞きません', '。']
    hir = ''.join(['ほん', 'を', 'よむまで、', 'わたし', 'は', 'おんがく', 'を', 'ききません', '。'])
    rus = ' '.join(['до тех пор пока не прочитаю', 'я', 'не слушаю', 'музыку'])
    jap = ''.join(jap)
    return jap, hir, rus, until_reading.__name__

def immediately_after_reading():
    # Сразу после чтения: "本を読んだ後すぐ、音楽を聞きます"
    jap = ['本', 'を', '読んだ後、', 'すぐ音楽', 'を', '聞きます', '。']
    hir = ''.join(['ほん', 'を', 'よんだあと、', 'すぐおんがく', 'を', 'ききます', '。'])
    rus = ' '.join(['сразу после чтения', 'я', 'слушаю', 'музыку'])
    jap = ''.join(jap)
    return jap, hir, rus








# 時 с глаголами движения: разное время в придаточном и главном предложении
def toki_movement_dict_main_dict():
    # Намерение на будущее: "в следующий раз когда поеду — куплю". 今度/次 + 行く時 + 買う
    mov = ran(movement_toki)
    act = ran(main_action_toki)
    marker = ran(toki_future_marker)
    jap = marker + mov + '時、' + act + '。'
    hir = toki_future_marker[marker]['hir'] + movement_toki[mov]['hir_dict'] + 'とき、' + main_action_toki[act]['hir_dict'] + '。'
    rus = ' '.join([toki_future_marker[marker]['ru'], 'когда', 'поеду', movement_toki[mov]['ru'], ',', main_action_toki[act]['ru_pres'], '(намерение на будущее)'])
    return jap, hir, rus, toki_movement_dict_main_dict.__name__


def toki_movement_dict_main_dict_habit():
    # Привычка: "обычно/часто/иногда когда еду — покупаю". Наречие + 行く時 + 買います
    mov = ran(movement_toki)
    act = ran(main_action_toki)
    adv = ran(toki_habit_adverb)
    jap = adv + mov + '時、' + act.replace('買う', '買います').replace('読む', '読みます').replace('撮る', '撮ります') + '。'
    hir = toki_habit_adverb[adv]['hir'] + movement_toki[mov]['hir_dict'] + 'とき、' + main_action_toki[act]['hir_masu'] + '。'
    rus = ' '.join([toki_habit_adverb[adv]['ru'], 'когда', 'еду', movement_toki[mov]['ru'], ',', main_action_toki[act]['ru_pres'], '(привычка)'])
    return jap, hir, rus, toki_movement_dict_main_dict_habit.__name__


def toki_movement_past_main_past():
    # 日本へ行った時、本を買った。 — Когда приехал, купил книгу. (оба в прошлом)
    mov = ran(movement_toki)
    act = ran(main_action_toki)
    jap = mov.replace('行く', '行った').replace('帰る', '帰った') + '時、' + act.replace('買う', '買った').replace('読む', '読んだ').replace('撮る', '撮った') + '。'
    hir = movement_toki[mov]['hir_past'] + 'とき、' + main_action_toki[act]['hir_past'] + '。'
    rus = ' '.join(['когда', 'приехал', movement_toki[mov]['ru'], ',', main_action_toki[act]['ru_past'], '(сначала первое действие, потом второе)'])
    return jap, hir, rus, toki_movement_past_main_past.__name__


def toki_movement_dict_main_past():
    # 日本へ行く時、本を買った。 — Перед поездкой (уже) купил книгу. (до отъезда сделал действие в прошлом)
    mov = ran(movement_toki)
    act = ran(main_action_toki)
    jap = mov + '時、' + act.replace('買う', '買った').replace('読む', '読んだ').replace('撮る', '撮った') + '。'
    hir = movement_toki[mov]['hir_dict'] + 'とき、' + main_action_toki[act]['hir_past'] + '。'
    rus = ' '.join(['перед тем как поехать', movement_toki[mov]['ru'], ',', main_action_toki[act]['ru_past'], '(До первого действия уже сделал второе)'])
    return jap, hir, rus, toki_movement_dict_main_past.__name__


def toki_movement_past_main_dict():
    # 日本へ行った時、本を買う。 — Когда приеду (приехав), куплю книгу. (после приезда — будущее в главном)
    mov = ran(movement_toki)
    act = ran(main_action_toki)
    jap = mov.replace('行く', '行った').replace('帰る', '帰った') + '時、' + act + '。'
    hir = movement_toki[mov]['hir_past'] + 'とき、' + main_action_toki[act]['hir_dict'] + '。'
    rus = ' '.join(['когда', 'приезжаю', movement_toki[mov]['ru'], ',', main_action_toki[act]['ru_pres'], '(сначала первое действие, потом второе в качестве привычки)'])
    return jap, hir, rus, toki_movement_past_main_dict.__name__

