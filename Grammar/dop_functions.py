import random
from Grammar.dictions_words import a


def ran(x):
    return random.choice(list(x.keys())) 


# Функции Дополнительные

def prop_no_sush(chosen_sush, var_ne): # выбор принадлежности предмета  или его свойства (цвет, форма и т.д.)
    jap_ne=''
    jap_ne_hir=''
    jap_ne_rus=''
    jap = ran(a['adj_for_small_object'][chosen_sush])
    hir = a['adj_for_small_object_hir'][chosen_sush][jap]
    rus = a['adj_for_small_object'][chosen_sush][jap]
    if jap in a['adj_non_predicative']:
        jap =jap+ 'な'
        hir = hir+'な'
    else:
        if var_ne =='only_pos': # только позитивные свойства, без отрицательного суффикса "кунай"
            var_ne = 0
        else:
            var_ne = random.randint(0,1)
        if var_ne==1:
            jap_ne = 'くない'
            jap_ne_hir = 'くない'
            jap_ne_rus = 'не'
        else:
            jap_ne = 'い'
            jap_ne_hir = 'い'
            jap_ne_rus = ''
    return jap,hir,rus,jap_ne,jap_ne_hir,jap_ne_rus


def prop_no_build(chosen_build): # выбор принадлежности/качества здания
    jap = ran(a['adj_for_buildings'][chosen_build])
    hir = a['adj_for_buildings_hir'][chosen_build][jap]
    rus = a['adj_for_buildings'][chosen_build][jap]
    if jap in a['adj_build_with_no']:
        jap = jap+'の'
        hir = hir +'の'
    elif jap in a['adj_non_predicative']:
        jap =jap+ 'な'
        hir = hir+'な'
    elif jap in a['adj_build_without_no']:
        jap =jap+ ''
        hir = hir+''
    else:
        jap =jap+ 'い'
        hir = hir+ 'い'
    return jap,hir,rus


class Glagols():
    # примеры использования
    # g = Glagols('glag_im_doing','all')
    # g = Glagols('glag_im_doing','choose',['withs','move'])
    def __init__(self,time,types,funcs=None):
        self.types = types
        self.time = time # время - будущее, настоящее или прошлое
        self.funcs = funcs if funcs else ['move','not_trans_slow','accusative','address','withs']

    def main(self):
        if self.types !='choose':
            rand_glag = random.choice(('move','not_trans_slow','accusative','address','withs'))
        else:
            rand_glag = random.choice(self.funcs)
        self.glag_jap = ran(a['glagol'][rand_glag])
        glag_hir = a['glagol'][rand_glag][self.glag_jap]
        glag_rus = a[self.time][self.glag_jap]
        jap_podl, jap_podl_hir, jap_podl_rus, padez, padez_rus = getattr(self, rand_glag)()
        return self.glag_jap,glag_hir,glag_rus,jap_podl,jap_podl_hir,jap_podl_rus,padez,padez_rus,rand_glag
        
    def accusative(self):
        jap_podl = ran(a['glag_accusative'][self.glag_jap])
        jap_podl_hir = a['glag_accusative_hir'][self.glag_jap][jap_podl]
        jap_podl_rus = a['glag_accusative'][self.glag_jap][jap_podl]
        padez = 'を'
        padez_rus = ''
        return jap_podl,jap_podl_hir,jap_podl_rus,padez,padez_rus

    def move(self):
        jap_podl = ran(a['buildings'])
        jap_podl_hir = a['buildings_hir'][jap_podl]
        jap_podl_rus = a['end_build2'][jap_podl]
        padez = 'に'
        padez_rus = 'в'
        return jap_podl,jap_podl_hir,jap_podl_rus,padez,padez_rus

    def address(self):
        jap_podl, jap_podl_hir, jap_podl_rus = who_f('end_family2','end_know2','suff')
        padez = 'に'
        padez_rus = ''
        return jap_podl,jap_podl_hir,jap_podl_rus,padez,padez_rus

    def withs(self):
        jap_podl, jap_podl_hir, jap_podl_rus = who_f('end_family3','end_know3','suff')
        padez = 'と'
        padez_rus = 'с'
        return jap_podl,jap_podl_hir,jap_podl_rus,padez,padez_rus
    
    def not_trans_slow(self):
        jap_podl, jap_podl_hir, jap_podl_rus=('','','')
        padez_rus = ''
        padez = ''
        return jap_podl,jap_podl_hir,jap_podl_rus,padez,padez_rus


