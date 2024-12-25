import random 

def ran(x):
    return random.choice(list(x.keys())) 

def lists_words_numbers():

    sp = []
    sp.append(ten())
    sp.append(nundred())
    sp.append(thousand())
    sp.append(man())
    return sp

a={}

def ten():
    
    numb_kanji = {0:'', 1:'一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六', 7:'七', 8:'八', 9:'九', 10:'十', 100:'百'}
    numb_hiragana = {0:'', 1:'いち', 2:'に', 3:'さん', 4:'よん', 5:'ご', 6:'ろく', 7:'しち', 8:'はち', 9:'きゅう', 10:'じゅう', 100:'ひゃく'}
    rand_numb = random.randint(11,100)
    kanji = ''
    if rand_numb == 100:
        kanji = '百'
    else:
        if rand_numb > 10:
            kanji += numb_kanji[rand_numb//10] + numb_kanji[10]
        kanji += numb_kanji[rand_numb%10]
    hir = ''
    if rand_numb == 100:
        hir = 'ひゃく'
    else:
        if rand_numb > 10:
            hir += numb_hiragana[rand_numb//10] + numb_hiragana[10]
        hir += numb_hiragana[rand_numb%10]
    return str(kanji),str(hir),str(rand_numb)

def nundred():
    numb_kanji = {0: '', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 100: '百', 1000: '千'}
    numb_hiragana = {0: '', 1: 'いち', 2: 'に', 3: 'さん', 4: 'よん', 5: 'ご', 6: 'ろく', 7: 'しち', 8: 'はち', 9: 'きゅう', 10: 'じゅう', 100: 'ひゃく', 1000: 'せん'}
    special_hiragana = {3: 'さんびゃく', 6: 'ろっぴゃく', 8: 'はっぴゃく'}
    rand_numb = random.randint(100, 1000)

    kanji = ''
    hundreds_digit = rand_numb // 100
    tens_and_ones = rand_numb % 100

    # Handling hundreds in Kanji and Hiragana
    if hundreds_digit in special_hiragana:
        kanji += numb_kanji[hundreds_digit] + numb_kanji[100]  # Use Kanji for special hundreds
        hiragana = special_hiragana[hundreds_digit]  # Use special Hiragana reading
    else:
        kanji += numb_kanji[hundreds_digit] + numb_kanji[100]
        hiragana = numb_hiragana[hundreds_digit] + numb_hiragana[100]

    # Handling tens and ones in Kanji and Hiragana
    if tens_and_ones >= 10:
        kanji += numb_kanji[tens_and_ones // 10] + numb_kanji[10]
        hiragana += numb_hiragana[tens_and_ones // 10] + numb_hiragana[10]
    kanji += numb_kanji[tens_and_ones % 10]
    hiragana += numb_hiragana[tens_and_ones % 10]

    return str(kanji),str(hiragana),str(rand_numb)

def thousand():
    numb_kanji = {0: '', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 100: '百', 1000: '千'}
    numb_hiragana = {0: '', 1: 'いち', 2: 'に', 3: 'さん', 4: 'よん', 5: 'ご', 6: 'ろく', 7: 'しち', 8: 'はち', 9: 'きゅう', 10: 'じゅう', 100: 'ひゃく', 1000: 'せん'}
    special_thousands_hiragana = {3: 'さんぜん', 8: 'はっせん'}
    
    rand_numb = random.randint(10, 100) * 100  # Generate a random number between 1000 and 10000, multiple of 100

    kanji = ''
    thousands_digit = rand_numb // 1000
    hundreds = rand_numb % 1000

    # Handling thousands in Kanji and Hiragana
    if thousands_digit in special_thousands_hiragana:
        kanji += numb_kanji[thousands_digit] + numb_kanji[1000]  # Use Kanji for special thousands
        hiragana = special_thousands_hiragana[thousands_digit]  # Use special Hiragana reading
    else:
        kanji += numb_kanji[thousands_digit] + numb_kanji[1000]
        hiragana = numb_hiragana[thousands_digit] + numb_hiragana[1000]

    # Handling hundreds in Kanji and Hiragana
    kanji += numb_kanji[hundreds // 100] + numb_kanji[100]
    hiragana += numb_hiragana[hundreds // 100] + numb_hiragana[100]

    return str(kanji),str(hiragana),str(rand_numb)

def man():
    numb_kanji = {0: '', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 100: '百', 1000: '千', 10000: '万'}
    numb_hiragana = {0: '', 1: 'いち', 2: 'に', 3: 'さん', 4: 'よん', 5: 'ご', 6: 'ろく', 7: 'しち', 8: 'はち', 9: 'きゅう', 10: 'じゅう', 100: 'ひゃく', 1000: 'せん', 10000: 'まん'}
    special_hiragana = {300: 'さんびゃく', 600: 'ろっぴゃく', 800: 'はっぴゃく', 3000: 'さんぜん', 8000: 'はっせん'}
    
    rand_numb = random.randint(100, 1000) * 100  # Generate a random number between 10,000 and 100,000, multiple of 100

    kanji = ''
    hiragana = ''

    # Split the number into man, thousands, and hundreds
    man = rand_numb // 10000
    remaining = rand_numb % 10000
    thousands = remaining // 1000
    hundreds = remaining % 1000

    # Handling "man" in Kanji and Hiragana
    kanji += numb_kanji[man] + numb_kanji[10000]
    hiragana += numb_hiragana[man] + numb_hiragana[10000]

    # Handling thousands
    if thousands * 1000 in special_hiragana:
        kanji += numb_kanji[thousands] + numb_kanji[1000]
        hiragana += special_hiragana[thousands * 1000]
    else:
        kanji += numb_kanji[thousands] + numb_kanji[1000]
        hiragana += numb_hiragana[thousands] + numb_hiragana[1000]

    # Handling hundreds
    if hundreds == 100:
        kanji += numb_kanji[100]
        hiragana += numb_hiragana[100]
    elif hundreds in special_hiragana:
        kanji += numb_kanji[hundreds // 100] + numb_kanji[100]
        hiragana += special_hiragana[hundreds]
    else:
        kanji += numb_kanji[hundreds // 100] + numb_kanji[100]
        hiragana += numb_hiragana[hundreds // 100] + numb_hiragana[100]

    return str(kanji),str(hiragana),str(rand_numb)

def ten_man():
    numb_kanji = {0: '', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 100: '百', 1000: '千', 10000: '万'}
    numb_hiragana = {0: '', 1: 'いち', 2: 'に', 3: 'さん', 4: 'よん', 5: 'ご', 6: 'ろく', 7: 'しち', 8: 'はち', 9: 'きゅう', 10: 'じゅう', 100: 'ひゃく', 1000: 'せん', 10000: 'まん'}
    special_thousands_hiragana = {3: 'さんぜん', 8: 'はっせん'}

    rand_numb = random.randint(100, 1000) * 1000  # Generate a random number between 100,000 and 1,000,000, multiple of 1000

    kanji = ''
    hiragana = ''

    # Split the number into ten-thousands and thousands
    ten_thousands = rand_numb // 10000
    thousands = (rand_numb % 10000) // 1000

    # Handling ten-thousands in Kanji and Hiragana
    if ten_thousands >= 10:
        kanji += numb_kanji[ten_thousands // 10] + numb_kanji[10]
        hiragana += numb_hiragana[ten_thousands // 10] + numb_hiragana[10]
    kanji += numb_kanji[ten_thousands % 10] + numb_kanji[10000]
    hiragana += numb_hiragana[ten_thousands % 10] + numb_hiragana[10000]

    # Handling thousands
    if thousands in special_thousands_hiragana:
        kanji += special_thousands_hiragana[thousands]
        hiragana += special_thousands_hiragana[thousands]
    elif thousands > 0:
        kanji += numb_kanji[thousands] + numb_kanji[1000]
        hiragana += numb_hiragana[thousands] + numb_hiragana[1000]

    return str(kanji),str(hiragana),str(rand_numb)

def multi_million():
    numb_kanji = {0: '', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 100: '百', 1000: '千', 10000: '万'}
    numb_hiragana = {0: '', 1: 'いち', 2: 'に', 3: 'さん', 4: 'よん', 5: 'ご', 6: 'ろく', 7: 'しち', 8: 'はち', 9: 'きゅう', 10: 'じゅう', 100: 'ひゃく', 1000: 'せん', 10000: 'まん'}

    rand_numb = random.randint(100, 1000)  # Generate a random number between 100 and 1000
    man = rand_numb  # This will be the number of man (10,000s)

    kanji = ''
    hiragana = ''

    # Handling man in Kanji and Hiragana
    # For each digit in the number
    for i, digit in enumerate(str(man)[::-1]):
        digit = int(digit)
        if digit != 0:
            if i == 0:
                kanji = numb_kanji[10000] + kanji
                hiragana = numb_hiragana[10000] + hiragana
            elif i == 1:
                kanji = numb_kanji[digit] + kanji
                hiragana = numb_hiragana[digit] + hiragana
            elif i == 2:
                kanji = numb_kanji[10] + numb_kanji[digit] + kanji
                hiragana = numb_hiragana[10] + numb_hiragana[digit] + hiragana
            elif i == 3:
                kanji = numb_kanji[digit] + numb_kanji[1000] + kanji
                hiragana = numb_hiragana[digit] + numb_hiragana[1000] + hiragana

    return kanji, hiragana, str(man * 10000)

def hundred_million():
    numb_kanji = {0: '', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 100: '百', 1000: '千', 10000: '万'}
    numb_hiragana = {0: '', 1: 'いち', 2: 'に', 3: 'さん', 4: 'よん', 5: 'ご', 6: 'ろく', 7: 'しち', 8: 'はち', 9: 'きゅう', 10: 'じゅう', 100: 'ひゃく', 1000: 'せん', 10000: 'まん'}

    rand_numb = random.randint(1000, 10000)  # Generate a random number between 1,000 and 10,000
    man = rand_numb  # This will be the number of man (10,000s)

    kanji = ''
    hiragana = ''

    # Handling man in Kanji and Hiragana
    # For each digit in the number
    for i, digit in enumerate(str(man)[::-1]):
        digit = int(digit)
        if digit != 0 or i == 0:
            if i == 0:
                kanji = numb_kanji[10000] + kanji
                hiragana = numb_hiragana[10000] + hiragana
            elif i == 1:
                kanji = numb_kanji[digit] + kanji
                hiragana = numb_hiragana[digit] + hiragana
            elif i == 2:
                kanji = numb_kanji[10] + numb_kanji[digit] + kanji
                hiragana = numb_hiragana[10] + numb_hiragana[digit] + hiragana
            elif i == 3:
                kanji = numb_kanji[digit] + numb_kanji[1000] + kanji
                hiragana = numb_hiragana[digit] + numb_hiragana[1000] + hiragana

    return kanji, hiragana, man * 10000

#print(lists_words_numbers())