class Times():
    # примеры использования
    # t = Times(glag_time')
    # t = Times('choose',['ho'])
    def __init__(self,glag,funcs=None):
        self.glag = glag # виды глаголов- все или отдельные
        self.funcs = funcs if funcs else ['we','ho','po','vov']

    def main(self):
        if self.glag == 'glag_budush': # время в будущем
            return random.choice((self.we(), self.po()))
        elif self.glag =='choose':
            if len(self.funcs) == 1:
                return getattr(self, self.funcs[0])()
            return random.choice([getattr(self, func)() for func in self.funcs])
    
    def we(self):
        time_jap = ran(a['week'])
        time_hir = a['week_hir'][time_jap] +'に'
        time_rus = ' в '+a['weeK_ending'][time_jap]
        time_jap = time_jap +'に'
        return time_jap,time_hir,time_rus
    
    def ho(self):
        noon = ran(a['hours'])
        time_jap = ran(a['hours'][noon])
        if random.randint(0,1)==0:
            han = '半'
            han_hir = 'はん'
            time_rus = ' в пол'+ a['hours_han'][time_jap]
        else:
            time_rus = ' в '+ a['hours'][noon][time_jap] +' '+ a['hours_rus'][noon][time_jap]
            han,han_hir=('','')
        time_hir = a['noon_hir'][noon]  + a['hours_hir'][noon][time_jap]+han_hir +'に'
        if noon =='午前' or han=='半':
            time_rus = time_rus+' ' + a['hours_rus_day'][time_jap]
        time_jap = noon+time_jap+han +'に'
        return time_jap,time_hir,time_rus
    
    def vov(self):
        even = ran(a['events'])
        time_jap = even +'の時'
        time_hir = a['events_hir'][even] + 'のとき'
        time_rus = ' во время ' + a['end_events'][even]
        return time_jap,time_hir,time_rus

    def po(self):
        do_posle = ran(a['posleslogi'])
        even = ran(a['events'])
        time_jap = even+ do_posle
        time_hir =a['events_hir'][even]+ a['posleslogi_hir'][do_posle]
        time_rus = a['posleslogi'][do_posle]+' '+a['end_events'][even]
        return time_jap,time_hir,time_rus


def date_year():
    year = random.randint(1980, 2024)
    years = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '10': '十', '0': '〇'},
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


def who_f(end_f,end_k,suff): # выбор имени/человека. обязательно надо выбирать окончания для семьи и знакомых людей
    list_who = random.choice((a['names'],a['family'],a['know_people']))
    who = ran(list_who)
    if who in a['names']:
        if suff !='no':
            jap_suff = ran(a['suff'])
            rus_who = a['names'][who]+a[suff][jap_suff]
            hir_who = a['names_hir'][who]+jap_suff
            who= who+jap_suff
        else:
            rus_who=a['names'][who]
            hir_who = a['names_hir'][who]
    elif who in a['know_people']:
        rus_who=a[end_k][who]
        hir_who = a['know_people_hir'][who]
    else:
        rus_who=a[end_f][who]
        hir_who = a['family_hur'][who]
    return who, hir_who,rus_who


def rus_end_num(rand_num,rand_obj): # функция для выбора окончания к существительному с числительным
    if rand_num=='1':
        end_num = a['end_small_1'][rand_obj]
    elif rand_num=='2' or rand_num=='3' or rand_num=='4':
        end_num = a['end_small_2'][rand_obj]
    else:
        end_num = a['end_small_5'][rand_obj]
    return end_num
