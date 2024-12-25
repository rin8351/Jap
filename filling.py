# -*- coding: utf-8 -*-
#  -------------------------------------- ПРОЧТИ ИНСТРУКЦЦИЮ КАК ДОБАВЛЯТЬ СЛОВА --------------------------------------
# Инструкция лежит в текстовом файле в этой же папке

import random 
from fill_num import a as suff_numbs, b1,k
from dictions_words import a

def ran(x):
    return random.choice(list(x.keys())) 

#===================================================================================================================================================
# Ниже два варианта функции lists_words и list_lessons, где функции разделены на номера уроков
#def lists_words():  # список функция с разделением на уроки, которые можно выбирать в приложении

    sp = { # Список функций всех уроков, которые можно выбирать в приложении
        'simple':[uk_rod_mest_f(),uk_koko_f()],
        '10': [napravl_f_with_mo(),event_start_stop()],
        '11':[aru(),where_how_much(),inside_outside_home(), uk_rod_mest_f_chisl(), iru_only(),iru_hito()],
        '12':[info_to_who(),what_he_doing_suru(),adjective_predicate()],
        '13':[ga_ski(), masyou(),take_nado(), kudasai(), kudasai_number(), prop_noadj_adverbs(),ga_ski_doing()],
        '14_15': [accus_ni_iku(),isyoni_in_build(),walk_and_doing(),reason_sorede(),probability_low_and_notlow()],
        '16': [ageru_simple(),kureru_simple(),morau_simple(),hairu_desu_nanika(),people_walk_there(),jyouzu_heta(),kara_and_donoka()],
        '17':[two_actions_de_form(), kara_made(), he_mistake(), to_meeting_go_with_friends(), masyou_after_event(), after_action_will_address()],
        '18': [ageru(),kureru(),morau(), all_demo(),all_demo_janai(), put_kudasai(),he_or_event_doing_and_continue(),condition(),
               kureru_help(),naru_senmon(), reason_kara(),naru_prop_and_like_it(),],
        '19':[reason_de(),comparison_1(),he_have(), he_talking_about_how(), comparison_2(),name_of_something(),this_property_conna(),
              homogeneous_predicates(),homogeneous_definitions(),if_that_then_that()],
        '20':[he_can(),i_want(), intention(),adjective_predicate_2(),definitions_expressed_by_the_verb(),reason_node()],
        '21':[can_do_it(),two_actions_formal(),qualifying_clause(),stable_its_sounds_good(),stable_ko_to_ga_aru(),stable_i_decited_to(), this_man_tell_about()],
        '22':[stable_actions_from_condition(),result_type(),negative_verb_gerund(),going_to_in_time(),tameni(),saying_that(),
              action_in_time_after_time()],
        '23':[passive(),passive_opportunity(), result_oku(),result_simau(), repetitive_aspect(), repetitive_aspect_adjectives(),double_case(),
              conditional_temporal_eba(), conditional_form_verb_ba_ii(), concessive_subordinate_noni(), substantivization_of_verbs(),substantivization_of_verbs_mono(),
              substantivization_of_verbs_no()],
        '24':[passive_omou(),passive_opportunity_intransitive(), concessive_subordinate_demo(), concessive_subordinate_demo_general(), intention_tokoro(),
              intention_tokoro_2(),subordinate_clause_mae_siro(),target_noni(), service_particle_toiu()],
        '25':[incentive_voice(),incentive_voice_kudasai(),permission_perform_action(),permission_perform_prop(),expression_prohibition(),
              expression_obligation(), reason_happening(), subordinate_clause_made(), service_word_sou()],
        '26':[imperative_passive_voice(),similary_youna(),similary_youna_target(), strive_to_do(), became_capable_youni(), prop_ha_sou(),
              bakari()],
        '27':[auxiliary_kuru(),auxiliary_iku(),distancing_in_time(),connection_with_ba(), condition_with_nara(),probability_you(),
              probability_sou(),measure_degree_hodo_kurai(), meaning_wake()],
        '28':[have_to_wazu(),time_jyouzu(), i_want_hosii(), state_mama(), reason_tame(), compulsion_yorihoka(), he_doing_onky_that()],
        '29':[politeness_imenn_skaz(), politeness_imenn_skaz_me(),politeness_2_3_action_special_verb(),politeness_2_3_action_special_form(),
              politeness_me_action_special_verb(),politeness_me_action_special_form(), politeness_there_build(),politeness_there_i()],
        '30':[totomoni(), simultaneity_kan(), expression_of_impossibility()],
        '31':[permission_perform_action_simple(), expression_obligation_myself(), i_have_no_time(), i_agreed_with_someone(), i_have_deal_for_it(),
              plan_youtei(), he_said_write_thought(), this_means_that(), similary_toorini()],
        '32':[do_you_know_that(), during_that_event(), i_dont_know_how_to_do(), invented_by_someone(), going_to_build(), doing_too_much(),
              just_recently_did_something(), made_conclusion()]
    }
    return sp

#  после добавления функция в общий список выше (lists_words) нужно вписать сюда названия второго уровня словаря (old, new и тд)
#list_lessons=['simple','10','11','12','13','14_15','16','17','18', '19','20','21','22', '23','24','25','26','27','28','29', '30', '31', '32']

# Ниже два варианта функции lists_words и list_lessons, где функции разделены на стили (именные, субстантиваторы и тд)
def lists_words():  # список функция с разделением на уроки, которые можно выбирать в приложении

    sp = {
    "Именные": [uk_rod_mest_f(), uk_rod_mest_f_chisl(), uk_koko_f(),prop_noadj_adverbs(),
                naru_senmon(),homogeneous_predicates(),adjective_predicate_2(),uk_koko_f_2()],
    "Субстантиваторы":[substantivization_of_verbs_mono(),definitions_expressed_by_the_verb(),substantivization_of_verbs_no()],
    'Простые': [napravl_f_with_mo(),event_start_stop(),what_he_doing(),what_he_doing_suru(),
               take_nado(),accus_ni_iku(),isyoni_in_build(),walk_and_doing(),people_walk_there(),
               to_meeting_go_with_friends(),kara_made(),naru_prop_and_like_it(),he_mistake(),he_or_event_doing_and_continue(),
               negative_verb_gerund()],
    'Средние':[he_can(),i_want(),if_that_then_that(), can_do_it(),i_want_hosii(), 
              qualifying_clause(),dake_takunaritai(),double_case()],
    'Называется, говорят':[this_man_tell_about(),he_talking_about_how(),name_of_something(),passive_omou(),
                       service_particle_toiu(),service_word_sou(),he_said_write_thought(),this_means_that(),
                       do_you_know_that()],
    'Ару_Иру':[iru_only(),iru_hito(),aru(),inside_outside_home(),adjective_predicate()],
    'Сколько':[where_how_much()],
    'Временные':[info_to_who(),going_to_in_time(),action_in_time_after_time(),subordinate_clause_mae_siro(),
            subordinate_clause_made(),time_jyouzu(),simultaneity_kan(),during_that_event()],
    'ga-ski_heta':[ga_ski(),jyouzu_heta(),substantivization_of_verbs()],
    'Вероятности': [probability_low_and_notlow(),saying_that(),probability_you(),probability_sou(),probability_rasii(),
                    have_to_wazu(),made_conclusion()],
    'Просьбы':[masyou(),masyou_after_event(),kudasai(),kudasai_number(),put_kudasai(),incentive_voice_kudasai()],
    'Дать_Получить':[ageru_simple(),ageru(),kureru_simple(),kureru(),morau_simple(),morau(),kureru_help()],
    'После':[after_action_will_address(),],
    'Причины':[reason_sorede(),reason_kara(),reason_de(),reason_node(),tameni(),target_noni(),reason_tame()],
    'Состояние':[condition(),stable_ko_to_ga_aru(),stable_actions_from_condition(),consists_the_fact(),strive_to_do(),
                 ga_ski_doing(),i_have_no_time(),i_agreed_with_someone(),i_have_deal_for_it(), i_dont_know_how_to_do()],
    'Сравнения':[comparison_1(),he_have(),comparison_2(),similary_youna(),similary_youna_target(),prop_ha_sou(),
                 similary_toorini()],
    'что-то_ничто_всё':[hairu_desu_nanika(),all_demo(),hairu_desu_nanika_to(),kara_and_donoka(), all_demo_janai()],
    'эмоциональное':[this_property_conna(),],
    'Два_действия':[two_actions_de_form(),homogeneous_definitions(), two_actions_formal()],
    'Намерения':[intention(),stable_i_decited_to()],
    "Виды глаголов":[result_type(),result_oku(),result_simau(),became_capable_youni(),auxiliary_kuru(),
                     auxiliary_iku(),distancing_in_time(),going_to_build()],
    'Особые слова':[niyotte(),repetitive_aspect(),repetitive_aspect_adjectives(),intention_tsumori(),
                    intention_tokoro(),intention_tokoro_2(),bakari(),subordinate_clause_uti(),measure_degree_hodo_kurai(),
                    meaning_wake(),state_mama(),compulsion_yorihoka(),he_doing_onky_that(),totomoni(),
                    expression_of_impossibility(),there_no_other_things(),plan_youtei(),invented_by_someone(),
                    doing_too_much(),just_recently_did_something()],
    'Залоги':[passive(),passive_opportunity(),passive_opportunity_intransitive(),incentive_voice(),imperative_passive_voice(),
              permission_perform_action_simple(),expression_obligation_myself()],
    'Хотя_Если':[conditional_temporal_eba(), concessive_subordinate_noni(),concessive_subordinate_demo(),time_form_in_tara_dara(),
                 concessive_subordinate_demo_general(),reason_happening(),time_form_in_tara_dara(),time_form_in_tara_dara_2(),
                 condition_with_nara()],
    "Можно_лучше":[conditional_form_verb_ba_ii(),stable_its_sounds_good(),permission_perform_prop(),permission_perform_action(),expression_prohibition(),
                   expression_obligation()],
    "Учтивые формы":[politeness_imenn_skaz(),politeness_imenn_skaz_me(),politeness_2_3_action_special_verb(),
                    politeness_2_3_action_special_form(),politeness_me_action_special_verb(),politeness_me_action_special_form(),
                     politeness_there_build(),politeness_there_i() ]
}
    return sp

list_lessons = ['Именные','Субстантиваторы','Простые','Средние','Называется, говорят','Ару_Иру','Сколько','Временные',
                'ga-ski_heta','Вероятности','Просьбы','Дать_Получить','После','Причины','Состояние','Сравнения',
                'что-то_ничто_всё','эмоциональное','Два_действия','Намерения','Виды глаголов','Особые слова','Залоги',
                'Хотя_Если','Можно_лучше','Учтивые формы']

#===================================================================================================================================================

glag_in_func={ # избирательные глаголы и слова в функциях (то есть не все глаголы выбираются в них, а только те что по смыслу функции подходят)
    'where_how_much':(('上','下','前','後ろ','右側','左側','隣','そば','中','間','近く','遠く')),
    'inside_outside_home':(('前','後ろ','右側','左側','隣','そば','近く','遠く')),
    'what_he_doing_suru':(('練習','そうじ')),
    'what_he_doing_suru_2':(('洗たく','たいそう','勉強','料理')),
    'ga_ski':(('買','ちゅうもん','探')),
    'masyou':(('買','ちゅうもん','持って来')),
    'accus_ni_iku':("if glag_jp != '買'or glag_jp != 'ちゅうもん':"),
    'isyoni_in_build':(('散歩','歩いて行','とお')),
    'ageru':(('買','ちゅうもん','作','持って来','借り','かえ','教え')),
    'hairu_desu_nanika':(('答え','聞_2','言',)),
    'people_walk_there':(('前','後ろ','右側','左側','隣','そば')),
    'masyou_after_event':(('買','ちゅうもん','持って来','見')),
    'kudasai':(('タンス','洋服ダンス')),
    'naru_senmon':(('先生','教授','中学校の教師','大学生')),
    'naru_prop_and_like_it':(('買','ちゅうもん','探')),
    'reason_kara':   (('見物','散歩','コンサート','パーティ','お祭り','お花見')),
    'reason_kara_2':(('公園','喫茶店','博物館','寺','動物園')),
    'he_can_but_mistake': (('答え','聞_2','話')),
    'he_can_but_mistake_2':(('しかし','でも')),
    'he_can_but_mistake_3':(('ふだん','時々','よく')),
    'put_kudasai':(('はこ','料理','れいぞころ')),
    'put_kudasai':(('しお','さとう')),
    'put_kudasai':(('ぎゅうにく','ぶたにく','とりにく')),
    'he_or_event_doing_and_continue':(('疲れて','忙しくて')),
    'condition':(('疲れて','忙しくて','よごれて','ふとって','年をとって')),
    'condition':(('もう','とても')),
    'condition':(('おぼえて','してい')),
    'kureru_help':(('てつだって','おくいて','なおして')), # なおして в другом условии
    'hairu_desu_nanika_to':(('答え','聞_2','言')),
    'this_property_conna':(('ふだん','いつも','よく')),
    'homogeneous_definitions':(('買','ちゅうもん','探')),
    'tameni':(('本','教科書','ざっし','新聞','辞典','映画')),
}

# Функции Дополнительные

def prop_no_sush(chosen_sush, var,var_ne): # выбор принадлежности предмета  или его свойства (цвет, форма и т.д.)
    jap_ne=''
    jap_ne_hir=''
    jap_ne_rus=''
    if var =='only_sush': # выбор только свойства прилагательного
        var = 0
    elif var == 'all': # выбор меджду прилагательным и принадлежностью человеку
        var = random.randint(0,1)
    if var==0:
        if chosen_sush in a['adj_for_small_object']:
            jap = ran(a['adj_for_small_object'][chosen_sush])
            hir = a['adj_for_small_object_hir'][chosen_sush][jap]
            rus = a['adj_for_small_object'][chosen_sush][jap]
            if jap in a['pril_with_no']:
                jap = jap +'の'
                hir = hir +'の'
            elif jap in a['adj_non_predicative']:
                jap =jap+ 'な'
                hir = hir+'な'
            else:
                if var_ne =='only_pos': # только позитивные свойства, без отрицательного суффикса "кунай"
                    var_ne = 0
                elif var_ne == 'all':
                    var_ne = random.randint(0,1)
                if var_ne==1:
                    if jap =='い':
                        jap='よ'
                        hir = 'よ'
                    jap_ne = 'くない'
                    jap_ne_hir = 'くない'
                    if random.randint(0,1)==0:
                        adverb = ran(a['adverbs']['negativ'])
                        jap =adverb + jap
                        hir = a['adverbs_hir']['negativ'][adverb] + hir
                        rus = a['adverbs']['negativ'][adverb]+' '+rus 
                        jap_ne_rus = ""
                    else:
                        jap_ne_rus = " не "
                else:
                    jap_ne = 'い'
                    jap_ne_hir = 'い'
                    jap_ne_rus = ''
                    if random.randint(0,1)==0:
                        adverb = ran(a['adverbs']['positiv'])
                        jap =adverb + jap
                        hir = a['adverbs_hir']['positiv'][adverb] + hir
                        rus = a['adverbs']['positiv'][adverb] +' '+rus
        else:
            jap,hir,rus = ('','','')
    else:
        rand = random.choice((a['names'],a['family']))
        jap = ran(rand)
        if rand == a['family']:
            rus = a['end_family4'][jap]
            hir = a['family_hur'][jap]
        else:
            jap_suff = ran(a['suff'])
            hir = a['names_hir'][jap]+jap_suff
            rus = rand[jap]+a['suff_no'][jap_suff]
            jap+jap_suff
        jap = jap +'の'
        hir = hir +'の'
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
        self.funcs = funcs if funcs else ['we','ho','po','vov','da_f'] # 

    def main(self):
        if self.glag == 'glag_budush':
            return random.choice((self.we(), self.ho(), self.da_f(), self.po()))
        elif self.glag == 'glag_nast_post':
             return random.choice((self.kan(), self.kan_nagai()))
        elif self.glag == 'glag_now':
            return self.now()
        elif self.glag == 'glag_past_post' or self.glag == 'glag_past_one_moment':
            return random.choice((self.we(), self.ho(), self.da_p(), self.po(),self.vov()))
        elif self.glag =='choose':
            if len(self.funcs) == 1:
                return getattr(self, self.funcs[0])()
            return random.choice([getattr(self, func)() for func in self.funcs])

    def now(self):
        time_jap = '今'
        time_hir = 'いま'
        time_rus = 'сейчас'
        return time_jap,time_hir,time_rus
    
    def kan(self):
        time_jap = ran(a['hours']['午前'])
        time_hir = a['hours_hir']['午前'][time_jap] + 'かん'
        time_rus_dop =  'в течение '
        time_rus = time_rus_dop+a['hours']['午前'][time_jap] +' '+ a['hours_rus']['午前'][time_jap]
        time_jap = time_jap + '間'
        return time_jap,time_hir,time_rus 
    
    def kan_nagai(self):
        time_jap = '長い間'
        time_hir = 'ながいかん'
        time_rus = 'долгое время'
        return time_jap,time_hir,time_rus
    
    def we(self):
        time_jap = ran(a['week'])
        time_hir = a['week_hir'][time_jap]
        time_rus = ' в '+a['weeK_ending'][time_jap]
        time_jap = time_jap
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
        time_hir = a['noon_hir'][noon]  + a['hours_hir'][noon][time_jap]+han_hir
        if noon =='午前' or han=='半':
            time_rus = time_rus+' ' + a['hours_rus_day'][time_jap]
        time_jap = noon+time_jap+han
        return time_jap,time_hir,time_rus
    
    def da_f(self): # время суток будущие
        time_jap = ran(a['time_fut']['budush'])
        time_hir = a['time_fut_hir']['budush'][time_jap]
        time_rus = a['time_fut']['budush'][time_jap]
        if self.glag == 'glag_nast_post':
            time_jap=time_jap+'毎日'
            time_hir = time_hir+'まいにち'
            time_rus = time_rus +' каждый день '
        return time_jap,time_hir,time_rus
    
    def da_p(self): # время суток прошлые
        time_jap = ran(a['time_fut']['past'])
        time_hir = a['time_fut_hir']['past'][time_jap]
        time_rus = a['time_fut']['past'][time_jap]
        if self.glag == 'glag_nast_post':
            time_jap=time_jap+'毎日'
            time_hir = time_hir+'まいにち'
            time_rus = time_rus +' каждый день '
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

def padez_napravl(): # выбор между двумя падежами направления
    padez = random.choice(('へ','に'))
    padez_hir = padez
    if padez =='へ':
        padez_rus =' к '
        end = 'end_build3'
    else:
        padez_rus=' в '
        end = 'end_build2'
    return padez,padez_hir,padez_rus,end

def date():
    month_numb = ran(k['月']['read'])
    month_jap = a['numbers_months'][month_numb]
    month_hir = k['月']['read'][month_numb]
    day_numb = ran(k['日']['read'])
    day_jap = a['numbers_day'][day_numb]
    day_hir = k['日']['read'][day_numb]
    if day_numb =='31':
        day_hir = 'おおみそか'
    jap= month_jap + '月' + day_jap
    hir = month_hir + day_hir
    rus =  k['日']['ending2'][day_numb] + ' '+ k['月']['ending2'][month_numb]
    return jap, hir, rus

def date_year():
    year = random.randint(1980, 2024)
    year_jap = ''.join(a['numbers_for_year'][digit] for digit in str(year))
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

def event_f():
    eve_jap = ran(a['events'])
    eve_hir = a['events_hir'][eve_jap]
    eve_rus = a['events'][eve_jap]
    return eve_jap,eve_hir,eve_rus

def dop_time(type): # дополнительное измерение времени- обычно, редко, еще и т.д. в качестве параметра- второй уровень словаря в adverbs
    dop_jap = ran(a['adverbs'][type])
    dop_hir = a['adverbs_hir'][type][dop_jap]
    dop_rus = a['adverbs'][type][dop_jap]
    return dop_jap, dop_hir,dop_rus

# функции генерации глаголов для присоединения их в функции для теста

def chose_glag_not_trans_fast(time_glag, podl): # функция для генерации подлеж и сказ. событие проиходит в какое то время, 
                                                  #  или человек совершает действие непереходное длящееся и не длящееся          
    if podl == 'rand':  # выбор подлежащего- либо рандомно, либо самим выбирать что будет- собвтие или человек что то сделал
        if random.randint(0,1)==0:
            podl = 'men'
        else:
            podl = 'even'
    if podl == 'even':
        jap_podl, jap_podl_hir, jap_podl_rus = event_f()
        glagol_type = 'not_trans_fast_ev'
    else:
        jap_podl, jap_podl_hir, jap_podl_rus = who_f('family','know_people','suff')
        glagol_type = random.choice(('not_trans_fast_men','not_trans_slow'))
    glag_jap = ran(a['glagol'][glagol_type])
    glag_hir = a['glagol'][glagol_type][glag_jap]
    glag_rus = a[time_glag][glag_jap]
    return jap_podl, jap_podl_hir, jap_podl_rus,glag_jap,glag_hir,glag_rus

def choose_glag_napravl(time_glag): # функция для генерации подлеж и сказ.- глагол направления
    who, hir_who, rus_who = who_f('family','know_people','suff') # в фуцию передаем какой суффикс использовать и окончание для родственника, если они выпадут
    glag_jap_origin = ran(a['glagol']['move'])
    glag_jap = glag_jap_origin
    glag_hir = a['glagol']['move'][glag_jap_origin]
    glag_rus = a[time_glag][glag_jap_origin]
    if glag_jap_origin == '行' or glag_jap_origin=='帰':
        sush_de = ran(a['glag_instrument'][glag_jap_origin])
        sush_de_hir = a['glag_instrument_hir'][glag_jap_origin][sush_de]
        sush_de_rus = a['glag_instrument'][glag_jap_origin][sush_de]
        padez = 'で'
        glag_jap = sush_de + padez + glag_jap_origin
        glag_hir = sush_de_hir + padez + glag_hir
        glag_rus = sush_de_rus+' '+glag_rus
    return glag_jap_origin, who, hir_who, rus_who,glag_jap,glag_hir,glag_rus

def choose_glag_accus(time): # функция для генерации подлеж и сказ. - действие над объектом- пить воду. читать книгу и т.д.
    glag_jp = ran(a['glagol']['accusative'])
    glag_hir = a['glagol']['accusative'][glag_jp]
    glag_rus = a[time][glag_jp]
    accus = ran(a['glag_accusative'][glag_jp])
    accus_hir = a['glag_accusative_hir'][glag_jp][accus]
    accus_rus = a['glag_accusative'][glag_jp][accus]
    if glag_jp =='聞_1' or glag_jp =='聞_2':
        glag_jp = '聞'
    return glag_jp, glag_hir, glag_rus, accus, accus_hir, accus_rus

# Функции для теста именные-----------------------------------------------------------------------------------------------
def uk_rod_mest_f():
    print('uk_rod_mest_f')
    jap1 = ran(a['small object'])
    hir = a['small object_hir'][jap1]
    rus1 = a['small object'][jap1]
    prinadl1 = 'принадлежит'
    jap_who, hir_who, rus_who = who_f('end_family2', 'end_know2', 'suff_no2')
    uk_rod_mest = [ran(a['uno']), jap1, 'は', jap_who, 'の', 'もの', ran(a['desu'])
        ]
    uk_rod_mest_hir = ''.join([uk_rod_mest[0], hir, 'は', hir_who, 'の', 'もの',
        uk_rod_mest[6]])
    uk_rod_mest_rus = ' '.join([a['uno'][uk_rod_mest[0]], rus1, a['desu'][
        uk_rod_mest[6]], prinadl1, rus_who])
    uk_rod_mest = ''.join(uk_rod_mest)
    return (uk_rod_mest, uk_rod_mest_hir, uk_rod_mest_rus, uk_rod_mest_f.
        __name__)

def uk_rod_mest_f_chisl():
    print('uk_rod_mest_f_chisl')
    ran_sush = ran(a['small object'])
    ran_sush_hir = a['small object_hir'][ran_sush]
    suff_obj = a['suffix for quantity'][ran_sush]
    suff_obj_hir = a['suffix for quantity_hir'][ran_sush]
    jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(ran_sush
        , 'only_sush', 'all')
    who, hir_who, rus_who = who_f('end_family4', 'end_know4', 'suff')
    rand_num = ran(a['numbers'])
    end_num = rus_end_num(rand_num, ran_sush)
    uk_rod_mest = [ran(a['uno']), rand_num, suff_obj, 'の', ran_sush, 'は',
        jap1, jap1_ne, 'です']
    uk_rod_mest_hir = ''.join([uk_rod_mest[0], rand_num, suff_obj_hir, 'の',
        ran_sush_hir, 'は', hir1, jap1_ne_hir, 'です'])
    uk_rod_mest_rus = ' '.join([a['uno'][uk_rod_mest[0]], rand_num, end_num,
        '-', jap1_ne_rus, rus1])
    uk_rod_mest = ''.join(uk_rod_mest)
    return (uk_rod_mest, uk_rod_mest_hir, uk_rod_mest_rus,
        uk_rod_mest_f_chisl.__name__)

def uk_koko_f():
    print('uk_koko_f')
    ran_build = ran(a['buildings'])
    jap2, hir, rus2 = prop_no_build(ran_build)
    jap2_2, hir2, rus2_2 = prop_no_build(ran_build)
    uk_koko = [ran(a['koko']), 'は', jap2, ran_build, 'です']
    uk_koko_hir = ''.join([uk_koko[0], 'は', hir, a['buildings_hir'][
        ran_build], uk_koko[4]])
    uk_koko_rus = ' '.join([a['koko'][uk_koko[0]], rus2, a['buildings'][
        uk_koko[3]]])
    uk_koko = ''.join(uk_koko)
    return uk_koko, uk_koko_hir, uk_koko_rus, uk_koko_f.__name__

def napravl_f_with_mo():
    print('napravl_f_with_mo')
    glag_time = 'glag_budush'
    (glag_jap_origin, who, hir_who, rus_who, glag_jap, glag_hir, glag_rus
        ) = choose_glag_napravl(glag_time)
    padez, padez_hir, padez_rus, end = padez_napravl()
    build1 = ran(a['buildings'])
    build2 = ran(a['buildings'])
    build1_hir = a['buildings_hir'][build1]
    build2_hir = a['buildings_hir'][build2]
    build1_rus = a[end][build1]
    build2_rus = a[end][build2]
    t = Times(glag_time)
    time_jap, time_hir, time_rus = t.main()
    if random.randint(0, 1) == 0:
        napravl = [time_jap, 'に', who, 'は', build1, padez, 'も、', build2,
            padez, 'も', glag_jap, a['glag_form'][glag_jap_origin][2], 'ます']
        napravl_hir = ''.join([time_hir, 'に', hir_who, 'は', build1_hir,
            padez_hir, 'も、', build2_hir, padez, 'も', glag_hir, a[
            'glag_form'][glag_jap_origin][2], 'ます'])
        napravl_rus = ' '.join([rus_who, time_rus, glag_rus, 'и', padez_rus,
            build1_rus, ', и', padez_rus, build2_rus])
    else:
        napravl = [time_jap, 'に', who, 'は', build1, padez, glag_jap, a[
            'glag_form'][glag_jap_origin][2], 'ます', build2, padez, 'も',
            glag_jap, a['glag_form'][glag_jap_origin][2], 'ます']
        napravl_hir = ''.join([time_hir, 'に', hir_who, 'は', build1_hir,
            padez_hir, glag_hir, a['glag_form'][glag_jap_origin][2], 'ます',
            build2_hir, padez, 'も', glag_jap, a['glag_form'][
            glag_jap_origin][2], 'ます'])
        napravl_rus = ' '.join([rus_who, time_rus, glag_rus, padez_rus,
            build1_rus, '. ', padez_rus, build2_rus, 'тоже', glag_rus])
    napravl = ''.join(napravl)
    return napravl, napravl_hir, napravl_rus, napravl_f_with_mo.__name__

def event_start_stop():
    print('event_start_stop')
    glag_time = 'glag_budush'
    jap_podl, jap_podl_hir, jap_podl_rus, glag_jap, glag_hir, glag_rus = (
        chose_glag_not_trans_fast(glag_time, 'rand'))
    dop_jap, dop_hir, dop_rus = '', '', ''
    if glag_jap in a['glagol']['not_trans_fast_men'] or glag_jap in a['glagol'
        ]['not_trans_fast_ev']:
        t = Times('choose', ['ho'])
        time_jap, time_hir, time_rus = t.main()
    else:
        t = Times(glag_time)
        time_jap, time_hir, time_rus = t.main()
    copula = 'ます'
    form = a['glag_form'][glag_jap][2]
    ev_st_st_jap = [time_jap, 'に', jap_podl, 'は', dop_jap, glag_jap, form,
        copula]
    ev_st_st_jap_hir = ''.join([time_hir, 'に', jap_podl_hir, 'は', dop_hir,
        glag_hir, form, copula])
    ev_st_st_jap_rus = ' '.join([jap_podl_rus, dop_rus, glag_rus, time_rus])
    ev_st_st_jap = ''.join(ev_st_st_jap)
    return (ev_st_st_jap, ev_st_st_jap_hir, ev_st_st_jap_rus,
        event_start_stop.__name__)

def iru_only():
    print('iru_only')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    where = random.choice(('room', 'buildings'))
    if where == 'room':
        end = 'end_room'
        wh_hir = 'room_hir'
    else:
        end = 'end_build4'
        wh_hir = 'buildings_hir'
    jap_w = ran(a[where])
    jap_iru = [jap_w, 'には', jap_podl, 'しか', 'いません']
    jap_hir = ''.join([a[wh_hir][jap_w], 'に', jap_podl_hir, 'しか', 'いません'])
    rus_iru = ''.join(['в ', a[end][jap_w],
        ' находится только (с сожалением)', jap_podl_rus])
    jap_iru = ''.join(jap_iru)
    return jap_iru, jap_hir, rus_iru, iru_only.__name__

def iru_hito():
    print('iru_hito')
    where = random.choice(('room', 'buildings'))
    if where == 'room':
        end = 'end_room'
        wh_hir = 'room_hir'
    else:
        end = 'end_build4'
        wh_hir = 'buildings_hir'
    jap_w = ran(a[where])
    rand_numb = ran(k['人']['read'])
    rand_jap = a['numbers'][rand_numb]
    rand_hir = k['人']['read'][rand_numb]
    rand_rus = k['人']['ending'][rand_numb]
    jap_iru = [jap_w, 'に', rand_jap, '人', 'が', 'います']
    jap_hir = ''.join([a[wh_hir][jap_w], 'に', rand_hir, 'が', 'います'])
    rus_iru = ''.join(['в ', a[end][jap_w], ' находится', rand_numb, rand_rus])
    jap_iru = ''.join(jap_iru)
    return jap_iru, jap_hir, rus_iru, iru_hito.__name__

def aru():
    print('aru')
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['small object'][obj]
    where = random.choice(('room', 'buildings'))
    if where == 'room':
        end = 'end_room'
        wh_hir = 'room_hir'
    else:
        end = 'end_build4'
        wh_hir = 'buildings_hir'
    jap_w = ran(a[where])
    if random.randint(0, 1) == 0:
        jap_iru = [jap_w, 'に', '何', 'が', 'あり', 'ますか？', obj, 'が', 'あり', 'ます']
        jap_hir = ''.join([a[wh_hir][jap_w], 'に', 'なに', 'が', 'あり', 'ますか？',
            obj_hir, 'が', 'あり', 'ます'])
        rus_iru = ''.join(['Что', ' находится в', a[end][jap_w], '? ', obj_rus]
            )
    else:
        jap_iru = [obj, 'は', 'どこ', 'に', 'あり', 'ますか？', jap_w, 'に', 'あり', 'ます']
        jap_hir = ''.join([obj_hir, 'は', 'どこ', 'に', 'あり', 'ますか？', a[wh_hir]
            [jap_w], 'に', 'あり', 'ます'])
        rus_iru = ' '.join(['Где находится', obj_rus, '?', obj_rus,' находится', 'в ', a[end][jap_w]])
    jap_iru = ''.join(jap_iru)
    return jap_iru, jap_hir, rus_iru, aru.__name__

def where_how_much():
    print('where_how_much')
    glag_jap = 'あ'
    rand_where = ran(a['furniture'])
    rand_obj = ran(a['small object'])
    suff_obj = a['suffix for quantity'][rand_obj]
    suff_obj_hir = a['suffix for quantity_hir'][rand_obj]
    rand_posl = random.choice(('上', '下', '前', '後ろ', '右側', '左側', '隣', 'そば',
        '中', '間', '近く', '遠く'))
    if rand_posl == '上':
        end = a['end_furniture']['上'][rand_where]
    elif rand_posl == '右側' or rand_posl == '左側' or rand_posl == '中' or rand_posl == '遠く':
        end = a['end_furniture']['右側'][rand_where]
    else:
        end = a['end_furniture']['下'][rand_where]
    if rand_posl == '間':
        rand_where2 = ran(a['furniture'])
        rand_where1 = rand_where + 'と' + rand_where2
        hir = a['furniture_hir'][rand_where] + 'と' + a['furniture_hir'][
            rand_where2]
        end = end + ' и ' + a['end_furniture']['下'][rand_where2]
    else:
        rand_where1 = rand_where
        hir = a['furniture_hir'][rand_where1]
    rand_num = ran(a['numbers'])
    end_num = rus_end_num(rand_num, rand_obj)
    jap = [rand_where1, 'の', rand_posl, 'に', rand_obj, 'が', rand_num,
        suff_obj, glag_jap, a['glag_form'][glag_jap][2], 'ます']
    hir = ''.join([hir, 'の', a['area_hir'][rand_posl], 'に', a[
        'small object_hir'][rand_obj], 'が', rand_num, suff_obj_hir,
        glag_jap, a['glag_form'][glag_jap][2], 'ます'])
    rus = ' '.join([a['area'][rand_posl], end, 'есть', rand_num, end_num])
    jap = ''.join(jap)
    return jap, hir, rus, where_how_much.__name__

def inside_outside_home():
    print('inside_outside_home')
    who = ran(a['names'])
    who_hir = a['names_hir'][who]
    if random.randint(0, 1) == 1:
        if random.randint(0, 1) == 1:
            rand_where = ran(a['insides'])
            rand_where_hir = a['insides_hir'][rand_where]
            rand_posl = random.choice(('前', '後ろ', '右側', '左側', '隣', 'そば',
                '近く', '遠く'))
            rand_posl_hir = a['area_hir'][rand_posl]
            if rand_posl == '右側' or rand_posl == '左側':
                rand_posl_end = a['end_insides2'][rand_where]
            else:
                rand_posl_end = a['end_insides3'][rand_where]
            where_jap = rand_where + 'の' + rand_posl
            where_hir = rand_where_hir + 'の' + rand_posl_hir
            where_rus = a['area'][rand_posl] + ' ' + rand_posl_end
            dop_pad = 'には、'
            dop_pad_hir = 'には、'
            dop_pad_rus = 'В доме '
        else:
            rand_num = ran(a['階']['read'])
            where_jap = a['numbers'][rand_num] + '階'
            where_hir = a['階']['read'][rand_num]
            where_rus = 'на ' + a['階']['ending2'][rand_num] + ' этаже '
            dop_pad = 'の'
            dop_pad_hir = 'の'
            dop_pad_rus = 'В доме '
        skazuemoe = ran(a['insides'])
        skazuemoe_hir = a['insides_hir'][skazuemoe]
        skazuemoe_rus = a['insides'][skazuemoe]
        glag = 'あります'
        glag_rus = ' есть '
        jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(
            'ins', 'only_sush', 'all')
    else:
        jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = ['', '', '',
            '', '', '']
        rand_where = ran(a['outsides'])
        rand_where_hir = a['outsides_hir'][rand_where]
        skazuemoe = ran(a['animals'])
        skazuemoe_hir = a['animals_hir'][skazuemoe]
        skazuemoe_rus = a['animals'][skazuemoe]
        dop_pad = 'の外に'
        dop_pad_hir = 'のそとに'
        dop_pad_rus = 'Снаружи дома '
        rand_posl = 'そば'
        rand_posl_end = a['end_outsides'][rand_where]
        where_jap = rand_where + 'の' + rand_posl
        where_hir = rand_where_hir + 'の' + rand_posl
        where_rus = a['area'][rand_posl] + ' ' + rand_posl_end
        glag = 'います'
        glag_rus = ' есть '
    ins_out_jap = [who, 'の', '家', dop_pad, where_jap, 'に', jap1, jap1_ne,
        skazuemoe, 'が', glag]
    ins_out_hir = ''.join([who_hir, 'の', 'いえ', dop_pad_hir, where_hir, 'に',
        hir1, jap1_ne_hir, skazuemoe_hir, 'が', glag])
    ins_out_rus = ' '.join([dop_pad_rus, a['names'][who], where_rus,
        glag_rus, jap1_ne_rus, rus1, skazuemoe_rus])
    ins_out_jap = ''.join(ins_out_jap)
    return ins_out_jap, ins_out_hir, ins_out_rus, inside_outside_home.__name__

def what_he_doing():
    print('what_he_doing')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    if random.randint(0, 1) == 0:
        glag_time = 'glag_now'
        glag_jap, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
            choose_glag_accus(glag_time))
        dop_jap = ''
        dop_hir = ''
        dop_rus = ''
    else:
        glag_time = 'glag_budush'
        glag_jap, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
            choose_glag_accus(glag_time))
        t = Times('glag_budush')
        dop_jap, dop_hir, dop_rus = t.main()
    if glag_jap in a['glag_for_build']:
        where = random.choice(a['glag_for_build'][glag_jap])
        where_hir = a['buildings_hir'][where]
        where_rus = 'в ' + a['end_build4'][where]
        de = 'で'
    else:
        where, where_hir, where_rus = '', '', ''
        de = ''
    if glag_jap in a['glag_place_small']:
        dop_jap = ran(a['glag_place_small'][glag_jap])
        dop_hir = a['glag_place_small_hir'][glag_jap][dop_jap]
        dop_rus = a['glag_place_small'][glag_jap][dop_jap]
        dop_hir = dop_hir + 'に'
        dop_jap = dop_jap + 'に'
    if glag_jap in a['glag_instrument']:
        dop_jap2 = ran(a['glag_instrument'][glag_jap])
        dop_hir2 = a['glag_instrument_hir'][glag_jap][dop_jap2]
        dop_rus2 = a['glag_instrument'][glag_jap][dop_jap2]
        dop_hir = dop_hir2 + 'で' + dop_hir
        dop_jap = dop_jap2 + 'で' + dop_jap
        dop_rus = dop_rus2 + ' ' + dop_rus
    jap = [jap_podl, 'は', where, de, dop_jap, accus, 'を', glag_jap, a[
        'glag_form'][glag_jap][2], 'ます']
    hir = ''.join([jap_podl_hir, 'は', where_hir, de, dop_hir, accus_hir,
        'を', glag_hir, a['glag_form'][glag_jap][2], 'ます'])
    rus = ' '.join([jap_podl_rus, where_rus, dop_rus, glag_rus, accus_rus])
    jap = ''.join(jap)
    return jap, hir, rus, what_he_doing.__name__


def what_he_doing_suru():
    print('what_he_doing_suru')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    glag_time = 'glag_nast_post'
    t = Times('choose', ['kan'])
    dop_jap, dop_hir, dop_rus = t.main()
    padez = 'を'
    if random.randint(0, 1) == 0:
        glag_jap = random.choice(('練習', 'そうじ'))
        glag_hir = a['glagol']['accusative'][glag_jap]
        glag_rus = a[glag_time][glag_jap]
        accus = ran(a['glag_accusative'][glag_jap])
        accus_hir = a['glag_accusative_hir'][glag_jap][accus]
        accus_rus = a['glag_accusative'][glag_jap][accus]
        no = 'の'
    else:
        glag_jap = random.choice(('洗たく', 'たいそう', '勉強', '料理'))
        glag_hir = a['glagol']['not_trans_slow'][glag_jap]
        glag_rus = a[glag_time][glag_jap]
        accus, accus_hir, accus_rus = '', '', ''
        no = ''
    jap = [jap_podl, 'は', dop_jap, 'ぐらい', 'に', accus, no, glag_jap, padez,
        'しています']
    hir = ''.join([jap_podl_hir, 'は', dop_hir, 'ぐらい', 'に', accus_hir, no,
        glag_hir, padez, 'しています'])
    rus = ' '.join([jap_podl_rus, 'примерно', dop_rus, glag_rus, accus_rus])
    jap = ''.join(jap)
    return jap, hir, rus, what_he_doing_suru.__name__


def info_to_who():
    print('info_to_who')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    jap_podl2, jap_podl_hir2, jap_podl_rus2 = who_f('end_family2',
        'end_know2', 'suff_no2')
    glag_jap = ran(a['glagol']['address'])
    glag_hir = a['glagol']['address'][glag_jap]
    glag_time = random.choice(('glag_budush', 'glag_past_post'))
    if glag_time == 'glag_budush':
        ch = ['vov', 'we']
    else:
        ch = ['vov', 'da_f', 'we']
    glag_rus = a[glag_time][glag_jap]
    if glag_jap == '聞_1' or glag_jap == '聞_2':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][2]
    if glag_jap in a['glag_accusative']:
        sunh_wo = ran(a['glag_accusative'][glag_jap])
        sush_wo_hir = a['glag_accusative_hir'][glag_jap][sunh_wo]
        sush_wo_rus = a['glag_accusative'][glag_jap][sunh_wo]
        glag_jap = sunh_wo + 'を' + glag_jap
        glag_hir = sush_wo_hir + 'を' + glag_hir
        glag_rus = glag_rus + ' ' + sush_wo_rus
    t = Times('choose', ch)
    if glag_time == 'glag_past_post':
        copula = 'ました'
    else:
        copula = 'ます'
    time_jap, time_hir, time_rus = t.main()
    jap = [time_jap, ',', jap_podl, 'は', jap_podl2, 'に', glag_jap, form, copula
        ]
    hir = ''.join([time_hir, ',', jap_podl_hir, 'は', jap_podl_hir2, 'に',
        glag_hir, form, copula])
    rus = ' '.join([jap_podl_rus, time_rus, glag_rus, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, info_to_who.__name__


def adjective_predicate():
    print('adjective_predicate')
    room = ran(a['room'])
    room_hir = a['room_hir'][room]
    room_rus = a['end_room'][room]
    un = ran(a['uno'])
    un_rus = a['uno_end'][un]
    obj1, obj2 = random.sample(list(a['room_objects'].keys()), k=2)
    obj_hir1 = a['room_objects_hir'][obj1]
    obj_hir2 = a['room_objects_hir'][obj2]
    obj1_rus = a['room_objects'][obj1]
    obj2_rus = a['room_objects'][obj2]
    rand_prop = ran(a['adj_rooms_si'])
    if rand_prop == 'colors':
        zen = '全部'
        zen_hir = 'ぜんぶ'
        zen_rus = 'полностью (сплошь)'
    else:
        zen, zen_hir, zen_rus = '', '', ''
    prop1 = ran(a['adj_rooms_si'][rand_prop])
    prop1_hir = a['adj_rooms_si_hir'][rand_prop][prop1]
    prop1_rus = a['adj_rooms_si'][rand_prop][prop1]
    prop2 = ran(a['adj_rooms_si'][rand_prop])
    prop2_hir = a['adj_rooms_si_hir'][rand_prop][prop2]
    prop2_rus = a['adj_rooms_si'][rand_prop][prop2]
    jap = [un, room, 'は', zen, prop1, obj1, 'が', 'ありますし、', obj2, 'が', prop2,
        'です']
    hir = ''.join([un, room_hir, 'は', zen_hir, prop1_hir, obj_hir1, 'が',
        'ありますし、', obj_hir2, 'が', prop2_hir, 'です'])
    rus = ' '.join(['В ', un_rus, room_rus, '-', zen_rus, prop1_rus,
        obj1_rus, ',и', obj2_rus, prop2_rus])
    jap = ''.join(jap)
    return jap, hir, rus, adjective_predicate.__name__


def ga_ski():
    print('ga_ski')
    jap_podl, jap_podl_hir, jap_podl_rus = '私', 'わたし', 'я'
    thing = ran(a['food'])
    thing_hir = a['food_hir'][thing]
    thing_rus = a['food'][thing]
    if random.randint(0, 1) == 0:
        dai_ski = '大'
        dai_ski_hir = 'だい'
        dai_ski_rus = 'очень'
    else:
        dai_ski, dai_ski_hir, dai_ski_rus = '', '', ''
    if random.randint(0, 1) == 0:
        ski = '好き'
        ski_hir = 'すき'
        ski_rus = 'люблю'
    else:
        ski = 'きらい'
        ski_hir = 'きらい'
        ski_rus = 'не люблю'
    jap = [jap_podl, 'は', thing, 'が', dai_ski, ski, 'です']
    hir = ''.join([jap_podl_hir, 'は', thing_hir, 'が', dai_ski_hir, ski_hir,
        'です'])
    rus = ' '.join([jap_podl_rus, dai_ski_rus, ski_rus, thing_rus])
    jap = ''.join(jap)
    return jap, hir, rus, ga_ski.__name__


def masyou():
    print('masyou')
    glag = random.choice(('買', 'ちゅうもん', '持って来'))
    glag_hir = a['glagol']['accusative'][glag]
    predmet = ran(a['glag_accusative'][glag])
    predmet_hir = a['glag_accusative_hir'][glag][predmet]
    predmet_rus = a['glag_accusative'][glag][predmet]
    if random.randint(0, 1) == 0:
        jap = ['私', 'が', predmet, 'を', glag, a['glag_form'][glag][2], 'ましょうか']
        hir = ''.join(['わたし', 'が', predmet_hir, 'を', glag_hir, a[
            'glag_form'][glag][2], 'ましょうか'])
        rus = ' '.join(['Давайте я', a['glag_im_going_todo'][glag],
            predmet_rus,
            ' (прим. Предложение своего действия в ситуации, когда решение о совершении действия уже принято)'
            ])
    else:
        jap = [predmet, 'を', glag, a['glag_form'][glag][2], 'ましょうか']
        hir = ''.join([predmet_hir, 'を', glag_hir, a['glag_form'][glag][2],
            'ましょうか'])
        rus = ' '.join(['Я', a['glag_im_going_todo'][glag], predmet_rus,
            """ (прим. Предложение своего действия в ситуации, когда это действие надо совершить, но никто об этом не сказал
 Второй вариант: Говорящий знает, что собеседник тоже намерен выполнить действие)"""
            ])
    jap = ''.join(jap)
    return jap, hir, rus, masyou.__name__


def take_nado():
    print('take_nado')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    food1, food2 = random.sample(list(a['food'].keys()), k=2)
    if random.randint(0, 1) == 0:
        glag, glag_hir, padez, padez_hir = 'おき', 'おき', 'の上に', 'のうえに'
        gal_rus = 'положил на стол'
    else:
        glag, glag_hir, padez, padez_hir = '取り', 'とり', 'から', 'から'
        gal_rus = 'взял со стола'
    jap = [jap_podl, 'は', ' テーブル', padez, food1, 'や', food2, 'など', 'を',
        glag, 'ました']
    hir = ''.join([jap_podl_hir, 'は', ' テーブル', padez_hir, a['food_hir'][
        food1], 'や', a['food_hir'][food2], 'など', 'を', glag_hir, 'ました'])
    rus = ' '.join([jap_podl_rus, gal_rus, a['end_food'][food1], ',', a[
        'end_food'][food2], 'и так далее'])
    jap = ''.join(jap)
    return jap, hir, rus, take_nado.__name__


def accus_ni_iku():
    print('accus_ni_iku')
    glag_time = random.choice(('glag_budush', 'glag_nast_post',
        'glag_past_post'))
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    zen, zen_hir, zen_rus = '', '', ''
    if random.randint(0, 1) == 0:
        glag_jp = ran(a['glagol']['not_trans_slow'])
        glag_hir = a['glagol']['not_trans_slow'][glag_jp]
        glag_rus = a['glag_verb_stem'][glag_jp]
        accus, accus_hir, accus_rus = '', '', ''
        padez = ''
    else:
        glag_jp, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
            choose_glag_accus('glag_verb_stem'))
        if glag_time == 'glag_past_post':
            if glag_jp != '買' or glag_jp != 'ちゅうもん':
                if random.randint(0, 1) == 0:
                    zen = '全部'
                    zen_hir = 'ぜんぶ'
                    zen_rus = 'полностью (сплошь)'
        padez = 'を'
    t = Times('choose', ['ho'])
    if glag_time == 'glag_past_post':
        copula = 'ました'
    else:
        copula = 'ます'
    dop_jap, dop_hir, dop_rus = t.main()
    jap = [jap_podl, 'は', zen, dop_jap, 'ごろ', accus, padez, glag_jp, a[
        'glag_form'][glag_jp][2], 'に', '行き', copula]
    hir = ''.join([jap_podl_hir, 'は', zen_hir, dop_hir, 'ごろ', accus_hir,
        padez, glag_hir, a['glag_form'][glag_jp][2], 'に', 'いき', copula])
    rus = ' '.join([jap_podl_rus, dop_rus, 'примерно', a[glag_time]['行'],
        zen_rus, glag_rus, accus_rus])
    jap = ''.join(jap)
    return jap, hir, rus, accus_ni_iku.__name__


def isyoni_in_build():
    print('isyoni_in_build')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    jap_podl2, jap_podl_hir2, jap_podl_rus2 = who_f('end_family3',
        'end_know3', 'suff')
    jap = [jap_podl, 'は', jap_podl2, 'ました']
    glag_jp = random.choice(('読', '飲', '食', '聞_1', '買'))
    where = random.choice(a['glag_for_build'][glag_jp])
    print('where', where)
    where_hir = a['buildings_hir'][where]
    where_rus = 'в ' + a['end_build4'][where]
    glag_hir = a['glagol']['accusative'][glag_jp]
    glag_rus = a['glag_past_post'][glag_jp]
    accus = ran(a['glag_accusative'][glag_jp])
    accus_hir = a['glag_accusative_hir'][glag_jp][accus]
    accus_rus = a['glag_accusative'][glag_jp][accus]
    if glag_jp == '聞_1':
        glag_jp = '聞'
    jap = [jap_podl, 'は', jap_podl2, 'といしょうに', where, 'で', accus, 'を',
        glag_jp, a['glag_form'][glag_jp][2], 'ました']
    hir = ''.join([jap_podl_hir, 'は', jap_podl_hir2, 'といしょうに', where_hir,
        'で', accus_hir, 'を', glag_hir, a['glag_form'][glag_jp][2], 'ました'])
    rus = ' '.join([jap_podl_rus, 'вместе с', jap_podl_rus2, glag_rus,
        accus_rus, where_rus])
    jap = ''.join(jap)
    return jap, hir, rus, isyoni_in_build.__name__


def walk_and_doing():
    print('walk_and_doing')
    jap_podl1, jap_podl_hir1, jap_podl_rus1 = who_f('family', 'know_people',
        'suff')
    glag_w = random.choice(('散歩', '歩いて行', 'とお'))
    print('glag_w', glag_w)
    for i in a['glagol']:
        if glag_w in a['glagol'][i]:
            glag_hir_w = a['glagol'][i][glag_w]
            glag_rus_w = a['glag_now'][glag_w]
    where = ran(a['street'])
    where_hir = a['street_hir'][where]
    where_rus = a['end_street'][where]
    rasst = ran(a['adverbs']['for_space'])
    rasst_hir = a['adverbs_hir']['for_space'][rasst]
    rasst_rus = a['end_adverbs'][rasst]
    g = Glagols('glag_nagara', 'choose', ['accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    print('glag_jap', glag_jap)
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][2]
    jap = [jap_podl1, 'は', jap_podl, padez, glag_jap, form, 'ながら', rasst,
        'の', where, 'を', glag_w, a['glag_form'][glag_w][2], 'ます']
    hir = ''.join([jap_podl_hir1, 'は', jap_podl_hir, padez, glag_hir, form,
        'ながら', rasst_hir, 'の', where_hir, 'を', glag_hir_w, a['glag_form'][
        glag_w][2], 'ます'])
    rus = ' '.join([jap_podl_rus1, glag_rus_w, 'по', rasst_rus, where_rus,
        ', ', glag_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, walk_and_doing.__name__


def ageru_simple():
    print('ageru_simple')
    who, hir_who, rus_who = who_f('end_family2', 'end_know2', 'no')
    who2, hir_who2, rus_who2 = who_f('family', 'know_people', 'suff')
    if who2[:2] in a['names']:
        who2 = '私'
        hir_who2 = 'わたし'
        rus_who2 = 'Я'
    else:
        rus_who2 = rus_who2 + '(близкий мне человек)'
    sen, sen_hir, sen_rus = '', '', ''
    if who == '妹' or who == '弟':
        glag = 'や'
    else:
        glag = 'あげ'
    if who in a['names']:
        if random.randint(0, 1) == 0:
            sen = '先生'
            sen_hir = 'せんせい'
            sen_rus = '-сенсею'
            glag = 'さしあげ'
        else:
            who = who + 'くん'
            hir_who = hir_who + 'くん'
            rus_who = rus_who + '-куну'
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['end_small_address'][obj]
    t = Times('choose', ['ho'])
    time_jap, time_hir, time_rus = t.main()
    day_jap, day_hir, day_rus = date()
    jap_prop, prop_hir, prop_rus, jap_ne, jap_ne_hir, jap_ne_rus = (
        prop_no_sush(obj, 'only_sush', 'only_pos'))
    jap = [day_jap, time_jap, 'に', who2, 'は', who, sen, 'に', jap_prop, obj,
        'を', glag, 'ました']
    hir = ''.join([day_hir, time_hir, 'に', hir_who2, 'は', hir_who, sen_hir,
        'に', prop_hir, obj_hir, 'を', glag, 'ました'])
    rus = ' '.join([day_rus, ' ', time_rus, ' ', rus_who2, 'дал', rus_who,
        sen_rus, prop_rus, obj_rus])
    jap = ''.join(jap)
    return jap, hir, rus, ageru_simple.__name__


def ageru():
    print('ageru')
    who, hir_who, rus_who = who_f('end_family2', 'end_know2', 'no')
    who2, hir_who2, rus_who2 = who_f('family', 'know_people', 'suff')
    if who2[:2] in a['names']:
        who2 = '私'
        hir_who2 = 'わたし'
        rus_who2 = 'Я'
    else:
        rus_who2 = rus_who2 + '(близкий мне человек)'
    sen, sen_hir, sen_rus = '', '', ''
    if who == '妹' or who == '弟':
        glag = 'や'
    else:
        glag = 'あげ'
    glag_jp = random.choice(('買', 'ちゅうもん', '作', '持って来', '借り', 'かえ', '教え'))
    glag_hir = a['glagol']['accusative'][glag_jp]
    if glag_jp == '借り':
        glag_rus = 'дал взаймы'
    else:
        glag_rus = a['glag_past_one_moment'][glag_jp]
    glag_form = a['glag_form'][glag_jp][6]
    if who in a['names']:
        if random.randint(0, 1) == 0:
            sen = '先生'
            sen_hir = 'せんせい'
            sen_rus = '-сенсею'
            glag = 'さしあげ'
        else:
            who = who + 'くん'
            hir_who = hir_who + 'くん'
            rus_who = rus_who + '-куну'
    day_jap, day_hir, day_rus = date()
    year_jap, year_hir, year_rus = date_year()
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['end_small_address'][obj]
    jap_prop, prop_hir, prop_rus, jap_ne, jap_ne_hir, jap_ne_rus = (
        prop_no_sush(obj, 'only_sush', 'only_pos'))
    jap = [year_jap, day_jap, 'に', who2, 'は', who, sen, 'に', jap_prop,
        jap_ne, obj, 'を', glag_jp, glag_form, glag, a['glag_form'][glag][2],
        'ました']
    hir = ''.join([year_hir, day_hir, 'に', hir_who2, 'は', hir_who, sen_hir,
        'に', prop_hir, jap_ne_hir, obj_hir, 'を', glag_hir, glag_form, glag,
        a['glag_form'][glag][2], 'ました'])
    rus = ' '.join([year_rus, day_rus, ', ', rus_who2, glag_rus, rus_who,
        sen_rus, prop_rus, obj_rus])
    jap = ''.join(jap)
    return jap, hir, rus, ageru.__name__


def kureru_simple():
    print('kureru_simple')
    who, hir_who, rus_who = who_f('family', 'know_people', 'no')
    who2, hir_who2, rus_who2 = who_f('end_family2', 'end_know2', 'suff_no2')
    if who2[:2] in a['names']:
        who2 = '私'
        hir_who2 = 'わたし'
        rus_who2 = 'мне'
    else:
        rus_who2 = rus_who2 + '(близкий мне человек)'
    sen, sen_hir, sen_rus = '', '', ''
    glag = 'くれ'
    glag_rus = 'дал'
    if who in a['names']:
        if random.randint(0, 1) == 0:
            sen = '先生'
            sen_hir = 'せんせい'
            sen_rus = '-сенсей'
            glag = 'くださ'
        else:
            who = who + 'くん'
            hir_who = hir_who + 'くん'
            rus_who = rus_who + '-кун'
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['end_small_address'][obj]
    t = Times('choose', ['ho'])
    time_jap, time_hir, time_rus = t.main()
    day_jap, day_hir, day_rus = date()
    jap = [day_jap, time_jap, 'に', who, sen, 'は', who2, 'に', obj, 'を', glag,
        a['glag_form'][glag][2], 'ました']
    hir = ''.join([day_hir, time_hir, 'に', hir_who, sen_hir, 'は', hir_who2,
        'に', obj_hir, 'を', glag, a['glag_form'][glag][2], 'ました'])
    rus = ' '.join([day_rus, ' ', time_rus, ' ', rus_who, sen_rus, glag_rus,
        rus_who2, obj_rus])
    jap = ''.join(jap)
    return jap, hir, rus, kureru_simple.__name__


def kureru():
    print('kureru')
    who, hir_who, rus_who = who_f('family', 'know_people', 'no')
    who2, hir_who2, rus_who2 = who_f('end_family2', 'end_know2', 'suff_no2')
    if who2[:2] in a['names']:
        who2 = '私'
        hir_who2 = 'わたし'
        rus_who2 = 'мне'
    else:
        rus_who2 = rus_who2 + '(близкий мне человек)'
    sen, sen_hir, sen_rus = '', '', ''
    glag = 'くれ'
    glag_jp = random.choice(('買', 'ちゅうもん', '作', '持って来', '借り', 'かえ', '教え'))
    glag_hir = a['glagol']['accusative'][glag_jp]
    if glag_jp == '借り':
        glag_rus = 'дал взаймы'
    else:
        glag_rus = a['glag_past_one_moment'][glag_jp]
    glag_form = a['glag_form'][glag_jp][6]
    if who in a['names']:
        if random.randint(0, 1) == 0:
            sen = '先生'
            sen_hir = 'せんせい'
            sen_rus = '-сенсей'
            glag = 'くださ'
        else:
            who = who + 'くん'
            hir_who = hir_who + 'くん'
            rus_who = rus_who + '-кун'
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['end_small_address'][obj]
    day_jap, day_hir, day_rus = date()
    year_jap, year_hir, year_rus = date_year()
    jap = [year_jap, day_jap, 'に', who, sen, 'は', who2, 'に', obj, 'を',
        glag_jp, glag_form, glag, a['glag_form'][glag][2], 'ました']
    hir = ''.join([year_hir, day_hir, 'に', hir_who, sen_hir, 'は', hir_who2,
        'に', obj_hir, 'を', glag_hir, glag_form, glag, a['glag_form'][glag][
        2], 'ました'])
    rus = ' '.join([year_rus, day_rus, ', ', rus_who, sen_rus, glag_rus,
        rus_who2, obj_rus])
    jap = ''.join(jap)
    return jap, hir, rus, kureru.__name__


def morau_simple():
    print('morau_simple')
    who, hir_who, rus_who = who_f('end_family4', 'end_know4', 'no')
    who2, hir_who2, rus_who2 = who_f('family', 'know_people', 'suff')
    if who2[:2] in a['names']:
        who2 = '私'
        hir_who2 = 'わたし'
        rus_who2 = 'Я'
    else:
        rus_who2 = rus_who2 + '(близкий мне человек)'
    sen, sen_hir, sen_rus = '', '', ''
    glag = 'もら'
    if who in a['names']:
        if random.randint(0, 1) == 0:
            sen = '先生'
            sen_hir = 'せんせい'
            sen_rus = '-сенсея'
            glag = 'いただ'
        else:
            who = who + 'くん'
            hir_who = hir_who + 'くん'
            rus_who = rus_who + '-куна'
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['end_small_address'][obj]
    t = Times('choose', ['da_f', 'da_p'])
    time_jap, time_hir, time_rus = t.main()
    jap = [time_jap, who2, 'は', who, sen, 'に', obj, 'を', glag, a[
        'glag_form'][glag][2], 'ました']
    hir = ''.join([time_hir, hir_who2, 'に', hir_who, sen_hir, 'に', obj_hir,
        'を', glag, a['glag_form'][glag][2], 'ました'])
    rus = ' '.join([time_rus, rus_who2, 'получил от', rus_who, sen_rus,
        obj_rus])
    jap = ''.join(jap)
    return jap, hir, rus, morau_simple.__name__


def morau():
    print('morau')
    who, hir_who, rus_who = who_f('end_family4', 'end_know4', 'no')
    who2, hir_who2, rus_who2 = who_f('family', 'know_people', 'suff')
    if who2[:2] in a['names']:
        who2 = '私'
        hir_who2 = 'わたし'
        rus_who2 = 'Я'
    else:
        rus_who2 = rus_who2 + '(близкий мне человек)'
    sen, sen_hir, sen_rus = '', '', ''
    glag = 'もら'
    if who in a['names']:
        if random.randint(0, 1) == 0:
            sen = '先生'
            sen_hir = 'せんせい'
            sen_rus = '-сенсея'
            glag = 'いただ'
        else:
            who = who + 'くん'
            hir_who = hir_who + 'くん'
            rus_who = rus_who + '-куна'
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['end_small_address'][obj]
    rus_words = {'買': 'покупку', 'ちゅうもん': 'заказ', '作': 'приготовку', '借り':
        'дачу в долг', 'かえ': 'возвращение', '教え': 'объяснение', '持って来':
        'приношение'}
    t = Times('choose', ['da_f', 'da_p'])
    time_jap, time_hir, time_rus = t.main()
    glag_jp = random.choice(('買', 'ちゅうもん', '作', '持って来', '借り', 'かえ', '教え'))
    glag_hir = a['glagol']['accusative'][glag_jp]
    glag_rus = rus_words[glag_jp]
    glag_form = a['glag_form'][glag_jp][6]
    obj_rus = a['end_return_small_object'][obj]
    jap = [time_jap, who2, 'は', who, sen, 'に', obj, 'を', glag_jp, glag_form,
        glag, a['glag_form'][glag][2], 'ました']
    hir = ''.join([time_hir, hir_who2, 'は', hir_who, sen_hir, 'に', obj_hir,
        'を', glag_hir, glag_form, glag, a['glag_form'][glag][2], 'ました'])
    rus = ' '.join([time_rus, rus_who2, 'получил от', rus_who, sen_rus,
        glag_rus, obj_rus])
    jap = ''.join(jap)
    return jap, hir, rus, morau.__name__


def hairu_desu_nanika():
    print('hairu_desu_nanika')
    where = ran(a['insides'])
    where_hir = a['insides_hir'][where]
    glag = random.choice(('答え', '聞_2', '言'))
    glag_hir = a['glagol']['address'][glag]
    glag_rus = a['glag_past_one_moment'][glag]
    if glag == '聞_2':
        glag = '聞'
    what_type = random.choice(('か', 'も'))
    what = '何' + what_type
    what_hir = 'なに' + what_type
    what_rus = a['nowhere_no_one'][what_type]['何']
    if what_type == 'も':
        masu = 'ませんでした'
        ne = 'не'
    else:
        masu = 'ました'
        ne = ''
    if random.randint(0, 1) == 0:
        glag_move = '出'
        glag_move_hir = 'で'
        glag_move_rus = 'вышел'
        padez = 'を'
        padez_rus = 'из'
        where_rus = a['end_insides2'][where]
    else:
        glag_move = '入'
        glag_move_hir = 'はい'
        glag_move_rus = 'зашёл'
        padez = 'に'
        padez_rus = 'в'
        where_rus = a['end_insides4'][where]
    jap = ['彼', 'は', where, padez, glag_move, a['glag_form'][glag][6], what,
        'を', glag, a['glag_form'][glag][2], masu]
    hir = ''.join(['かれ', 'は', where_hir, padez, glag_move_hir, a[
        'glag_form'][glag][6], what_hir, 'を', glag_hir, a['glag_form'][glag
        ][2], masu])
    rus = ' '.join(['Он', glag_move_rus, padez_rus, where_rus, 'и',
        what_rus, ne, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, hairu_desu_nanika.__name__

def hairu_desu_nanika_to():
    print('hairu_desu_nanika_to')
    where = ran(a['insides'])
    where_hir = a['insides_hir'][where]
    glag = random.choice(('答え', '聞_2', '言'))
    glag_hir = a['glagol']['address'][glag]
    glag_rus = a['glag_past_one_moment'][glag]
    if glag == '聞_2':
        glag = '聞'
    what = '何か'
    what_hir = 'なにか'
    what_rus = a['nowhere_no_one']['か']['何']
    if random.randint(0, 1) == 0:
        glag_move = '出'
        glag_move_hir = 'で'
        glag_move_rus = 'вышел'
        padez = 'を'
        padez_rus = 'из'
        where_rus = a['end_insides2'][where]
    else:
        glag_move = '入'
        glag_move_hir = 'はい'
        glag_move_rus = 'зашёл'
        padez = 'に'
        padez_rus = 'в'
        where_rus = a['end_insides4'][where]
    jap = ['彼', 'は', where, padez, glag_move, a['glag_form'][glag][6], what,
        glag, a['glag_form'][glag][2], 'ました']
    hir = ''.join(['かれ', 'は', where_hir, padez, glag_move_hir, a[
        'glag_form'][glag][6], what_hir, glag_hir, a['glag_form'][glag][2],
        'ました'])
    rus = ' '.join(['Когда он', glag_move_rus, padez_rus, where_rus, ', то',
        what_rus, glag_rus, '(сразу произошло действие)'])
    jap = ''.join(jap)
    return jap, hir, rus, hairu_desu_nanika_to.__name__


def people_walk_there():
    print('people_walk_there')
    who = ran(a['people'])
    who_hir = a['people_hir'][who]
    who_rus = a['people'][who]
    build = ran(a['buildings'])
    build_hir = a['buildings_hir'][build]
    area = random.choice(('前', '後ろ', '右側', '左側', '隣', 'そば'))
    area_hir = a['area_hir'][area]
    area_rus = a['area'][area]
    if area == '右側' or area == '左側':
        build_rus = a['end_build'][build]
    else:
        build_rus = a['end_build5'][build]
    glag = random.choice(('休', '遊', '散歩', '話'))
    glag_rus_dict = {'休': 'отдыхают', '遊': 'играют', '散歩': 'гуляют', '話':
        'разговаривают'}
    glag_rus = glag_rus_dict[glag]
    for i in a['glagol']:
        if glag in a['glagol'][i]:
            glag_hir = a['glagol'][i][glag]
    ran_adv = ran(a['adverbs']['neutral'])
    adv_hir = a['adverbs_hir']['neutral'][ran_adv]
    adv_rus = a['adverbs']['neutral'][ran_adv]
    jap = [who, 'は', build, 'の', area, 'で', ran_adv, glag, a['glag_form'][
        glag][6], 'います']
    hir = ''.join([who_hir, 'は', build_hir, 'の', area_hir, 'で', adv_hir,
        glag_hir, a['glag_form'][glag][6], 'います'])
    rus = ' '.join([who_rus, adv_rus, glag_rus, area_rus, build_rus])
    jap = ''.join(jap)
    return jap, hir, rus, people_walk_there.__name__


def jyouzu_heta():
    print('jyouzu_heta')
    who, hir_who, rus_who = who_f('family', 'know_people', 'suff')
    rand_can = random.choice(('上手', '下手'))
    adv, adv_rus = '', ''
    if rand_can == '上手':
        can_hir = 'じょうず'
        can_rus = 'хорош(а) в'
    else:
        can_hir = 'へた'
        can_rus = 'плох(а) в'
    glag = ran(a['can_do'])
    glag_hir = a['can_do_hir'][glag]
    glag_rus = a['end_can'][glag]
    if random.randint(0, 1) == 0:
        if rand_can == '上手':
            adv = 'もう'
            adv_rus = 'уже'
        else:
            adv = 'まだ'
            adv_rus = 'все еще'
    jap = [who, 'は', glag, 'が', adv, rand_can, 'です']
    hir = ''.join([hir_who, 'は', glag_hir, 'が', adv, can_hir, 'です'])
    rus = ' '.join([rus_who, adv_rus, can_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, jyouzu_heta.__name__


def to_meeting_go_with_friends():
    print('to_meeting_go_with_friends')
    t = Times('glag_budush')
    time_jap, time_hir, time_rus = t.main()
    event = ran(a['events'])
    ev_hir = a['events_hir'][event]
    ev_rus = a['events'][event]
    numb = str(random.randint(2, 6))
    where = ran(a['buildings'])
    where_hir = a['buildings_hir'][where]
    where_rus = a['end_build4'][where]
    jap_num = a['numbers'][numb]
    hir_numb = a['numbers_hir'][numb]
    rus_numb = a['numbers_rus'][numb]
    if numb == '2':
        nin = ''
    else:
        nin = 'にん'
    jap = [time_jap, where, 'で', event, 'が', 'あります。私たちは', jap_num, '人でそこへ行きます']
    hir = ''.join([time_hir, where_hir, 'で', ev_hir, 'が', 'あります。わたしたちは',
        hir_numb, nin, 'で', 'そこへいきます'])
    rus = ' '.join([time_rus, 'в', where_rus, 'будет', ev_rus,
        '. Мы пойдем туда', rus_numb])
    jap = ''.join(jap)
    return jap, hir, rus, to_meeting_go_with_friends.__name__


def two_actions_de_form():
    print('two_actions_de_form')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    glag = ran(a['glagol']['not_trans_fast_men'])
    glag_hir = a['glagol']['not_trans_fast_men'][glag]
    glag_rus = a['glag_nast_post'][glag]
    glag_betw = ran(a['glagol']['hygiene'])
    glag_betw_hir = a['glagol']['hygiene'][glag_betw]
    glag_betw_rus = a['glag_nast_post'][glag_betw]
    if glag_betw in a['glag_accusative']:
        glag_betw_acc = ran(a['glag_accusative'][glag_betw])
        glag_betw_acc_hir = a['glag_accusative_hir'][glag_betw][glag_betw_acc]
        glag_betw_acc_rus = a['glag_accusative'][glag_betw][glag_betw_acc]
    else:
        glag_betw_acc, glag_betw_acc_hir, glag_betw_acc_rus = '', '', ''
    glag_slow = ran(a['glagol']['not_trans_slow'])
    glag_slow_hir = a['glagol']['not_trans_slow'][glag_slow]
    glag_slow_rus = a['glag_nast_post'][glag_slow]
    time_jap2, time_hir2, time_rus2 = '', '', ''
    t = Times('choose', ['ho'])
    time_jap, time_hir, time_rus = t.main()
    if glag_betw == '走':
        inst = '公園で'
        inst_hir = 'こうえんで'
        inst_rus = 'в парке'
    elif glag_betw == 'たいそう':
        inst = '外で'
        inst_hir = 'そとで'
        inst_rus = 'снаружи дома'
    else:
        inst, inst_hir, inst_rus = '', '', ''
    if glag == '起':
        jap = [jap_podl, 'は', '毎日', time_jap, glag, a['glag_form'][glag][6],
            '、', inst, glag_betw_acc, 'を', glag_betw, a['glag_form'][
            glag_betw][6], '、', glag_slow, a['glag_form'][glag_slow][6], 'います']
        hir = ''.join([jap_podl_hir, 'は', 'まいにち', time_hir, glag_hir, a[
            'glag_form'][glag][6], '、', inst_hir, glag_betw_acc_hir, 'を',
            glag_betw_hir, a['glag_form'][glag_betw][6], '、', glag_slow_hir,
            a['glag_form'][glag_slow][6], 'います'])
        rus = ' '.join([jap_podl_rus, 'каждый день', time_rus, glag_rus,
            ',', glag_betw_rus, inst_rus, glag_betw_acc_rus, ', а затем',
            glag_slow_rus])
    else:
        t2 = Times('choose', ['kan'])
        time_jap2, time_hir2, time_rus2 = t2.main()
        jap = [jap_podl, 'は', '毎日', time_jap2, glag_slow, a['glag_form'][
            glag_slow][6], '、', inst, glag_betw_acc, 'を', glag_betw, a[
            'glag_form'][glag_betw][6], '、', time_jap, glag, a['glag_form']
            [glag][2], 'ます']
        hir = ''.join([jap_podl_hir, 'はまいにち', time_hir2, glag_slow_hir, a[
            'glag_form'][glag_slow][6], '、', inst_hir, glag_betw_acc_hir,
            'を', glag_betw_hir, a['glag_form'][glag_betw][6], '、', time_hir,
            glag_hir, a['glag_form'][glag][2], 'ます'])
        rus = ' '.join([jap_podl_rus, 'каждый день', time_rus2,
            glag_slow_rus, ',', glag_betw_rus, inst_rus, glag_betw_acc_rus,
            ', а затем', time_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, two_actions_de_form.__name__


def kara_made():
    print('kara_made')
    where1 = ran(a['buildings'])
    where2 = ran(a['buildings'])
    where1_hir = a['buildings_hir'][where1]
    where2_hir = a['buildings_hir'][where2]
    where1_rus = a['end_build'][where1]
    minutes = str(random.choice((5, 10, 15, 20, 25, 30, 35, 40, 45, 50)))
    min_hir = a['minutes_hir'][minutes]
    adverb = ran(a['adverbs']['person'])
    adverb_hir = a['adverbs_hir']['person'][adverb]
    adv_rus = a['adverbs']['person'][adverb]
    if random.randint(0, 1) == 0:
        where2_rus = a['end_build'][where2]
        jap = ['私', 'は', adverb, where1, 'から', where2, 'まで', minutes, '分で行きます']
        hir = ''.join(['わたし', 'は', adverb_hir, where1_hir, 'から', where2_hir,
            'まで', min_hir, 'でいきます'])
        rus = ' '.join([adv_rus, 'я прохожу от', where1_rus, 'до',
            where2_rus, 'за', minutes, 'минут'])
    else:
        where2_rus = a['end_build2'][where2]
        jap = ['私', 'は', minutes, '分後', 'に', where2, 'に', '行きます']
        hir = ''.join(['わたし', 'は', min_hir, 'あと', 'に', where2_hir, 'に', 'いきます']
            )
        rus = ' '.join(['я приду в', where2_rus, 'через', minutes, 'минут'])
    jap = ''.join(jap)
    return jap, hir, rus, kara_made.__name__


def masyou_after_event():
    print('masyou_after_event')
    glag = random.choice(('買', '見'))
    glag_begin = ran(a['glagol']['not_trans_fast_ev'])
    glag_begin_hir = a['glagol']['not_trans_fast_ev'][glag_begin]
    glag_begin_rus = a['glag_budush'][glag_begin]
    eve_jap, eve_hir, eve_rus = event_f()
    glag_hir = a['glagol']['accusative'][glag]
    predmet = ran(a['glag_accusative'][glag])
    predmet_hir = a['glag_accusative_hir'][glag][predmet]
    predmet_rus = a['glag_accusative'][glag][predmet]
    copula = 'ませんか'
    prim = (
        ' (прим. Говорящий НЕ знает, намерен ли собеседник выполнить действие)'
        )
    jap = [eve_jap, 'が', glag_begin, a['glag_form'][glag_begin][6], 'から、',
        predmet, 'を', glag, a['glag_form'][glag][2], copula]
    hir = ''.join([eve_hir, 'が', glag_begin_hir, a['glag_form'][glag_begin]
        [6], 'から、', predmet_hir, 'を', glag_hir, a['glag_form'][glag][2],
        copula])
    rus = ' '.join(['После того как', glag_begin_rus, eve_rus, ', давай', a
        ['glag_masyou'][glag], predmet_rus, '?', prim])
    jap = ''.join(jap)
    return jap, hir, rus, masyou_after_event.__name__


def after_action_will_address():
    print('after_action_will_address')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('end_family2', 'end_know2',
        'suff')
    glag_jap = ran(a['glagol']['address'])
    glag_hir = a['glagol']['address'][glag_jap]
    glag_rus = a['glag_im_going_todo'][glag_jap]
    glag_jap2 = ran(a['glagol']['not_trans_slow'])
    glag_hir2 = a['glagol']['not_trans_slow'][glag_jap2]
    glag_rus2 = a['glag_verb_stem'][glag_jap2]
    if glag_jap == '聞_1' or glag_jap == '聞_2':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][2]
    jap = ['私', 'は', glag_jap2, a['glag_form'][glag_jap2][2], '終わってから、',
        jap_podl, 'に', glag_jap, form, 'ます']
    hir = ''.join(['わたし', 'は', glag_hir2, a['glag_form'][glag_jap2][2],
        'おわってから、', jap_podl_hir, 'に', glag_hir, form, 'ます'])
    rus = ' '.join(['После того, как я закончу', glag_rus2, ', ', glag_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, after_action_will_address.__name__


def kudasai():
    print('kudasai')
    rand = random.randint(0, 1)
    if rand == 0:
        glag_jp, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
            choose_glag_accus('glag_kudasai'))
    else:
        glag_jp, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
            choose_glag_accus('glag_kudasai_rude'))
    if rand == 0:
        form = a['glag_form'][glag_jp][6]
        rus_expl = ', пожалуйста,'
        copula = 'ください'
    else:
        copula = ''
        rus_expl = '(грубая форма, между близкими или от родителей детям)'
        form = a['glag_form'][glag_jp][4]
    if glag_jp == 'かり':
        glag_rus = 'одолжите в займы'
    jap = [accus, 'を', glag_jp, form, copula]
    hir = ''.join([accus_hir, 'を', glag_hir, form, copula])
    rus = ' '.join([glag_rus, accus_rus, rus_expl])
    jap = ''.join(jap)
    return jap, hir, rus, kudasai.__name__


def kudasai_number():
    print('kudasai_number')
    suff = random.choice(list(suff_numbs.keys()))
    obj = ran(suff_numbs[suff]['words'])
    rand_num = ran(b1['kanji_numerical'])
    obj_hir = suff_numbs[suff]['read_words'][obj]
    obj_rus_numb = b1['rus_num'][rand_num]
    if rand_num == '1':
        end_rus = suff_numbs[suff]['words'][obj]
    elif int(rand_num) >= 2 and int(rand_num) <= 4:
        end_rus = suff_numbs[suff]['ending_1'][obj]
    else:
        end_rus = suff_numbs[suff]['ending_2'][obj]
    jap = [obj, 'を', rand_num, suff, 'ください']
    read = suff_numbs[suff]['read'][rand_num]
    hir = ''.join([obj_hir, 'を', read, 'ください'])
    rus = ' '.join(['дате пожалуйста,', obj_rus_numb, end_rus])
    jap = ''.join(jap)
    return jap, hir, rus, kudasai_number.__name__


def prop_noadj_adverbs():
    uno = ran(a['uno'])
    uno_rus = a['uno'][uno]
    where = ran(a['buildings'])
    where_hir = a['buildings_hir'][where]
    where_rus = a['buildings'][where]
    if random.randint(0, 1) == 0:
        adverb = ran(a['adverbs']['negativ'])
        adverb_rus = a['adverbs']['negativ'][adverb]
        copula = 'ではありません'
    else:
        adverb = ran(a['adverbs']['negativ2'])
        adverb_rus = a['adverbs']['negativ2'][adverb]
        copula = 'です'
    prop = ran(a['adj_non_predicative_hir'])
    prop_hir = a['adj_non_predicative_hir'][prop]
    prop_rus = a['adj_non_predicative_rus'][prop]
    jap = [uno, where, 'は', adverb, prop, copula]
    hir = ''.join([uno, where_hir, 'は', adverb, prop_hir, copula])
    rus = ' '.join([uno_rus, where_rus, adverb_rus, prop_rus])
    jap = ''.join(jap)
    return jap, hir, rus, prop_noadj_adverbs.__name__


def naru_senmon():
    print('naru_senmon')
    proff = random.choice(('先生', '教授', '中学校の教師', '大学生'))
    proff_hir = a['profession_hir'][proff]
    proff_rus = a['end_proffesion'][proff]
    mounth = ran(a['mounths'])
    mounth_hir = a['mounths_hir'][mounth]
    mounth_rus = a['end_mounths'][mounth]
    sen = ran(a['senmon'])
    sen_hir = a['senmon_hir'][sen]
    sen_rus = a['senmon'][sen]
    jap = ['私', 'は', mounth, 'に', proff, 'に', 'なりました。専門は', sen, 'です']
    hir = ''.join(['わたし', 'は', mounth_hir, 'に', proff_hir, 'に',
        'なりました。せんもんは', sen_hir, 'です'])
    rus = ' '.join(['Я', mounth_rus, 'стал(а)', proff_rus,
        '. Моя специальность-', sen_rus])
    jap = ''.join(jap)
    return jap, hir, rus, naru_senmon.__name__


def reason_sorede():
    print('reason_sorede')
    eve = ran(a['events'])
    eve_hir = a['events_hir'][eve]
    eve_rus = a['end_events2'][eve]
    reas = ran(a['reasons'])
    reas_hir = a['reasons_hir'][reas]
    reas_rus = a['reasons'][reas]
    jap = [reas, '。それ', 'で、私', 'は', eve, 'に行きませんでした']
    hir = ''.join([reas_hir, '。それ', 'で、', 'わたし', 'は', eve_hir, 'に', 'いきませんでした']
        )
    rus = ' '.join([reas_rus, '. Поэтому я не ходил в(на)', eve_rus,
        '(второе предложение объясняет следствие, вытекающее из сообщения, сделанного в предыдущем предложении)'
        ])
    jap = ''.join(jap)
    return jap, hir, rus, reason_sorede.__name__


def naru_prop_and_like_it():
    print('naru_prop_and_like_it')
    where = ran(a['buildings'])
    where_hir = a['buildings_hir'][where]
    where_rus = a['end_build4'][where]
    if random.randint(0, 1) == 0:
        prop = ran(a['adj_non_predicative_hir'])
        prop_hir = a['adj_non_predicative_hir'][prop]
        prop_rus = a['adj_non_predicative_endings'][prop]
        padez = 'に'
    else:
        prop = ran(a['adj_for_small_object2'])
        prop_hir = a['adj_for_small_object2_hir'][prop]
        prop_rus = a['adj_for_small_endings3'][prop]
        padez = 'く'
    jap = [where, 'は', prop, padez, 'なりました']
    hir = ''.join([where_hir, 'は', prop_hir, padez, 'なりました'])
    rus = ' '.join(['В ', where_rus, 'стало', prop_rus])
    jap = ''.join(jap)
    return jap, hir, rus, naru_prop_and_like_it.__name__


def reason_kara():
    print('reason_kara')
    eve = random.choice(('見物', '散歩', 'コンサート', 'パーティ', 'お祭り', 'お花見'))
    eve_hir = a['events_hir'][eve]
    eve_rus = a['end_events2'][eve]
    build = random.choice(('公園', '喫茶店', '博物館', '寺', '動物園'))
    build_hir = a['buildings_hir'][build]
    build_rus = a['buildings'][build]
    reas = ran(a['reasons_pos'])
    reas_hir = a['reasons_pos_hir'][reas]
    reas_rus = a['reasons_pos'][reas]
    jap = [reas, 'から、私', 'は', eve, 'とか', build, 'に', '行きます']
    hir = ''.join([reas_hir, 'から、わたし', 'は', eve_hir, 'とか', build_hir, 'に',
        'いきます'])
    rus = ' '.join(['Так как', reas_rus, ', ', 'я пойду в(на)', eve_rus,
        'или в', build_rus,
        '(личная причина, по своему мнению, акцент на то том что пошел на событие)'
        ])
    jap = ''.join(jap)
    return jap, hir, rus, reason_kara.__name__


def he_can():
    print('he_can_')
    podl = random.choice(('彼', '彼女'))
    podl_hir = a['me_and_them_hir'][podl]
    podl_rus = a['me_and_them'][podl]
    lang = ran(a['languages'])
    lang_hir = a['languages_hir'][lang]
    lang_rus = a['end_lang'][lang]
    glag = random.choice(('答え', '聞_2', '話'))
    for i in a['glagol']:
        if glag in a['glagol'][i]:
            glag_hir = a['glagol'][i][glag]
    glag_rus = a['glag_verb_stem'][glag]
    if glag == '聞_1' or glag == '聞_2':
        glag = '聞'
    form = a['glag_form'][glag][3]
    work = ran(a['at_work'])
    work_hir = a['at_work_hir'][work]
    work_rus = a['at_work'][work]
    but_list = {'しかし': 'однако,', 'でも': 'но,'}
    if work == '間違っている' or work == '言葉を忘れている':
        but = random.choice(('しかし', 'でも'))
        but_hir = 'but'
        but_rus = but_list[but]
        dop_jap = random.choice(('ふだん', '時々', 'よく'))
        dop_hir = dop_jap
        dop_rus = a['adverbs']['person'][dop_jap]
    else:
        dop_jap, dop_hir, dop_rus = dop_time('person')
        but = ran(a['time_at'])
        but_hir = a['time_at_hir'][but]
        but_rus = a['time_at'][but]
    jap = [podl, 'は', lang, 'で', glag, form, 'ことができる。', but, dop_jap, work]
    hir = ''.join([podl_hir, 'は', lang_hir, 'で', glag_hir, form, 'ことができる。',
        but_hir, dop_hir, work_hir])
    rus = ' '.join([podl_rus, 'умеет', glag_rus, lang_rus, '.', but_rus,
        dop_rus, work_rus])
    jap = ''.join(jap)
    return jap, hir, rus, he_can.__name__


def he_mistake():
    print('he_mistake')
    podl = random.choice(('彼', '彼女'))
    podl_hir = a['me_and_them_hir'][podl]
    podl_rus = a['me_and_them'][podl]
    work = ran(a['at_work'])
    work_hir = a['at_work_hir'][work]
    work_rus = a['at_work'][work]
    if work == '間違っている' or work == '言葉を忘れている':
        dop_jap = random.choice(('ふだん', '時々', 'よく'))
        dop_hir = dop_jap
        dop_rus = a['adverbs']['person'][dop_jap]
    else:
        dop_jap, dop_hir, dop_rus = dop_time('person')
    jap = [podl, 'は', dop_jap, work]
    hir = ''.join([podl_hir, 'は', dop_hir, work_hir])
    rus = ' '.join([podl_rus, dop_rus, work_rus])
    jap = ''.join(jap)
    return jap, hir, rus, he_mistake.__name__


def this_man_tell_about():
    print('this_man_tell_about')
    name = ran(a['names'])
    rus_who = a['names'][name]
    hir_who = a['names_hir'][name]
    char = ran(a['character'])
    char_hir = a['character_hir'][char]
    char_rus = a['character'][char]
    about = ran(a['telling'])
    about_hir = a['telling_hir'][about]
    about_rus = a['end_telling'][about]
    jap = ['あの方', 'は', name, '先生です。彼', 'は', 'とても', char, 'です。学生たち', 'に',
        about, 'について', '話す', 'のが', '好きです']
    hir = ''.join(['あのかた', 'は', hir_who, 'せんせいです。かれ', 'は', 'とても', char_hir,
        'です。がくせいたち', 'に', about_hir, 'について', 'はなす', 'のが', 'すきです'])
    rus = ' '.join(['Это преподаватель', rus_who, '. Он очень', char_rus,
        '. Он любит рассказывать (обобщенно, НЕ личная история) ученикам',
        about_rus])
    jap = ''.join(jap)
    return jap, hir, rus, this_man_tell_about.__name__


def he_talking_about_how():
    print('he_talking_about_how')
    jap_podl, jap_podl_hir, jap_podl_rus = event_f()
    jap_podl_rus = a['end_events3'][jap_podl]
    t = Times('glag_past_one_moment')
    time_jap, time_hir, time_rus = t.main()
    jap = [time_jap, '彼', 'は', 'みんな', 'に', jap_podl, 'のこと', 'を', '話しました']
    hir = ''.join([time_hir, 'かれ', 'は', 'みんな', 'に', jap_podl_hir, 'のこと',
        'を', 'はなしました'])
    rus = ' '.join([time_rus,
        'он рассказал (личная история, детальная) всем о ', jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, he_talking_about_how.__name__


def i_want():
    print('i_want')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][2]
    rand_time = random.choice(('da_p', 'da_f'))
    t = Times('choose', [rand_time])
    if rand_time == 'da_p':
        copula = 'たかったです'
        cop_rus = 'хотел'
    else:
        copula = 'たいです'
        cop_rus = 'хочу'
    time_jap, time_hir, time_rus = t.main()
    jap = [time_jap, 'に', jap_podl, padez, glag_jap, form, copula]
    hir = ''.join([time_hir, 'に', jap_podl_hir, padez, glag_hir, form, copula])
    rus = ' '.join([time_rus, cop_rus, padez_rus, jap_podl_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, i_want.__name__


def all_demo():
    print('all_demo')
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    rand_glag = random.choice(('move', 'not_trans_slow', 'accusative',
        'address'))
    glag = ran(a['glagol'][rand_glag])
    glag_hir = a['glagol'][rand_glag][glag]
    glag_rus = a['glag_nast_post'][glag]
    if rand_glag == 'not_trans_slow':
        jap_podl = 'どこででも'
        jap_podl_hir = 'どこででも'
        jap_podl_rus = 'везде (всюду)'
    elif rand_glag == 'accusative':
        jap_podl = '何でも'
        jap_podl_hir = 'なんでも'
        jap_podl_rus = 'всё'
    elif rand_glag == 'address':
        jap_podl = 'だれでも'
        jap_podl_hir = 'だれにでも'
        jap_podl_rus = 'со всеми (всем)'
    else:
        events = ran(a['events'])
        events_hir = a['events_hir'][events]
        events_rus = a['end_events'][events]
        events = 'どの' + events
        events_hir = 'どの' + events_hir
        jap_podl = events + 'でも'
        jap_podl_hir = events_hir + 'でも'
        jap_podl_rus = 'на все ' + events_rus
    if glag == '聞_2' or glag == '聞_1':
        glag = '聞'
    form = a['glag_form'][glag][2]
    jap = [jap_who, 'は', jap_podl, glag, form, 'ます']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, glag_hir, form, 'ます'])
    rus = ' '.join([rus_podl_who, jap_podl_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, all_demo.__name__

def all_demo_janai():
    print('all_demo_janai')
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    rand_glag = random.choice(('move', 'not_trans_slow', 'accusative',
        'address'))
    glag = ran(a['glagol'][rand_glag])
    glag_hir = a['glagol'][rand_glag][glag]
    glag_rus = a['glag_nast_post'][glag]
    if rand_glag == 'not_trans_slow':
        jap_podl = 'どこでも'
        jap_podl_hir = 'どこでも'
        jap_podl_rus = 'нигде не'
    elif rand_glag == 'accusative':
        jap_podl = '何も'
        jap_podl_hir = 'なんも'
        jap_podl_rus = 'ничего не'
    elif rand_glag == 'address':
        jap_podl = 'だれも'
        jap_podl_hir = 'だれにも'
        jap_podl_rus = 'ни с кем не'
    else:
        events = ran(a['events'])
        events_hir = a['events_hir'][events]
        events_rus = a['end_events'][events]
        events = 'どの' + events
        events_hir = 'どの' + events_hir
        jap_podl = events + 'も'
        jap_podl_hir = events_hir + 'も'
        jap_podl_rus = 'на все ' + events_rus + ' не '
    if glag == '聞_2' or glag == '聞_1':
        glag = '聞'
    form = a['glag_form'][glag][2]
    jap = [jap_who, 'は', jap_podl, glag, form, 'ません']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, glag_hir, form, 'ません'])
    rus = ' '.join([rus_podl_who, jap_podl_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, all_demo_janai.__name__


def put_kudasai():
    print('put_kudasai')
    furnit = random.choice(('はこ', '料理', 'れいぞころ'))
    if furnit == 'はこ':
        accus = ran(a['small object'])
        accus_hir = a['small object_hir'][accus]
        accus_rus = a['small object'][accus]
    elif furnit == '料理':
        accus = random.choice(('しお', 'さとう'))
        accus_list = {'しお': 'соль', 'さとう': 'сахар'}
        accus_hir = accus
        accus_rus = accus_list[accus]
    else:
        accus = random.choice(('ぎゅうにく', 'ぶたにく', 'とりにく'))
        accus_list = {'ぎゅうにく': 'говядину', 'ぶたにく': 'свинину', 'とりにく': 'курицу'}
        accus_hir = accus
        accus_rus = accus_list[accus]
    furnit_list = {'はこ': 'короб', '料理': 'блюдо', 'れいぞころ': 'холодильник'}
    furnit_rus = furnit_list[furnit]
    question = ''
    pref = ''
    rand = random.randint(0, 3)
    if rand == 0:
        kudasai = 'ください'
        form = 'て'
        kudasai_rus = 'Положите, пожалуйста,'
    elif rand == 1:
        kudasai = 'くださいませんか'
        form = 'て'
        kudasai_rus = (
            'Положите, пожалуйста (самая вежливая форма, приносишь неудобства)'
            )
        question = '?'
    elif rand == 2:
        kudasai = 'ください'
        form = ''
        pref = 'お'
        kudasai_rus = (
            'Положите, пожалуйста (очень вежливо, но не самая при самая вежливая форма),'
            )
    else:
        kudasai = 'なさい'
        form = ''
        kudasai_rus = 'Положи'
        pref = 'お'
    jap = [accus, 'を', furnit, 'に', pref, '入れ', form, kudasai]
    hir = ''.join([accus_hir, 'を', furnit, 'に', pref, 'いれ', form, kudasai])
    rus = ' '.join([kudasai_rus, accus_rus, 'в', furnit_rus, question])
    jap = ''.join(jap)
    return jap, hir, rus, put_kudasai.__name__


def probability_low_and_notlow():
    print('probability_low_and_notlow')
    g = Glagols('glag_nast_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    form = a['glag_form'][glag_jap][3]
    rand_for_time = random.choice(['ho', 'now', 'kan'])
    t = Times('choose', [rand_for_time])
    time_jap, time_hir, time_rus = t.main()
    if rand_for_time == 'ho':
        ni = 'から'
        ni_rus = 'c'
        time_rus = time_rus[2:]
    else:
        ni = ''
        ni_rus = ''
    if random.randint(0, 1):
        copula = 'でしょう'
        cop_rus = 'наверное (средняя вероятность)'
    else:
        copula = 'かもしれません'
        cop_rus = 'может быть (маленькая вероятность)'
    jap = [jap_who, 'は', time_jap, ni, jap_podl, padez, glag_jap, form, copula]
    hir = ''.join([hir_podl_who, 'は', time_hir, ni, jap_podl_hir, padez,
        glag_hir, form, copula])
    rus = ' '.join([rus_podl_who, cop_rus, ni_rus, time_rus, padez_rus,
        jap_podl_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, probability_low_and_notlow.__name__


def he_or_event_doing_and_continue():
    print('he_or_event_doing_and_continue')
    if random.randint(0, 1) == 0:
        eve_jap, eve_hir, eve_rus = event_f()
        mou = 'もう'
        mou_rus = 'уже'
        jap = [eve_jap, 'は', mou, '始めています']
        hir = ''.join([eve_hir, 'は', mou, 'はじめています'])
        rus = ' '.join([eve_rus, mou_rus, 'началось(лся)'])
    else:
        (glag_jap_origin, jap_podl, jap_podl_hir, jap_podl_rus, glag_jap,
            glag_hir, glag_rus) = choose_glag_napravl('glag_past_one_moment')
        form = a['glag_form'][glag_jap_origin][6]
        build = ran(a['buildings'])
        build_hir = a['buildings_hir'][build]
        build_rus = a['end_build2'][build]
        jap = [jap_podl, 'は', build, 'に', glag_jap, form, 'います']
        hir = ''.join([jap_podl_hir, 'は', build_hir, 'に', glag_hir, form,
            'います'])
        rus = ' '.join([jap_podl_rus, 'в', build_rus, glag_rus,
            '(и там остается)'])
    jap = ''.join(jap)
    return jap, hir, rus, he_or_event_doing_and_continue.__name__


def condition():
    print('condition')
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    if random.randint(0, 1) == 0:
        glag_jap = random.choice(('疲れて', '忙しくて', 'よごれて', 'ふとって', '年をとって'))
        glag_list = {'疲れて': ['つかれて', 'устал(а)'], '忙しくて': ['いそがしくて',
            'занят(а)'], 'よごれて': ['よごれて', 'грязный'], 'ふとって': ['ふとって',
            'толстый'], '年をとって': ['ねんをとって', 'пожилой']}
        glag_hir = glag_list[glag_jap][0]
        glag_rus = glag_list[glag_jap][1]
        adverb = random.choice(('もう', 'とても'))
        adverb_list = {'もう': 'уже', 'とても': 'очень'}
        adverb_rus = adverb_list[adverb]
        jap = [jap_podl, 'は', adverb, glag_jap, 'います']
        hir = ''.join([jap_podl_hir, 'は', adverb, glag_hir, 'います'])
        rus = ' '.join([jap_podl_rus, adverb_rus, glag_rus])
    else:
        glag_jap = random.choice(('おぼえて', 'してい'))
        glag_list = {'おぼえて': ['おぼえて', 'помнит'], 'してい': ['してい', 'знает']}
        glag_hir = glag_list[glag_jap][0]
        glag_rus = glag_list[glag_jap][1]
        event = ran(a['events'])
        event_hir = a['events_hir'][event]
        event_rus = a['end_events3'][event]
        jap = [jap_podl, 'は', event, 'を', glag_jap, 'います']
        hir = ''.join([jap_podl_hir, 'は', event_hir, 'を', glag_hir, 'います'])
        rus = ' '.join([jap_podl_rus, glag_rus, 'о', event_rus])
    jap = ''.join(jap)
    return jap, hir, rus, condition.__name__


def kureru_help():
    print('kureru_help')
    who, hir_who, rus_who = who_f('family', 'know_people', 'no')
    sen, sen_hir, sen_rus = '', '', ''
    glag = 'くれ'
    if who in a['names']:
        if random.randint(0, 1) == 0:
            sen = '先生'
            sen_hir = 'せんせい'
            sen_rus = '-сенсей'
            glag = 'ください'
        else:
            who = who + 'くん'
            hir_who = hir_who + 'くん'
            rus_who = rus_who + '-кун'
    if random.randint(0, 1):
        glag_jp = random.choice(('てつだって', 'おくいて'))
        glag_List = {'てつだって': ['てつだって', 'помог(ла)'], 'おくいて': ['おくいて',
            'проводил(ла)']}
        who2, hir_who2, rus_who2 = who_f('end_family', 'end_know', 'suff_no')
        if who2[:2] in a['names']:
            who2 = '私'
            hir_who2 = 'わたし'
            rus_who2 = 'мне'
        else:
            rus_who2 = rus_who2 + '(близкий мне человек)'
        glag_hir = glag_List[glag_jp][0]
        glag_rus = glag_List[glag_jp][1]
        if glag_jp == 'おくいて':
            build = ran(a['buildings'])
            build_hir = a['buildings_hir'][build]
            build_rus = a['end_build'][build]
            padez = 'まで'
            padez_rus = 'до'
        else:
            build, build_hir, build_rus, padez, padez_rus = ['', '', '', '', ''
                ]
        jap = [who, sen, 'は', build, padez, who2, 'を', glag_jp, glag, 'ました']
        hir = ''.join([hir_who, sen_hir, 'は', build_hir, padez, hir_who2,
            'を', glag_hir, glag, 'ました'])
        rus = ' '.join([rus_who, sen_rus, glag_rus, padez_rus, build_rus,
            rus_who2])
    else:
        glag_jp = 'なおして'
        glag_hir = 'なおして'
        glag_rus = 'починил(а)'
        obj = ran(a['small object'])
        obj_hir = a['small object_hir'][obj]
        obj_rus = a['end_small_address'][obj]
        who2, hir_who2, rus_who2 = who_f('end_family4', 'end_know4', 'suff_no')
        if who2[:2] in a['names']:
            who2 = '私'
            hir_who2 = 'わたし'
            rus_who2 = 'мне'
        else:
            rus_who2 = rus_who2 + '(близкий мне человек)'
        jap = [who, sen, 'は', who2, 'の', obj, 'を', glag_jp, glag, 'ました']
        hir = ''.join([hir_who, sen_hir, 'は', hir_who2, 'の', obj_hir, 'を',
            glag_hir, glag, 'ました'])
        rus = ' '.join([rus_who, sen_rus, glag_rus, obj_rus, rus_who2])
    jap = ''.join(jap)
    return jap, hir, rus, kureru_help.__name__


def reason_de():
    print('reason_de')
    eve = ran(a['events'])
    eve_hir = a['events_hir'][eve]
    eve_rus = a['end_events2'][eve]
    reas = ran(a['reason_noun'])
    reas_hir = a['reason_noun_hir'][reas]
    reas_rus = a['reason_noun'][reas]
    jap = ['私', 'は', reas, 'で', eve, 'に行きませんでした']
    hir = ''.join(['わたし', 'は', reas_hir, 'で', eve_hir, 'に', 'いきませんでした'])
    rus = ' '.join(['Из-за', reas_rus, 'я не ходил в(на)', eve_rus,
        '(сильный акцент на причине)'])
    jap = ''.join(jap)
    return jap, hir, rus, reason_de.__name__


def comparison_1():
    print('comparison_1')
    obj1, obj2 = random.sample(list(a['small object'].keys()), k=2)
    obj_hir1 = a['small object_hir'][obj1]
    obj_hir2 = a['small object_hir'][obj2]
    obj1_rus = a['small object'][obj1]
    obj2_rus = a['small object'][obj2]
    jap_prop, prop_hir, prop_rus, jap_ne, jap_ne_hir, jap_ne_rus = (
        prop_no_sush(obj1, 'only_sush', 'only_pos'))
    rand = random.randint(0, 3)
    if rand == 0:
        jap = [obj1, 'は', obj2, 'より', jap_prop, jap_ne, 'です']
        hir = ''.join([obj_hir1, 'は', obj_hir2, 'より', prop_hir, jap_ne_hir,
            'です'])
        rus = ' '.join([obj1_rus, 'более ', prop_rus, 'чем', obj2_rus])
    elif rand == 1:
        jap = [obj2, 'より', obj1, 'の方が', jap_prop, jap_ne, 'です']
        hir = ''.join([obj_hir2, 'より', obj_hir1, 'の方が', prop_hir,
            jap_ne_hir, 'です'])
        rus = ' '.join(['По сравнению с', obj2_rus, ',', obj1_rus, 'более ',
            prop_rus])
    elif rand == 2:
        jap = [obj2, 'より', jap_prop, jap_ne, 'です']
        hir = ''.join([obj_hir2, 'より', prop_hir, jap_ne_hir, 'です'])
        rus = ' '.join(['Более ', prop_rus, 'чем', obj2_rus])
    else:
        jap = [obj1, 'の方が', jap_prop, jap_ne, 'です']
        hir = ''.join([obj_hir1, 'の方が', prop_hir, jap_ne_hir, 'です'])
        rus = ' '.join([obj1_rus, 'более ', prop_rus])
    jap = ''.join(jap)
    return jap, hir, rus, comparison_1.__name__


def he_have():
    print('he_have_and_i_want')
    who, hir_who, rus_who = who_f('end_family4', 'end_know4', 'suff')
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['small object'][obj]
    citiy = ran(a['cities'])
    citiy_hir = a['cities_hir'][citiy]
    city_rus = a['cities'][citiy]
    if obj in a['adj_for_small_object']:
        jap_prop = ran(a['adj_for_small_object'][obj])
        hir_prop = a['adj_for_small_object_hir'][obj][jap_prop]
        rus_prop = a['adj_for_small_object'][obj][jap_prop]
        if jap_prop in a['pril_with_no']:
            ok_jap = 'いい' + jap_prop + 'の'
            ok_hir = 'いい' + hir_prop + 'の'
            rus_prop = 'лучший (ая)' + rus_prop
        elif jap_prop in a['adj_non_predicative']:
            ok_jap = jap_prop + 'な'
            ok_hir = hir_prop + 'な'
        else:
            ok_jap = jap_prop + 'い'
            ok_hir = hir_prop + 'い'
    else:
        jap_prop, hir_prop, rus_prop = '', '', ''
        ok_jap = ''
        ok_hir = ''
    if random.randint(0, 1) == 0:
        jap = [who, 'は', 'いちばん', ok_jap, obj, 'が', 'あります。これ', 'は', citiy,
            '店', 'と', '同じくらい', ok_jap]
        hir = ''.join([hir_who, 'は', 'いちばん', ok_hir, obj_hir, 'が',
            'あります。これ', 'は', citiy_hir, 'みせ', 'と', 'おなじくらい', ok_hir])
        rus = ' '.join(['У', rus_who, 'есть', 'самый (ая)', rus_prop,
            obj_rus, '. Он такой же', rus_prop, 'как в магазине', city_rus])
    else:
        jap = [who, 'は', 'いちばん', ok_jap, obj, 'が', 'あります。これ', 'は', citiy,
            '店', 'ほど', ok_jap, 'くない']
        hir = ''.join([hir_who, 'は', 'いちばん', ok_hir, obj_hir, 'が',
            'あります。これ', 'は', citiy_hir, 'みせ', 'ほど', ok_jap, 'くない'])
        rus = ' '.join(['У', rus_who, 'есть', 'самый (ая)', rus_prop,
            obj_rus, '. Он не такой', rus_prop, 'как в магазине', city_rus])
    jap = ''.join(jap)
    return jap, hir, rus, he_have.__name__


def comparison_2():
    print('comparison_2')
    obj1, obj2 = random.sample(list(a['small object'].keys()), k=2)
    obj_hir1 = a['small object_hir'][obj1]
    obj_hir2 = a['small object_hir'][obj2]
    obj1_rus = a['small object'][obj1]
    obj2_rus = a['small object'][obj2]
    jap_prop, prop_hir, prop_rus, jap_ne, jap_ne_hir, jap_ne_rus = (
        prop_no_sush(obj1, 'only_sush', 'only_pos'))
    rand = random.randint(0, 3)
    if rand == 0:
        copula = 'では'
    elif rand == 1:
        copula = 'で'
    elif rand == 2:
        copula = 'は'
    else:
        copula = '、'
    jap = [obj1, 'と', obj2, 'と', copula, 'どちらが', jap_prop, jap_ne, 'ですか']
    hir = ''.join([obj_hir1, 'と', obj_hir2, 'と', copula, 'どちらが', prop_hir,
        jap_ne_hir, 'ですか'])
    rus = ' '.join(['Что более', prop_rus, '-', obj1_rus, 'или', obj2_rus, '?']
        )
    jap = ''.join(jap)
    return jap, hir, rus, comparison_2.__name__


def if_that_then_that():
    print('if_that_then_that')
    if random.randint(0, 1) == 0:
        season = ran(a['seasons'])
        season_hir = a['seasons_hir'][season]
        season_rus = a['seasons'][season]
        temp = ran(a['temperature'])
        temp_hir = a['temperature_hir'][temp]
        temp_rus = a['temperature'][temp]
        jap = [season, 'は', 'なる', 'と', temp, 'くなります']
        hir = ''.join([season_hir, 'は', 'なる', 'と', temp_hir, 'くなります'])
        rus = ' '.join(['Когда приходит', season_rus, ', то становится',
            temp_rus])
    else:
        build = ran(a['buildings'])
        build_hir = a['buildings_hir'][build]
        build_rus = a['buildings'][build]
        turn = random.choice(('まっすぐ', '右に', '左に'))
        turn_list = {'まっすぐ': ['まっすぐ', 'прямо'], '右に': ['みぎに', 'направо'],
            '左に': ['ひだりに', 'налево']}
        turn_hir = turn_list[turn][0]
        turn_rus = turn_list[turn][1]
        jap = [turn, '行く', 'と', build, 'は', 'あそこで', 'あります']
        hir = ''.join([turn_hir, 'いく', 'と', build_hir, 'は', 'あそこで', 'あります'])
        rus = ' '.join(['Если пойдете', turn_rus, ', то там будет', build_rus])
    jap = ''.join(jap)
    return jap, hir, rus, if_that_then_that.__name__


def kara_and_donoka():
    print('kara_and_donoka')
    build = ran(a['buildings'])
    build_hir = a['buildings_hir'][build]
    build_rus = a['end_build'][build]
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['small object'][obj]
    if random.randint(0,1)==0:
        doko = 'どこへも'
        doko_rus = 'никуда не'
        copula = 'ませんでした'
    else:
        doko = 'どこかへ'
        doko_rus = 'куда то'
        copula = 'ました'
    if random.randint(0,1)==0:
        nani = '何か'
        nani_rus ='какой то' 
        morau = 'もらいまして、'
        morau_rus = 'получив от'
        padez = 'を'
    else:
        nani = 'どの'
        nani_rus = 'никакого'
        morau = 'もらわずに'
        morau_rus = 'не получив от '
        padez = 'か'
    jap = ['彼', 'は', build, 'から', nani, obj, padez,morau ,doko,'行き',copula]
    hir = ''.join(['かれ', 'は', build_hir, 'から', nani, obj_hir, padez, morau,doko, 'いき',copula])
    rus = ' '.join([morau_rus, build_rus,nani_rus , obj_rus,', он',doko_rus, 'пошел'])
    jap = ''.join(jap)
    return jap, hir, rus, kara_and_donoka.__name__


def name_of_something():
    print('name_of_something')
    obj = ran(a['small object'])
    obj_hir = a['small object_hir'][obj]
    obj_rus = a['small object'][obj]
    jap = ['これ', 'は', obj, 'と', 'いいます']
    hir = ''.join(['これ', 'は', obj_hir, 'と', 'いいます'])
    rus = ' '.join(['Это называется', obj_rus])
    jap = ''.join(jap)
    return jap, hir, rus, name_of_something.__name__


def this_property_conna():
    print('this_property_conna')
    if random.randint(0, 1) == 0:
        food = ran(a['food'])
        food_hir = a['food_hir'][food]
        food_rus = a['end_food'][food]
        mest = random.choice(('こんな', 'そんな', 'あんな'))
        okon_list = {'こんな': '(близкий мне объект)', 'そんな':
            '(объект не известен собеседнику)', 'あんな':
            '(отдаленный от меня объект)'}
        okon = okon_list[mest]
        jap = [mest, food, 'は', '食べないんだ']
        hir = ''.join([mest, food_hir, 'は', 'たべないんだ'])
        rus = ' '.join(['Такой(ие)', food_rus, 'я не ем', '(эмоционально)',
            okon])
    else:
        if random.randint(0, 1) == 0:
            glag = ran(a['glagol']['not_trans_slow'])
            glag_hir = a['glagol']['not_trans_slow'][glag]
            glag_rus = a['glag_nast_post'][glag]
            form = a['glag_form'][glag][3]
            adverb = random.choice(('ふだん', 'いつも', 'よく'))
            adverb_hir = a['adverbs_hir']['person'][adverb]
            adverb_rus = a['adverbs']['person'][adverb]
            mest = random.choice(('こんな', 'そんな', 'あんな'))
            okon_list = {'こんな': '(я знаком с такой деятельностью и восхищен)',
                'そんな': '(удивлен такому уровню занятия)', 'あんな':
                '(оттенок отдаленности или незнакомости)'}
            okon = okon_list[mest]
            jap_podl, jap_podl_hir, jap_podl_rus = who_f('family',
                'know_people', 'suff')
            jap = [jap_podl, 'は', adverb, mest, 'に', glag, form, 'んです']
            hir = ''.join([jap_podl_hir, 'は', adverb_hir, mest, 'に', glag_hir,
                form, 'んです'])
            rus = ' '.join([jap_podl_rus, adverb_rus, 'так', glag_rus,
                '(эмоционально)', okon])
        else:
            obj = ran(a['small object'])
            obj_hir = a['small object_hir'][obj]
            obj_rus = a['end_small_address'][obj]
            jap_podl2, jap_podl_hir2, jap_podl_rus2 = who_f('family','know_people', 'suff')
            jap_prop, prop_hir, prop_rus, jap_ne, jap_ne_hir, jap_ne_rus = (prop_no_sush(obj, 'only_sush', 'only_pos'))
            jap = [jap_podl2,'は','こんな', 'に', jap_prop, obj, 'が','好き','んです']
            hir = ''.join([ jap_podl_hir2, 'は', 'こんな','に', prop_hir, obj_hir,'が','すき', 'んです'])
            rus = ' '.join([jap_podl_rus2, 'любит такие/ую/ой',prop_rus,obj_rus, '(эмоционально)'])

    jap = ''.join(jap)
    return jap, hir, rus, this_property_conna.__name__


def homogeneous_predicates():
    print('homogeneous_predicates')
    rand = random.randint(0, 2)
    if rand == 0:
        prof = ran(a['profession'])
        prof_hir = a['profession_hir'][prof]
        prof_rus = a['profession'][prof]
        famil = ran(a['family'])
        famil_hir = a['family_hur'][famil]
        famil_rus = a['family'][famil]
        jap = ['あの方', 'は', prof, 'で', '、私', 'の', famil, 'です']
        hir = ''.join(['あのかた', 'は', prof_hir, 'で', '、わたし', 'の', famil_hir,
            'です'])
        rus = ' '.join(['Этот человек-', prof_rus, ', моя (мой)', famil_rus])
    elif rand == 1:
        obj = ran(a['room_objects'])
        obj_hir2 = a['room_objects_hir'][obj]
        obj1_rus = a['room_objects'][obj]
        rand_prop = ran(a['adj_rooms_si'])
        prop1 = ran(a['adj_rooms_si'][rand_prop])
        prop1_hir = a['adj_rooms_si_hir'][rand_prop][prop1]
        prop1_rus = a['adj_rooms_si'][rand_prop][prop1]
        prop2 = ran(a['adj_rooms_si'][rand_prop])
        prop2_hir = a['adj_rooms_si_hir'][rand_prop][prop2]
        prop2_rus = a['adj_rooms_si'][rand_prop][prop2]
        prop1 = prop1[:-1]
        prop1_hir = prop1_hir[:-1]
        jap = ['この', '部屋', 'の', obj, 'は', prop1, 'くて、', prop2, 'です']
        hir = ''.join(['この', 'へや', 'の', obj_hir2, 'は', prop1_hir, 'くて、',
            prop2_hir, 'です'])
        rus = ' '.join([obj1_rus, 'этой комнаты-', prop1_rus, 'и', prop2_rus])
    else:
        build = ran(a['buildings'])
        build_hir = a['buildings_hir'][build]
        build_rus = a['end_build'][build]
        prop1 = ran(a['adj_for_buildings']['部屋'])
        prop1_hir = a['adj_for_buildings_hir']['部屋'][prop1]
        prop1_rus = a['adj_for_buildings']['部屋'][prop1]
        jap = ['この', '部屋', 'は', build, 'から', '近く', 'なくて、', prop1, 'くないです']
        hir = ''.join(['この', 'へや', 'は', build_hir, 'から', 'ちかく', 'なくて、',
            prop1_hir, 'くないです'])
        rus = ' '.join(['Эта комната далеко от', build_rus, ', и не очень ',
            prop1_rus])
    jap = ''.join(jap)
    return jap, hir, rus, homogeneous_predicates.__name__


def homogeneous_definitions():
    print('homogeneous_definitions')
    glag_jap = random.choice(('買', 'ちゅうもん', '探'))
    glag_hir = a['glagol']['accusative'][glag_jap]
    glag_rus = a['glag_im_going_todo'][glag_jap]
    form = a['glag_form'][glag_jap][2]
    accus = ran(a['small object'])
    accus_hir = a['small object_hir'][accus]
    accus_rus = a['end_get_small_object'][accus]
    jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(accus,
        'only_sush', 'only_pos')
    jap2, hir2, rus2, jap2_ne, jap2_ne_hir, jap2_ne_rus = prop_no_sush(accus,
        'only_sush', 'only_pos')
    if jap2 == jap1:
        while jap2 == jap1:
            jap2, hir2, rus2, jap2_ne, jap2_ne_hir, jap2_ne_rus = prop_no_sush(
                accus, 'only_sush', 'only_pos')
    if jap1[:-1] in a['pril_with_no'] or jap1[:-1] in a['adj_non_predicative']:
        copula = 'で、'
    else:
        copula = 'くて、'
    if jap1[:-1] in a['adj_non_predicative']:
        jap1 = jap1[:-1]
    if jap1 == 'い':
        jap1 = 'よ'
        hir1 = 'よ'
    jap = ['私', 'は', jap1, copula, jap2, jap2_ne, accus, 'を', glag_jap,
        form, 'ます']
    hir = ''.join(['わたし', 'は', hir1, copula, hir2, jap2_ne_hir, accus_hir,
        'を', glag_hir, form, 'ます'])
    rus = ' '.join(['Я', glag_rus, rus1, 'и', rus2, accus_rus])
    jap = ''.join(jap)
    return jap, hir, rus, homogeneous_definitions.__name__


def intention():
    print('intention')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    jap_podl2, jap_podl_hir2, jap_podl_rus2 = ['', '', '']
    ha = ''
    rand = random.randint(0, 3)
    if rand == 0:
        copula = ''.join(['たい', 'と', '思います'])
        copula_hir = ''.join(['たい', 'と', 'おもいます'])
        cop_rus = 'мне хочется (я намереваюсь)'
        form = a['glag_form'][glag_jap][2]
        glag_rus = a['glag_verb_stem_2'][glag_jap]
    elif rand == 1:
        copula = ''.join(['と', '思います'])
        copula_hir = ''.join(['と', 'おもいます'])
        cop_rus = 'я собираюсь\u3000(сейчас появилось желание)'
        form = a['glag_form'][glag_jap][5]
        glag_rus = a['glag_verb_stem_2'][glag_jap]
    elif rand == 2:
        copula = ''.join(['と', '思っています'])
        copula_hir = ''.join(['と', 'おもっています'])
        cop_rus = 'собирается '
        form = a['glag_form'][glag_jap][5]
        glag_rus = a['glag_verb_stem_2'][glag_jap]
        jap_podl2, jap_podl_hir2, jap_podl_rus2 = who_f('family','know_people', 'suff')
        ha = 'は'
    else:
        copula = ''.join(['と', '思っています'])
        copula_hir = ''.join(['と', 'おもっています'])
        cop_rus = 'я собираюсь (ранее возникшее намерение)'
        form = a['glag_form'][glag_jap][5]
        glag_rus = a['glag_verb_stem'][glag_jap]
    jap = [jap_podl2, ha, jap_podl, padez, glag_jap, form, copula]
    hir = ''.join([jap_podl_hir2, ha, jap_podl_hir, padez, glag_hir, form,
        copula_hir])
    rus = ' '.join([jap_podl_rus2, cop_rus, padez_rus, jap_podl_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, intention.__name__


def adjective_predicate_2():
    rand = random.randint(0, 3)
    if rand == 0:
        prof = ran(a['profession'])
        prof_hir = a['profession_hir'][prof]
        prof_rus = a['profession'][prof]
        famil = ran(a['family'])
        famil_hir = a['family_hur'][famil]
        famil_rus = a['family'][famil]
        jap = ['あの方', 'は', famil, 'が', prof, 'です']
        hir = ''.join(['あのかた', 'は', famil_hir, 'が', prof_hir, 'です'])
        rus = ' '.join(['Его', famil_rus, '-', prof_rus])
    elif rand == 1:
        seas = ran(a['seasons'])
        seas_hir = a['seasons_hir'][seas]
        seas_rus = a['seasons'][seas]
        jap = ['私', 'は', '好きな', '季節', 'が', seas, 'です']
        hir = ''.join(['わたし', 'は', 'すきな', 'きせつ', 'が', seas_hir, 'です'])
        rus = ' '.join(['Мой любимый сезон - ', seas_rus])
    elif rand == 2:
        rand_num = str(random.randint(3, 6))
        num = a['numbers'][rand_num]
        num_hir = a['numbers2'][rand_num]
        if rand_num == '3' or rand_num == '4':
            end_rus = 'человека.'
        elif rand_num == '5' or rand_num == '6':
            end_rus = 'человек.'
        jap = ['あの方', 'は', '家族', 'が', num, '人です']
        hir = ''.join(['あの方', 'は', 'かぞく', 'が', num_hir, 'にんです'])
        rus = ' '.join(['В его семье ', rand_num, end_rus])
    else:
        senm = ran(a['senmon'])
        senm_hir = a['senmon_hir'][senm]
        senm_rus = a['senmon'][senm]
        jap = ['私', 'は', 'せん門', 'が', senm, 'です']
        hir = ''.join(['わたし', 'は', 'せんもん', 'が', senm_hir, 'です'])
        rus = ' '.join(['Моя специальность - ', senm_rus])
    jap = ''.join(jap)
    return jap, hir, rus, adjective_predicate_2.__name__


def definitions_expressed_by_the_verb():
    print('definitions_expressed_by_the_verb')
    rand = random.randint(0, 2)
    if rand == 0:
        who = ran(a['names'])
        who_hir = a['names_hir'][who]
        who_rus = a['names'][who]
        if random.randint(0, 1) == 0:
            opr_jap = ''.join(['そこ', 'に', '立っている'])
            opr_hir = ''.join(['そこ', 'に', 'たっている'])
            opr_rus = 'стоит там'
        else:
            jap_podl, jap_podl_hir, jap_podl_rus = who_f('end_family3',
                'end_know3', 'suff')
            glag_with = ran(a['glagol']['withs'])
            glag_with_hir = a['glagol']['withs'][glag_with]
            glag_with_rus = a['glag_now'][glag_with]
            form = a['glag_form'][glag_with][3]
            opr_jap = ''.join([jap_podl, 'に', glag_with, form])
            opr_hir = ''.join([jap_podl_hir, 'に', glag_with_hir, form])
            opr_rus = ' '.join([glag_with_rus, 'c', jap_podl_rus])
        jap = [opr_jap, '人', 'は', who, 'さん', 'です']
        hir = ''.join([opr_hir, 'ひと', 'は', who_hir, 'さん', 'です'])
        rus = ' '.join(['Человек, который', opr_rus, ' - ', who_rus])
    elif rand == 1:
        reas = ran(a['reason_3_form'])
        reas_hir = a['reason_3_form_hir'][reas]
        reas_rus = a['reason_3_form'][reas]
        glag_jap, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
            choose_glag_accus('glag_past_post'))
        form = a['glag_form'][glag_jap][3]
        jap = [reas, '日', 'に、', '私', 'は', accus, 'を', glag_jap, form]
        hir = ''.join([reas_hir, 'にち', 'に、', 'わたし', 'は', accus_hir, 'を',
            glag_hir, form])
        rus = ' '.join(['В день, когда ', reas_rus, 'я', glag_rus, accus_rus])
    else:
        jap_podl, jap_podl_hir, jap_podl_rus = who_f('end_family3',
            'end_know3', 'suff')
        glag_with = ran(a['glagol']['withs'])
        glag_with_hir = a['glagol']['withs'][glag_with]
        glag_with_rus = a['glag_past_post'][glag_with]
        build = ran(a['buildings'])
        build_hir = a['buildings_hir'][build]
        build_rus = a['buildings'][build]
        jap2, hir2, rus2 = prop_no_build(build)
        form = a['glag_form'][glag_with][3]
        jap = [jap_podl, 'に', glag_with, form, build, 'は', jap2, build, 'です']
        hir = ''.join([jap_podl_hir, 'に', glag_with_hir, form, build_hir,
            'は', hir2, build_hir, 'です'])
        rus = ' '.join([build_rus, 'в котором (ой) я', glag_with_rus, 'c',
            jap_podl_rus, '-', rus2, build_rus])
    jap = ''.join(jap)
    return jap, hir, rus, definitions_expressed_by_the_verb.__name__

def reason_node():
    print('reason_node')
    eve = ran(a['events'])
    eve_hir = a['events_hir'][eve]
    eve_rus = a['end_events2'][eve]
    reas = ran(a['reasone_node'])
    reas_hir = a['reasone_node_hir'][reas]
    reas_rus = a['reasone_node'][reas]
    jap = [reas, 'ので、私', 'は', eve, 'に行きません']
    hir = ''.join([reas_hir, 'ので、', 'わたし', 'は', eve_hir, 'に', 'いきません'])
    rus = ' '.join(['Так как', reas_rus, '. я не пойду в(на)', eve_rus,
        '(собеседникам понятна причинно-следственная связь)'])
    jap = ''.join(jap)
    return jap, hir, rus, reason_node.__name__

def can_do_it():
    print('can_do_it')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][2]
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    if glag_jap in a['glagol_2_conjugation']:
        form = 'られ'
    else:
        form = a['glag_form'][glag_jap][4]
    t = Times('glag_budush')
    if glag_jap == 'す':
        glag_jap = 'でき'
        form = ''
    time_jap, time_hir, time_rus = t.main()
    jap = [jap_who, 'は', time_jap, jap_podl, padez, glag_jap, form, 'ます']
    hir = ''.join([hir_podl_who, 'は', time_hir, jap_podl_hir, padez,
        glag_hir, form, 'ます'])
    rus = ' '.join([rus_podl_who, time_rus, 'может', padez_rus,
        jap_podl_rus, glag_rus, '  (у него (нее) есть такая возможность)'])
    jap = ''.join(jap)
    return jap, hir, rus, can_do_it.__name__

def two_actions_formal():
    print('two_actions_formal')
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    g = Glagols('glag_budush', 'choose', ['move', 'not_trans_slow',
        'accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][2]
    g2 = Glagols('glag_budush', 'choose', ['move', 'not_trans_slow',
        'accusative'])
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][2]
    t = Times('glag_budush')
    time_jap, time_hir, time_rus = t.main()
    jap = [jap_who, 'は', time_jap, 'に', jap_podl, padez, glag_jap, form,
        '、', jap_podl2, padez2, glag_jap2, form2, 'ます']
    hir = ''.join([hir_podl_who, 'は', time_hir, 'に', jap_podl_hir, padez,
        glag_hir, form, '、', jap_podl_hir2, padez2, glag_hir2, form2, 'ます'])
    rus = ' '.join([rus_podl_who, time_rus, padez_rus, jap_podl_rus,
        glag_rus, ',', padez_rus2, jap_podl_rus2, glag_rus2,
        '(формальная, письменная речь)'])
    jap = ''.join(jap)
    return jap, hir, rus, two_actions_formal.__name__

def uk_koko_f_2():
    print('uk_koko_f_2')
    ran_build = ran(a['buildings'])
    build_hir = a['buildings_hir'][ran_build]
    build_rus = a['buildings'][ran_build]
    jap2, hir, rus2 = prop_no_build(ran_build)
    if jap2[:-1] not in a['adj_build_without_no'] and jap2[:-1] not in a[
        'adj_build_with_no'] and jap2[:-1] not in a['adj_non_predicative'
        ] and jap2[:-1] not in a['pril_with_no']:
        jap2 = jap2[:-1] + 'く'
        hir = hir[:-1] + 'く'
    jap2_2, hir2, rus2_2 = prop_no_build(ran_build)
    uk_koko = [ran(a['uno']), ran_build, 'は', jap2, '、', jap2_2, 'です']
    uk_koko_hir = ''.join([uk_koko[0], build_hir, 'は', hir, '、', hir2, 'です'])
    uk_koko_rus = ' '.join([a['uno'][uk_koko[0]], build_rus, rus2, ', ',
        rus2_2])
    uk_koko = ''.join(uk_koko)
    return uk_koko, uk_koko_hir, uk_koko_rus, uk_koko_f_2.__name__


def qualifying_clause():
    print('11')
    rand = random.randint(0, 3)
    if rand == 0:
        print('0')
        jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people',
            'suff')
        glag_jap, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
            choose_glag_accus('glag_past_one_moment'))
        if accus in a['adj_for_small_object']:
            pril, pril_hir, pril_rus, jap1_ne, jap1_ne_hir, jap1_ne_rus = (
                prop_no_sush(accus, 'only_sush', 'all'))
        else:
            pril_list = {'高い': ['たかい', 'дорогой'], '安い': ['やすい', 'дешевый']}
            pril = ran(pril_list)
            pril_hir = pril_list[pril][0]
            pril_rus = pril_list[pril][1]
            jap1_ne, jap1_ne_hir, jap1_ne_rus = '', '', ''
        form = a['glag_form'][glag_jap][7]
        jap = [jap_who, 'の', glag_jap, form, accus, 'は', pril, jap1_ne, 'です']
        hir = ''.join([hir_podl_who, 'の', glag_hir, form, accus_hir, 'は',
            pril_hir, jap1_ne_hir, 'です'])
        rus = ' '.join([accus_rus, 'которого(ое)', glag_rus, rus_podl_who,
            '-', jap1_ne_rus, pril_rus])
    elif rand == 1:
        print('1')
        jap_who, hir_podl_who, rus_podl_who = who_f('end_family4',
            'end_know4', 'suff')
        thing = ran(a['food'])
        thing_hir = a['food_hir'][thing]
        thing_rus = a['food'][thing]
        jap = [jap_who, 'の', '好きな', '食べ物', 'は', thing, 'です']
        hir = ''.join([hir_podl_who, 'の', 'すきな', 'たべもの', 'は', thing_hir, 'です'])
        rus = ' '.join(['Любимая еда', rus_podl_who, '-', thing_rus])
    elif rand == 2:
        print('2')
        obj1 = ran(a['room_objects'])
        obj_hir1 = a['room_objects_hir'][obj1]
        obj1_rus = a['room_objects'][obj1]
        rand_prop = ran(a['adj_rooms_si'])
        prop1 = ran(a['adj_rooms_si'][rand_prop])
        prop1_hir = a['adj_rooms_si_hir'][rand_prop][prop1]
        prop1_rus = a['adj_rooms_si'][rand_prop][prop1]
        jap_who, hir_podl_who, rus_podl_who = who_f('end_family4',
            'end_know4', 'suff')
        jap = [obj1, 'の', prop1, '部屋', 'は', jap_who, 'の', 'です']
        hir = ''.join([obj_hir1, 'の', prop1_hir, 'へや', 'は', hir_podl_who,
            'の', 'です'])
        rus = ' '.join(['Комната в которой', prop1_rus, obj1_rus,
            '- комната', rus_podl_who])
    else:
        print('3')
        glag_with = ran(a['glagol']['not_trans_slow'])
        glag_with_hir = a['glagol']['not_trans_slow'][glag_with]
        glag_with_rus = a['glag_im_doing'][glag_with]
        build = ran(a['buildings'])
        build_hir = a['buildings_hir'][build]
        build_rus = a['buildings'][build]
        jap2, hir2, rus2 = prop_no_build(build)
        form = a['glag_form'][glag_with][6]
        adverb = ran(a['adverbs']['person'])
        adverb_hir = a['adverbs_hir']['person'][adverb]
        adverb_rus = a['adverbs']['person'][adverb]
        jap = ['私', 'の', adverb, glag_with, form, 'いる', build, 'は', jap2,
            build, 'です']
        hir = ''.join(['わたし', 'の', adverb_hir, glag_with_hir, form, 'いる',
            build_hir, 'は', hir2, build_hir, 'です'])
        rus = ' '.join([build_rus, 'в котором (ой) я', adverb_rus,
            glag_with_rus, '-', rus2, build_rus])
    jap = ''.join(jap)
    return jap, hir, rus, qualifying_clause.__name__


def stable_ko_to_ga_aru():
    print('12')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    if random.randint(0, 1) == 0:
        form = a['glag_form'][glag_jap][3]
        cop_rus = ' случается (иногда так происходит)'
    else:
        form = a['glag_form'][glag_jap][7]
        cop_rus = 'случалось (раньше так происходило)'
    jap = ['私', 'は', jap_podl, padez, glag_jap, form, 'ことがあります']
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, glag_hir, form, 'ことがあります'])
    rus = ' '.join(['Мне', cop_rus, glag_rus, padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, stable_ko_to_ga_aru.__name__

def stable_its_sounds_good():
    print('13')
    g = Glagols('glag_verb_stem_2', 'choose', ['move', 'accusative',
        'address', 'withs'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    if rand_glag == 'move':
        dop_jap, dop_hir, dop_rus = prop_no_build(jap_podl)
    elif rand_glag == 'accusative':
        if rand_glag in a['glag_accusative']:
            dop_jap = ran(a['glag_accusative'][rand_glag])
            dop_hir = a['glag_accusative_hir'][rand_glag][dop_jap]
            dop_rus = a['glag_accusative'][rand_glag][dop_jap]
        else:
            dop_jap, dop_hir, dop_rus = '', '', ''
    else:
        t = Times('glag_budush')
        dop_jap, dop_hir, dop_rus = t.main()
    if random.randint(0, 1) == 0:
        form = a['glag_form'][glag_jap][3]
        cop_rus = ' Лучше всего (гипотетически, стоит так поступить)'
    else:
        form = a['glag_form'][glag_jap][7]
        cop_rus = 'Лучше все же сделать так (настоятельная рекомендация)'
    jap = [dop_jap, jap_podl, padez, glag_jap, form, '方がいい']
    hir = ''.join([dop_hir, jap_podl_hir, padez, glag_hir, form, 'かたがいい'])
    rus = ' '.join([glag_rus, padez_rus, jap_podl_rus, dop_rus, cop_rus])
    jap = ''.join(jap)
    return jap, hir, rus, stable_its_sounds_good.__name__

def stable_i_decited_to():
    print('14')
    g = Glagols('glag_verb_stem_2', 'choose', ['move', 'accusative',
        'address', 'withs'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    rand = random.randint(0, 2)
    if rand == 0:
        t = Times('glag_budush')
        dop_jap, dop_hir, dop_rus = t.main()
        dop_jap += 'に'
        dop_hir += 'に'
        copula = 'ことにする'
        cop_rus = ' решил (сейчас это решил)'
    elif rand == 1:
        dop_jap, dop_hir, dop_rus = '', '', ''
        copula = 'ことにした'
        cop_rus = (
            'решил (решение принято ранее, само действие уже совершено или скоро может быть свершится)'
            )
    else:
        dop_jap = ran(a['adverbs']['person'])
        dop_hir = a['adverbs_hir']['person'][dop_jap]
        dop_rus = a['adverbs']['person'][dop_jap]
        copula = 'ことにしっている'
        cop_rus = 'решил (взял за обыкновение, за правило)'
        glag_rus = a['glag_verb_stem'][glag_jap]
    jap = ['私', 'は', dop_jap, jap_podl, padez, glag_jap, form, copula]
    hir = ''.join(['わたし', 'は', dop_hir, jap_podl_hir, padez, glag_hir, form,
        copula])
    rus = ' '.join(['Я', cop_rus, glag_rus, padez_rus, jap_podl_rus, dop_rus])
    jap = ''.join(jap)
    return jap, hir, rus, stable_i_decited_to.__name__

def negative_verb_gerund():
    print('15')
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    g = Glagols('glag_past_post', 'choose', ['move', 'accusative',
        'address', 'withs', 'not_trans_slow'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][2]
    g2 = Glagols('glag_gerund_past', 'choose', ['accusative', 'address',
        'withs', 'not_trans_slow'])
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag2) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][1]
    jap = [jap_who, 'は', jap_podl2, padez2, glag_jap2, form2, 'ず', 'に',
        jap_podl, padez, glag_jap, form, 'ました']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir2, padez2, glag_hir2,
        form2, 'ず', 'に', jap_podl_hir, padez, glag_hir, form, 'ました'])
    rus = ' '.join([rus_podl_who, ', не', glag_rus2, padez_rus2,
        jap_podl_rus2, ',', glag_rus, padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, negative_verb_gerund.__name__

def result_type():
    print('16')
    glag_jap, glag_hir, glag_rus, accus, accus_hir, accus_rus = (
        choose_glag_accus('glag_result'))
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][6]
    jap = [accus, 'が', glag_jap, form, 'あります']
    hir = ''.join([accus_hir, 'が', glag_hir, form, 'あります'])
    rus = ' '.join([accus_rus, glag_rus, '(/а/о)'])
    jap = ''.join(jap)
    return jap, hir, rus, result_type.__name__

def stable_actions_from_condition():
    print('17')
    g = Glagols('glag_budush', 'choose', ['move', 'accusative', 'address'])
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    rand = random.randint(0, 2)
    if rand == 0:
        t = Times('glag_budush')
        dop_jap, dop_hir, dop_rus = t.main()
        dop_jap += 'に'
        dop_hir += 'に'
        copula = 'ことになる'
        cop_rus = ' Так получается, что'
    elif rand == 1:
        dop_jap, dop_hir, dop_rus = '', '', ''
        copula = 'ことになった'
        cop_rus = 'Так случилось (так решено), что'
    else:
        dop_jap = ran(a['adverbs']['person'])
        dop_hir = a['adverbs_hir']['person'][dop_jap]
        dop_rus = a['adverbs']['person'][dop_jap]
        copula = 'ことになっている'
        cop_rus = 'Так получается, что'
        glag_rus = a['glag_nast_post'][glag_jap]
    jap = [jap_who, 'は', dop_jap, jap_podl, padez, glag_jap, form, copula]
    hir = ''.join([hir_podl_who, 'は', dop_hir, jap_podl_hir, padez,
        glag_hir, form, copula])
    rus = ' '.join([cop_rus, rus_podl_who, glag_rus, padez_rus,
        jap_podl_rus, dop_rus])
    jap = ''.join(jap)
    return jap, hir, rus, stable_actions_from_condition.__name__

def going_to_in_time():
    print('18')
    g = Glagols('glag_verb_stem_2', 'choose', ['move', 'not_trans_slow',
        'accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][5]
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    g2 = Glagols('glag_past_one_moment', 'choose', ['move',
        'not_trans_slow', 'accusative'])
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][2]
    jap = [jap_podl, padez, glag_jap, form, 'とした', '時、', jap_who, 'は',
        jap_podl2, padez2, glag_jap2, form2, 'ました']
    hir = ''.join([jap_podl_hir, padez, glag_hir, form, 'とした', 'とき、',
        hir_podl_who, 'は', jap_podl_hir2, padez2, glag_hir2, form2, 'ました'])
    rus = ' '.join(['Когда я собрался', glag_rus, padez_rus, jap_podl_rus,
        ',', rus_podl_who, glag_rus2, padez_rus2, jap_podl_rus2,
        ' (речь о временном промежутке)'])
    jap = ''.join(jap)
    return jap, hir, rus, going_to_in_time.__name__

def tameni():
    print('19')
    glag_time = random.choice(('glag_im_going_todo', 'glag_past_one_moment'))
    if glag_time == 'glag_budush':
        copula = 'ます'
        copula_rus = 'куплю'
    else:
        copula = 'ました'
        copula_rus = 'купил'
    rand = random.randint(0, 2)
    if rand == 0:
        jap_podl = ran(a['glag_accusative']['買'])
        jap_podl_hir = a['glag_accusative_hir']['買'][jap_podl]
        jap_podl_rus = a['glag_accusative']['買'][jap_podl]
        jap_who, hir_podl_who, rus_podl_who = who_f('end_family4',
            'end_know4', 'suff')
        jap = [jap_who, 'のために', jap_podl, 'を', '買い', '', copula]
        hir = ''.join([hir_podl_who, 'のために', jap_podl_hir, 'を', 'かい', copula])
        rus = ' '.join(['Я для', rus_podl_who, copula_rus, jap_podl_rus])
    elif rand == 1:
        jap_podl = ran(a['profession'])
        jap_podl_hir = a['profession_hir'][jap_podl]
        jap_podl_rus = a['end_proffesion2'][jap_podl]
        jap_podl2 = random.choice(('本', '教科書', 'ざっし', '新聞', '辞典', '映画'))
        jap_podl_hir2 = a['small object_hir'][jap_podl2]
        jap_podl_rus2 = a['small object'][jap_podl2]
        jap = [jap_podl, 'のための', jap_podl2, 'を', '買い', '', copula]
        hir = ''.join([jap_podl_hir, 'のための', jap_podl_hir2, 'を', 'かい', copula])
        rus = ' '.join(['Я', copula_rus, jap_podl_rus2, 'для', jap_podl_rus])
    else:
        g = Glagols(glag_time, 'choose', ['move', 'not_trans_slow',
            'accusative'])
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][2]
        g2 = Glagols('glag_verb_stem_2', 'choose', ['move',
            'not_trans_slow', 'accusative'])
        (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
            jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
        if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
            glag_jap2 = '聞'
        form2 = a['glag_form'][glag_jap2][3]
        jap = [jap_podl2, padez2, glag_jap2, form2, 'ために、', '私', 'は',
            jap_podl, padez, glag_jap, form, copula]
        hir = ''.join([jap_podl_hir2, padez2, glag_hir2, form2, 'ために、',
            'わたし', 'は', jap_podl_hir, padez, glag_hir, form, copula])
        rus = ' '.join(['Для того чтобы', glag_rus2, padez_rus2,
            jap_podl_rus2, ', я', glag_rus, padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, tameni.__name__

def saying_that():
    print('20')
    glag_time = random.choice(('glag_budush', 'glag_past_one_moment'))
    if glag_time == 'glag_budush':
        copula = 3
    else:
        copula = 7
    g = Glagols(glag_time, 'choose', ['move', 'not_trans_slow', 'accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][copula]
    rand = random.randint(0, 2)
    if rand == 0:
        jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people',
            'suff')
        jap_who2, hir_podl_who2, rus_podl_who2 = who_f('family',
            'know_people', 'suff')
        jap = [jap_who, 'は', jap_who2, 'が', jap_podl, padez, glag_jap, form,
            'と', '言う', 'ました']
        hir = ''.join([hir_podl_who, 'は', hir_podl_who2, 'が', jap_podl_hir,
            padez, glag_hir, form, 'と', 'いう', 'ました'])
        rus = ' '.join([rus_podl_who, 'сказал, что', rus_podl_who2,
            glag_rus, padez_rus, jap_podl_rus])
    elif rand == 1:
        form = a['glag_form'][glag_jap][1]
        t = Times('glag_budush')
        time_jap, time_hir, time_rus = t.main()
        jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people',
            'suff')
        jap = [jap_who, 'は', time_jap, 'に', jap_podl, padez, glag_jap, form,
            'ない', 'と', '思い', 'ます']
        hir = ''.join([hir_podl_who, 'は', time_hir, 'に', jap_podl_hir,
            padez, glag_hir, form, 'ない', 'と', 'おもい', 'ます'])
        rus = ' '.join(['Думаю, что', rus_podl_who, time_rus, 'не',
            glag_rus, padez_rus, jap_podl_rus])
    else:
        form = a['glag_form'][glag_jap][2]
        glag_rus = a['glag_masyou'][glag_jap]
        jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people',
            'suff')
        jap = [jap_who, 'は', '「', jap_podl, padez, glag_jap, form, 'ましょうか',
            '」', 'と', '言う', 'ました']
        hir = ''.join([hir_podl_who, 'は', '「', jap_podl_hir, padez,
            glag_hir, form, 'ましょうか', '」', 'と', 'いう', 'ました'])
        rus = ' '.join([rus_podl_who, 'сказал: "Давайте', glag_rus,
            padez_rus, jap_podl_rus, '"'])
    jap = ''.join(jap)
    return jap, hir, rus, saying_that.__name__

def action_in_time_after_time():
    print('21')
    g = Glagols('glag_nast_post', 'choose', ['move', 'not_trans_slow',
        'accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    rand = random.randint(0, 3)
    if rand == 0:
        reas = ran(a['reason_simple'])
        reas_hir = a['reason_simple_hir'][reas]
        reas_rus = a['reason_simple'][reas]
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][2]
        jap = [reas, '時、', jap_who, 'は', jap_podl, padez, glag_jap, form, 'ます']
        hir = ''.join([reas_hir, 'とき、', hir_podl_who, 'は', jap_podl_hir,
            padez, glag_hir, form, 'ます'])
        rus = ' '.join(['Когда', reas_rus, ',', rus_podl_who, glag_rus,
            padez_rus, jap_podl_rus, ' (речь о временном промежутке)'])
    elif rand == 1:
        jap_prof = ran(a['profession'])
        jap_prof_hir = a['profession_hir'][jap_prof]
        jap_prof_rus = a['end_proffesion'][jap_prof]
        dop_jap = ran(a['adverbs']['person'])
        dop_hir = a['adverbs_hir']['person'][dop_jap]
        dop_rus = a['adverbs']['person'][dop_jap]
        glag_rus = a['glag_past_post'][glag_jap]
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        jap = [jap_who, 'が', jap_prof, 'だった', '時、', dop_jap, jap_podl,
            padez, glag_jap, form, 'いました']
        hir = ''.join([hir_podl_who, 'が', jap_prof_hir, 'だった', 'とき、',
            dop_hir, jap_podl_hir, padez, glag_hir, form, 'いました'])
        rus = ' '.join(['Когда', rus_podl_who, 'был(а)', jap_prof_rus, '-',
            dop_rus, glag_rus, padez_rus, jap_podl_rus,
            ' (речь о временном промежутке)'])
    else:
        how = random.choice(('しずか', 'きれい', 'にぎやか', 'りっぱ', 'すてき', 'ゆう名', 'けっこう')
            )
        how_rus = a['end_predicative'][how]
        build = ran(a['buildings'])
        build_hir = a['buildings_hir'][build]
        build_rus = a['buildings'][build]
        glag_rus = a['glag_past_post'][glag_jap]
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        jap = [build, 'が', how, 'な', '時、', jap_who, 'は', 'そこで', jap_podl,
            padez, glag_jap, form, 'いました']
        hir = ''.join([build_hir, 'が', how, 'な', 'とき、', hir_podl_who, 'は',
            'そこで', jap_podl_hir, padez, glag_hir, form, 'いました'])
        rus = ' '.join(['Когда', build_rus, 'был', how_rus, '-',
            rus_podl_who, 'там', glag_rus, padez_rus, jap_podl_rus,
            ' (речь о временном промежутке)'])
    jap = ''.join(jap)
    return jap, hir, rus, action_in_time_after_time.__name__

def dake_takunaritai():
    print('dake_takunaritai')
    jap_podl = ran(a['buildings'])
    jap_podl_hir = a['buildings_hir'][jap_podl]
    jap_podl_rus = a['end_build2'][jap_podl]
    glag_jap = ran(a['glagol']['move'])
    glag_hir = a['glagol']['move'][glag_jap]
    glag_rus = a['glag_verb_stem_2'][glag_jap]
    form = a['glag_form'][glag_jap][3]
    if random.randint(0, 1) == 0:
        jap = ['私', 'は', jap_podl, 'だけ', 'へ', glag_jap, form, 'たくなり', 'ます']
        hir = ''.join(['わたし', 'は', jap_podl_hir, 'だけ', 'へ', glag_hir, form,
            'たくなり', 'ます'])
        rus = ' '.join(['я захотел', glag_rus, 'только в', jap_podl_rus])
    else:
        jap_podl2 = ran(a['buildings'])
        jap_podl_hir2 = a['buildings_hir'][jap_podl2]
        jap_podl_rus2 = a['end_build2'][jap_podl2]
        jap = ['私', 'は', jap_podl, 'だけでなく、', jap_podl2, 'へ', 'も', glag_jap,
            form, 'たくなり', 'ます']
        hir = ''.join(['わたし', 'は', jap_podl_hir, 'だけでなく、', jap_podl_hir2,
            'へ', 'も', glag_hir, form, 'たくなり', 'ます'])
        rus = ' '.join(['я захотел', glag_rus, 'не только в', jap_podl_rus,
            ', но и в', jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, dake_takunaritai.__name__

def niyotte():
    print('niyotte')
    event = ran(a['events'])
    event_hir = a['events_hir'][event]
    event_rus = a['events'][event]
    cond = ran(a['conditions'])
    cond_hir = a['conditions_hir'][cond]
    cond_rus = a['conditions'][cond]
    prop_dict = {'いい': 'хорошим', 'おもしろい': 'интересным', 'つまらない': 'скучным',
        'にぎやか': 'оживленным'}
    prop_dict_hir = {'いい': 'いい', 'おもしろい': 'おもしろい', 'つまらない': 'つまらない', 'にぎやか':
        'にぎやか'}
    rand_prop = ran(prop_dict)
    rand_prop_hir = prop_dict_hir[rand_prop]
    rand_prop_rus = prop_dict[rand_prop]
    jap = [event, 'は', cond, 'によって', rand_prop, 'です']
    hir = ''.join([event_hir, 'は', cond_hir, 'によって', rand_prop_hir, 'です'])
    rus = ' '.join([event_rus, 'бывает', rand_prop_rus, 'в зависимости от ',
        cond_rus])
    jap = ''.join(jap)
    return jap, hir, rus, niyotte.__name__

def passive():
    print('passive')
    if random.randint(0, 1):
        g = Glagols('glag_passive_eba', 'choose', ['accusative'])
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        podl1, podl1_hir, podl1_rus = who_f('end_family3', 'end_know3',
            'suff_no3')
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][1]
        if glag_jap in a['glagol_2_conjugation']:
            copula = 'られた'
        else:
            copula = 'れた'
        if random.randint(0, 1):
            padez = 'に'
            dop = ' (простая речь, не формальная)'
        else:
            padez = 'によって'
            dop = ' (формальная, как по новостям)'
        jap = [jap_podl, 'は', podl1, padez, glag_jap, form, copula]
        hir = ''.join([jap_podl_hir, 'は', podl1_hir, padez, glag_hir, form,
            copula])
        rus = ' '.join([jap_podl_rus,
            '(мысленно переделай в основной падеж)', glag_rus, podl1_rus, dop])
    else:
        glag_jap = ran(a['glagol']['address'])
        glag_hir = a['glagol']['address'][glag_jap]
        glag_rus = a['glag_passive_eba'][glag_jap]
        jap_podl, jap_podl_hir, jap_podl_rus = who_f('family',
            'know_people', 'suff')
        if glag_jap == '聞_2':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][1]
        if glag_jap in a['glagol_2_conjugation']:
            copula = 'られた'
        else:
            copula = 'れた'
        podl1, podl1_hir, podl1_rus = who_f('end_family3', 'end_know3',
            'suff_no3')
        jap = [jap_podl, 'は', podl1, 'から', glag_jap, form, copula]
        hir = ''.join([jap_podl_hir, 'は', podl1_hir, 'から', glag_hir, form,
            copula])
        rus = ' '.join([jap_podl_rus, glag_rus, podl1_rus])
    jap = ''.join(jap)
    return jap, hir, rus, passive.__name__

def passive_opportunity():
    print('passive_opportunity')
    g = Glagols('glag_passive_eba', 'choose', ['accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    podl1, podl1_hir, podl1_rus = who_f('end_family3', 'end_know3', 'suff_no3')
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][1]
    if glag_jap in a['glagol_2_conjugation']:
        copula = 'られた'
    else:
        copula = 'れた'
    jap = [jap_podl, 'は', podl1, 'が', glag_jap, form, copula]
    hir = ''.join([jap_podl_hir, 'は', podl1_hir, 'が', glag_hir, form, copula])
    rus = ' '.join([jap_podl_rus,
        '(мысленно переделай в основной падеж), может быть', glag_rus,
        podl1_rus, '(письменная форма. акцент на явлении, а не на человеке)'])
    jap = ''.join(jap)
    return jap, hir, rus, passive_opportunity.__name__

def result_oku():
    print('result_oku')
    glag_jap = random.choice(('練習', 'そうじ', '買', 'しゃしんをと', '読', '飾', '包',
        '持って来'))
    glag_jap_hir = a['glagol']['accusative'][glag_jap]
    glag_rus = a['glag_past_one_moment'][glag_jap]
    dop_jap = ran(a['glag_accusative'][glag_jap])
    dop_hir = a['glag_accusative_hir'][glag_jap][dop_jap]
    dop_rus = a['glag_accusative'][glag_jap][dop_jap]
    form = a['glag_form'][glag_jap][6]
    jap = ['彼', 'は', dop_jap, 'を', glag_jap, form, 'おいました']
    hir = ''.join(['かれ', 'は', dop_hir, 'を', glag_jap_hir, form, 'おいました'])
    rus = ' '.join(['Он ', glag_rus, dop_rus,
        ' (результативный вид. Результат сохраняется и Позже будет использован)'
        ])
    jap = ''.join(jap)
    return jap, hir, rus, result_oku.__name__

def result_simau():
    print('result_simau')
    glag_jap = random.choice(('練習', 'そうじ', '買', 'しゃしんをと', '読', '飾', '包',
        '持って来'))
    glag_jap_hir = a['glagol']['accusative'][glag_jap]
    glag_rus = a['glag_past_one_moment'][glag_jap]
    dop_jap = ran(a['glag_accusative'][glag_jap])
    dop_hir = a['glag_accusative_hir'][glag_jap][dop_jap]
    dop_rus = a['glag_accusative'][glag_jap][dop_jap]
    form = a['glag_form'][glag_jap][6]
    jap = ['彼', 'は', 'もう', dop_jap, 'を', glag_jap, form, 'しまいました']
    hir = ''.join(['かれ', 'は', 'もう', dop_hir, 'を', glag_jap_hir, form, 'しまいました']
        )
    rus = ' '.join(['Он уже', glag_rus, dop_rus,
        ' (результативный вид. Результат необратим)'])
    jap = ''.join(jap)
    return jap, hir, rus, result_simau.__name__

def repetitive_aspect():
    print('repetitive_aspect')
    g1 = Glagols('glag_past_one_moment', 'all')
    (glag_jap1, glag_hir1, glag_rus1, jap_podl1, jap_podl_hir1,
        jap_podl_rus1, padez1, padez_rus1, rand_glag1) = g1.main()
    if glag_jap1 == '聞_2' or glag_jap1 == '聞_1':
        glag_jap1 = '聞'
    g2 = Glagols('glag_past_one_moment', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag2) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form1 = a['glag_form'][glag_jap1][7]
    form2 = a['glag_form'][glag_jap2][7]
    sentence_type = random.choice(['alternation', 'depending',
        'representative'])
    if sentence_type == 'alternation':
        jap = [jap_podl1, padez1, glag_jap1, form1, 'り', jap_podl2, padez2,
            glag_jap2, form2, 'り', 'します']
        hir = ''.join([jap_podl_hir1, padez1, glag_hir1, form1, 'り',
            jap_podl_hir2, padez2, glag_hir2, form2, 'り', 'します'])
        rus = ' '.join(['То', glag_rus1, padez_rus1, jap_podl_rus1 + ',',
            'то', glag_rus2, padez_rus2, jap_podl_rus2])
    elif sentence_type == 'depending':
        condition = random.choice(['人', '場所', '時間'])
        condition_hir = {'人': 'ひと', '場所': 'ばしょ', '時間': 'じかん'}[condition]
        condition_rus = {'人': 'человека', '場所': 'места', '時間': 'времени'}[
            condition]
        jap = [condition, 'によって', jap_podl1, padez1, glag_jap1, form1, 'り、',
            jap_podl2, padez2, glag_jap2, form2, 'り', 'します']
        hir = ''.join([condition_hir, 'によって', jap_podl_hir1, padez1,
            glag_hir1, form1, 'り、', jap_podl_hir2, padez2, glag_hir2, form2,
            'り', 'します'])
        rus = ' '.join(['В зависимости от', condition_rus, 'то', glag_rus1,
            padez_rus1, jap_podl_rus1 + ',', 'то', glag_rus2, padez_rus2,
            jap_podl_rus2])
    else:
        jap = [jap_podl1, padez1, glag_jap1, form1, 'り', 'します']
        hir = ''.join([jap_podl_hir1, padez1, glag_hir1, form1, 'り', 'します'])
        rus = ' '.join(['Например,', glag_rus1, padez_rus1, jap_podl_rus1])
    jap = ''.join(jap)
    return jap, hir, rus, repetitive_aspect.__name__

def repetitive_aspect_adjectives():
    print('repetitive_aspect_adjectives')
    obj1, obj2 = random.sample(list(a['small object'].keys()), k=2)
    obj1_hir = a['small object_hir'][obj1]
    obj2_hir = a['small object_hir'][obj2]
    obj1_rus = a['small object'][obj1]
    obj2_rus = a['small object'][obj2]
    adj1 = ran(a['adj_for_small_object'][obj1])
    adj2 = ran(a['adj_for_small_object'][obj2])
    adj1_hir = a['adj_for_small_object_hir'][obj1][adj1]
    adj2_hir = a['adj_for_small_object_hir'][obj2][adj2]
    adj1_rus = a['adj_for_small_object'][obj1][adj1]
    adj2_rus = a['adj_for_small_object'][obj2][adj2]
    sentence_type = random.choice(['alternation', 'representative'])
    if sentence_type == 'alternation':
        jap = [obj1, 'は', adj1, 'かった', 'り、', obj2, 'は', adj2, 'かった', 'り', 'です']
        hir = ''.join([obj1_hir, 'は', adj1_hir, 'かった', 'り、', obj2_hir, 'は',
            adj2_hir, 'かった', 'り', 'です'])
        rus = ' '.join(['То', obj1_rus, 'бывает', adj1_rus + ',', 'то',
            obj2_rus, 'бывает', adj2_rus])
    else:
        jap = [obj1, 'は', adj1, 'かった', 'り', 'です']
        hir = ''.join([obj1_hir, 'は', adj1_hir, 'かった', 'り', 'です'])
        rus = ' '.join(['Например,', obj1_rus, 'бывает', adj1_rus])
    jap = ''.join(jap)
    return jap, hir, rus, repetitive_aspect_adjectives.__name__

def double_case():
    print('double_case')
    construction_type = random.choice(['from', 'to', 'with'])
    if construction_type == 'from':
        sender, sender_hir, sender_rus = who_f('end_family4', 'end_know4',
            'suff')
        item = ran(a['small object'])
        item_hir = a['small object_hir'][item]
        item_rus = a['small object'][item]
        jap = [sender, 'から', 'の', item, 'が', '来ました']
        hir = ''.join([sender_hir, 'から', 'の', item_hir, 'が', 'きました'])
        rus = ' '.join(['Пришло', item_rus, 'от', sender_rus])
    elif construction_type == 'to':
        place = ran(a['buildings'])
        place_hir = a['buildings_hir'][place]
        place_rus = a['end_build4'][place]
        action = ran(a['events'])
        action_hir = a['events_hir'][action]
        action_rus = a['end_events2'][action]
        jap = [place, 'への', action, 'を', '計画しています']
        hir = ''.join([place_hir, 'への', action_hir, 'を', 'けいかくしています'])
        rus = ' '.join(['Планирую', action_rus, 'в', place_rus])
    else:
        companion, companion_hir, companion_rus = who_f('end_family3',
            'end_know3', 'suff')
        activity = ran(a['events'])
        activity_hir = a['events_hir'][activity]
        activity_rus = a['end_events2'][activity]
        jap = [companion, 'との', activity, 'を', '楽しみにしています']
        hir = ''.join([companion_hir, 'との', activity_hir, 'を', 'たのしみにしています'])
        rus = ' '.join(['Я с нетерпением жду', activity_rus, 'с',
            companion_rus])
    jap = ''.join(jap)
    return jap, hir, rus, double_case.__name__

def conditional_temporal_eba():
    print('conditional_temporal_eba')
    g = Glagols('glag_im_going_todo', 'all')
    (glag_jap1, glag_hir1, glag_rus1, jap_podl1, jap_podl_hir1,
        jap_podl_rus1, padez1, padez_rus1, rand_glag) = g.main()
    if glag_jap1 == '聞_2' or glag_jap1 == '聞_1':
        glag_jap1 = '聞'
    rand = random.randint(0, 2)
    form_1 = a['glag_form'][glag_jap1][2]
    if rand == 0:
        g = Glagols('glag_im_going_todo', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        if random.randint(0, 1) == 0:
            form = a['glag_form'][glag_jap][4] + 'ば'
            form_hir = a['glag_form'][glag_jap][4] + 'ば'
            rus_condition = 'Если ' + glag_rus
        else:
            form = a['glag_form'][glag_jap][1] + 'なければ'
            form_hir = a['glag_form'][glag_jap][1] + 'なければ'
            rus_condition = 'Если не ' + glag_rus
        jap = [jap_podl, padez, glag_jap, form, '、', jap_podl1, padez1,
            glag_jap1, form_1, 'ます']
        hir = ''.join([jap_podl_hir, padez, glag_hir, form_hir, '、',
            jap_podl_hir1, padez1, glag_hir1, form_1, 'ます'])
        rus = ' '.join([rus_condition, padez_rus, jap_podl_rus + ',', 'я',
            glag_rus1, padez_rus1, jap_podl_rus1])
    elif rand == 1:
        action = ran(a['events'])
        action_hir = a['events_hir'][action]
        action_rus = a['end_events2'][action]
        prop_dict = {'にぎやか': 'оживленный\\ая', 'しずか': 'тихий/ая'}
        prop_dict_hir = {'にぎやか': 'にぎやか', 'しずか': 'しずか'}
        prop = ran(prop_dict)
        if random.randint(0, 1) == 0:
            form = prop + 'であれば'
            form_hir = prop_dict_hir[prop] + 'であれば'
            rus_condition = 'Если ' + prop_dict[prop]
        else:
            form = prop + 'でなければ'
            form_hir = prop_dict_hir[prop] + 'でなければ'
            rus_condition = 'Если не ' + prop_dict[prop]
        jap = [action, 'は', form, '、', jap_podl1, padez1, glag_jap1, form_1,
            'ます']
        hir = ''.join([action_hir, 'は', form_hir, '、', jap_podl_hir1,
            padez1, glag_hir1, form_1, 'ます'])
        rus = ' '.join([rus_condition, action_rus + ',', 'я', glag_rus1,
            padez_rus1, jap_podl_rus1])
    else:
        action = ran(a['events'])
        action_hir = a['events_hir'][action]
        action_rus = a['end_events2'][action]
        prop_dict = {'よ': 'хороший/ее', 'おもしろ': 'интересный\\ая', 'つまらな':
            'скучный\\ая'}
        prop_dict_hir = {'よ': 'よ', 'おもしろ': 'おもしろ', 'つまらな': 'つまらな'}
        prop = ran(prop_dict)
        if random.randint(0, 1) == 0:
            form = prop + 'ければ'
            form_hir = prop_dict_hir[prop] + 'ければ'
            rus_condition = 'Если ' + prop_dict[prop]
        else:
            form = prop + 'くなければ'
            form_hir = prop_dict_hir[prop] + 'くなければ'
            rus_condition = 'Если не ' + prop_dict[prop]
        jap = [action, 'は', form, '、', jap_podl1, padez1, glag_jap1, form_1,
            'ます']
        hir = ''.join([action_hir, 'は', form_hir, '、', jap_podl_hir1,
            padez1, glag_hir1, form_1, 'ます'])
        rus = ' '.join([rus_condition, action_rus + ',', 'я', glag_rus1,
            padez_rus1, jap_podl_rus1])
    jap = ''.join(jap)
    return jap, hir, rus, conditional_temporal_eba.__name__

def conditional_form_verb_ba_ii():
    print('conditional_form_verb_ba_ii')
    glag = ran(a['glag_instrument'])
    glag_hir = a['glag_instrument_hir_for_glagoles'][glag]
    glag_rus = a['glag_verb_stem'][glag]
    instr = ran(a['glag_instrument'][glag])
    instr_hir = a['glag_instrument_hir'][glag][instr]
    instr_rus = a['glag_instrument'][glag][instr]
    if glag == '聞_2' or glag == '聞_1':
        glag = '聞'
    form = a['glag_form'][glag][4]
    jap = [instr, 'で', glag, form, 'ばいい', 'です']
    hir = ''.join([instr_hir, 'で', glag_hir, form, 'ばいい', 'です'])
    rus = ' '.join(['Следует', glag_rus, instr_rus])
    jap = ''.join(jap)
    return jap, hir, rus, conditional_form_verb_ba_ii.__name__

def concessive_subordinate_noni():
    print('concessive_subordinate_noni')
    eve = random.choice(('見物', '散歩', 'コンサート', 'パーティ', 'お祭り', 'お花見'))
    eve_hir = a['events_hir'][eve]
    eve_rus = a['end_events2'][eve]
    reas = ran(a['reason_simple'])
    reas_hir = a['reason_simple_hir'][reas]
    reas_rus = a['reason_simple'][reas]
    jap = [reas, 'のに、私', 'は', eve, 'に', '行きません']
    hir = ''.join([reas_hir, 'のに、わたし', 'は', eve_hir, 'に', 'いきせん'])
    rus = ' '.join(['Хотя', reas_rus, ', ', 'я не пойду в(на)', eve_rus,
        '( противопоставляются только реальные события)'])
    jap = ''.join(jap)
    return jap, hir, rus, concessive_subordinate_noni.__name__

def substantivization_of_verbs():
    print('substantivization_of_verbs')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap1, glag_hir1, glag_rus1, jap_podl1, jap_podl_hir1,
        jap_podl_rus1, padez1, padez_rus1, rand_glag) = g.main()
    if glag_jap1 == '聞_2' or glag_jap1 == '聞_1':
        glag_jap1 = '聞'
    form = a['glag_form'][glag_jap1][3]
    jap_podl, jap_podl_hir, jap_podl_rus = who_f('family', 'know_people',
        'suff')
    if random.randint(0, 1) == 0:
        ski = '好き'
        ski_hir = 'すき'
        ski_rus = 'любит'
    else:
        ski = 'きらい'
        ski_hir = 'きらい'
        ski_rus = 'не любит'
    jap = [jap_podl, 'は', jap_podl1, padez1, glag_jap1, form, 'こと', 'が',
        ski, 'です']
    hir = ''.join([jap_podl_hir, 'は', jap_podl_hir1, padez1, glag_hir1,
        form, 'こと (の)', 'が', ski_hir, 'です'])
    rus = ' '.join([jap_podl_rus, ski_rus, glag_rus1, padez_rus1,
        jap_podl_rus1])
    jap = ''.join(jap)
    return jap, hir, rus, substantivization_of_verbs.__name__

def substantivization_of_verbs_mono():
    print('substantivization_of_verbs_mono')
    g = Glagols('glag_im_doing', 'choose', ['accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap = [glag_jap, form, 'もの', 'は', jap_podl, 'です']
    hir = ''.join([glag_hir, form, 'もの', 'は', jap_podl_hir, 'です'])
    rus = ' '.join(['Вещь, которую я', glag_rus, '-', jap_podl_rus,
        '(мысленно переделай в основной падеж)'])
    jap = ''.join(jap)
    return jap, hir, rus, substantivization_of_verbs_mono.__name__

def substantivization_of_verbs_no():
    print('substantivization_of_verbs_no')
    g = Glagols('glag_past_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    jap_podl1, jap_podl_hir1, jap_podl_rus1 = who_f('family', 'know_people',
        'suff')
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    skaz = random.choice(('見', '聞_1'))
    skaz_hir = a['glagol']['accusative'][skaz]
    skaz_dict = {'見': 'видел', '聞_1': 'слышал'}
    skaz_rus = skaz_dict[skaz]
    if skaz == '聞_1':
        skaz = '聞'
    form2 = a['glag_form'][skaz][2]
    jap = ['私', 'は', jap_podl1, 'が', jap_podl, padez, glag_jap, form, 'の',
        'を', skaz, form2, 'ました']
    hir = ''.join(['わたし', 'は', jap_podl_hir1, 'が', jap_podl_hir, padez,
        glag_hir, form, 'の', 'を', skaz_hir, form2, 'ました'])
    rus = ' '.join(['Я', skaz_rus, ', как', jap_podl_rus1, glag_rus,
        padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, substantivization_of_verbs_no.__name__

def passive_opportunity_intransitive():
    print('passive_opportunity_intransitive')
    glag_jap = random.choice(a['intransitive_glagols'])
    glag_hir = a['intransitive_glagols_hir'][glag_jap]
    glag_rus = a['glag_past_one_moment2'][glag_jap]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    form = a['glag_form'][glag_jap][1]
    if glag_jap in a['glagol_2_conjugation']:
        copula = 'られた'
    else:
        copula = 'れた'
    jap = ['私', 'は', podl1, 'に', glag_jap, form, copula]
    hir = ''.join(['わたし', 'は', podl1_hir, 'に', glag_hir, form, copula])
    rus = ' '.join(['', 'я подвергся тому, что', podl1_rus, glag_rus,
        ' (Эффект неприятный для меня)'])
    jap = ''.join(jap)
    return jap, hir, rus, passive_opportunity_intransitive.__name__

def passive_omou():
    print(passive_omou)
    dicts_words = {'言われる': ['いわれる', 'Говорят, что'], '見られる': ['みられる',
        'Думается (выглядит так), что'], '思われる': ['おもわれる', 'Считается, что']}
    word = ran(dicts_words)
    word_hir = dicts_words[word][0]
    word_rus = dicts_words[word][1]
    telling = ran(a['telling'])
    telling_hir = a['telling_hir'][telling]
    telling_rus = a['telling'][telling]
    prop_dict = {'おもしろい': 'интересная', 'むずかしい': 'сложная', 'つまらない':
        'скучная', 'やすい': 'легкая'}
    prop = ran(prop_dict)
    prop_hir = prop
    prop_rus = prop_dict[prop]
    jap = [telling, 'は', prop, 'もの', 'と', word]
    hir = ''.join([telling_hir, 'は', prop_hir, 'もの', 'と', word_hir])
    rus = ' '.join([word_rus, telling_rus, '-', prop_rus, ' вещь (тема)'])
    jap = ''.join(jap)
    return jap, hir, rus, passive_omou.__name__

def concessive_subordinate_demo():
    print('concessive_subordinate_demo')
    eve = random.choice(('見物', '散歩', 'コンサート', 'パーティ', 'お祭り', 'お花見'))
    eve_hir = a['events_hir'][eve]
    eve_rus = a['end_events2'][eve]
    reas = ran(a['reasons_without_copula'])
    reas_hir = a['reasons_without_copula_hir'][reas]
    reas_rus = a['reasons_without_copula'][reas]
    rand = random.randint(0, 1)
    if rand == 0:
        ikura = 'いくら'
        rus_expl = '(плюс усиление степени)'
    else:
        ikura = ''
        rus_expl = ''
    jap = [ikura, reas, 'でも、私', 'は', eve, 'に', '行く']
    hir = ''.join([ikura, reas_hir, 'でも、わたし', 'は', eve_hir, 'に', 'いく'])
    rus = ' '.join(['Даже если', reas_rus, ', ', 'я пойду в(на)', eve_rus,
        '( противопоставляются и реальные и вероятные события)', rus_expl])
    jap = ''.join(jap)
    return jap, hir, rus, concessive_subordinate_demo.__name__

def concessive_subordinate_demo_general():
    print('concessive_subordinate_demo_general')
    g = Glagols('glag_past_one_moment', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][6]
    g = Glagols('glag_im_going_todo', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][2]
    question_words = {'だれ': {'hir': 'だれ', 'rus': 'кто бы', 'particle': 'が'},
        'いつ': {'hir': 'いつ', 'rus': 'когда бы', 'particle': ''}, 'どこ': {
        'hir': 'どこ', 'rus': 'где бы', 'particle': 'で'}}
    ques = ran(question_words)
    ques_hir = question_words[ques]['hir']
    ques_rus = question_words[ques]['rus']
    particle = question_words[ques]['particle']
    jap = [ques, particle, jap_podl, padez, glag_jap, form1, 'でも、',
        jap_podl2, padez2, glag_jap2, form2, 'ない']
    hir = ''.join([ques_hir, particle, jap_podl_hir, padez, glag_hir, form1,
        'でも、', jap_podl_hir2, padez2, glag_hir2, form2, 'ない'])
    rus = ' '.join([ques_rus, 'ни', glag_rus, padez_rus, jap_podl_rus,
        ', я не', glag_rus2, padez_rus2, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, concessive_subordinate_demo_general.__name__

def intention_tsumori():
    print('intention_tsumori')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    glag_rus = a['glag_verb_stem_2'][glag_jap]
    jap = ['私', 'は', jap_podl, padez, glag_jap, form, 'つもり', 'です']
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, glag_hir, form, 'つもり',
        'です'])
    rus = ' '.join(['я намереваюсь', glag_rus, padez_rus, jap_podl_rus,
        '(устойчивое по времени намерение)'])
    jap = ''.join(jap)
    return jap, hir, rus, intention_tsumori.__name__

def intention_tokoro():
    print('intention_tokoro')
    rand = random.randint(0, 2)
    if rand == 0:
        time = 'glag_verb_stem_2'
        g = Glagols(time, 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][3]
        moment_rus = 'как раз собираюсь'
    elif rand == 1:
        time = 'glag_im_doing'
        g = Glagols(time, 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6] + 'いる'
        moment_rus = 'как раз сейчас'
    else:
        time = 'glag_past_one_moment2'
        g = Glagols(time, 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        form = a['glag_form'][glag_jap][7]
        moment_rus = 'только что'
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    jap = ['私', 'は', jap_podl, padez, glag_jap, form, 'ところ', 'です']
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, glag_hir, form, 'ところ',
        'です'])
    rus = ' '.join(['я ', moment_rus, glag_rus, padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, intention_tokoro.__name__

def intention_tokoro_2():
    print('intention_tokoro_2')
    rand = random.randint(0, 1)
    if rand == 0:
        time = 'glag_past_one_moment2'
        mou_jap = 'もう少しで、'
        mou_hir = 'もうすこしで、'
        mou_rus = 'Еще немного, и он бы'
        moment_rus = ''
    else:
        time = 'glag_verb_stem_2'
        moment_rus = 'он как раз собирался'
        t = Times('glag_past_one_moment')
        mou_jap, mou_hir, mou_rus = t.main()
    g = Glagols(time, 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap = [mou_jap, '彼', 'が', jap_podl, padez, glag_jap, form, 'ところ', 'でした']
    hir = ''.join([mou_hir, 'かれ', 'が', jap_podl_hir, padez, glag_hir, form,
        'ところ', 'でした'])
    rus = ' '.join([mou_rus, moment_rus, glag_rus, padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, intention_tokoro_2.__name__

def subordinate_clause_mae_siro():
    print('subordinate_clause_mae_siro')
    rand = random.randint(0, 1)
    if rand == 0:
        mae_siro = '前'
        mae_siro_hir = 'まえ'
        mae_siro_rus = 'Перед тем, как'
        time_form1 = 3
    else:
        mae_siro = '後'
        mae_siro_hir = 'あと'
        mae_siro_rus = 'До того, как'
        time_form1 = 7
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][time_form1]
    g = Glagols('glag_past_one_moment', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][2]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form1, mae_siro, '、',
        jap_podl2, padez2, glag_jap2, form2, 'ました']
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form1,
        mae_siro_hir, '、', jap_podl_hir2, padez2, glag_hir2, form2, 'ました'])
    rus = ' '.join([mae_siro_rus, glag_rus, padez_rus, jap_podl_rus, ', ',
        podl1_rus, glag_rus2, padez_rus2, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, subordinate_clause_mae_siro.__name__

def target_noni():
    print('target_noni')
    glag_jap = random.choice(('書', '食', '習'))
    glag_hir = a['glag_instrument_hir_for_glagoles'][glag_jap]
    glag_rus = a['glag_verb_stem'][glag_jap]
    form1 = a['glag_form'][glag_jap][3]
    instr = ran(a['glag_instrument'][glag_jap])
    instr_hir = a['glag_instrument_hir'][glag_jap][instr]
    instr_rus = a['instrument_osnova'][instr]
    rand = random.randint(0, 2)
    if rand == 0:
        noni = '使っています'
        noni_hir = 'つかっています'
        noni_rus = 'используется'
    elif rand == 1:
        noni = '要る'
        noni_hir = 'いる'
        noni_rus = 'требуется'
    else:
        noni = '必要です'
        noni_hir = 'ひつようです'
        noni_rus = 'необходим'
    jap = [glag_jap, form1, 'のに、', instr, 'が', noni]
    hir = ''.join([glag_hir, form1, 'のに、', instr_hir, 'が', noni_hir])
    rus = ' '.join(['Чтобы', glag_rus, ', ', noni_rus, instr_rus])
    jap = ''.join(jap)
    return jap, hir, rus, target_noni.__name__

def service_particle_toiu():
    print('service_particle_toiu')
    g = Glagols('glag_past_one_moment', 'choose', ['move'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][2]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    name_jap = ran(a['name_of_buildings_duct'])
    name_hir = a['name_of_buildings_duct_hir'][name_jap]
    name_rus = a['name_of_buildings_duct'][name_jap]
    jap = [podl1, 'は', name_jap, 'という', jap_podl, padez, glag_jap, form1, 'ました'
        ]
    hir = ''.join([podl1_hir, 'は', name_hir, 'という', jap_podl_hir, padez,
        glag_hir, form1, 'ました'])
    rus = ' '.join([podl1_rus, glag_rus, padez_rus, jap_podl_rus,
        ', который называется', name_rus])
    jap = ''.join(jap)
    return jap, hir, rus, service_particle_toiu.__name__

def incentive_voice():
    print('incentive_voice')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][1]
    rand = random.randint(0, 1)
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    if rand == 0:
        if glag_jap in a['glagol_2_conjugation']:
            suff = 'させる'
        else:
            suff = 'せる'
        dop = ''
        dop_rus = 'заставляет'
        podl2, podl2_hir, podl2_rus = who_f('end_family', 'end_know', 'suff')
    else:
        if glag_jap in a['glagol_2_conjugation']:
            suff = 'させ'
        else:
            suff = 'せ'
        dop = 'てもらいました'
        dop_rus = 'позволил/а'
        podl2, podl2_hir, podl2_rus = who_f('end_family2', 'end_know2', 'suff')
    jap = [podl1, 'は', podl2, 'に', jap_podl, padez, glag_jap, form1, suff, dop]
    hir = ''.join([podl1_hir, 'は', podl2_hir, 'に', jap_podl_hir, padez,
        glag_hir, form1, suff, dop])
    rus = ' '.join([podl1_rus, dop_rus, podl2_rus, glag_rus, padez_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, incentive_voice.__name__

def incentive_voice_kudasai():
    print('incentive_voice_kudasai')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    rand = random.randint(0, 1)
    if rand == 0:
        copula = 'てくださいませんか'
        rus_expl = '(чуть менее вежливый вариант)'
        if glag_jap in a['glagol_2_conjugation']:
            suff = 'させ'
        else:
            suff = 'せ'
        form1 = a['glag_form'][glag_jap][1]
    else:
        copula = 'いただけませんか'
        suff = ''
        rus_expl = '(очень вежливый вариант)'
        form1 = a['glag_form'][glag_jap][6]
    jap = [jap_podl, padez, glag_jap, form1, suff, copula]
    hir = ''.join([jap_podl_hir, padez, glag_hir, form1, suff, copula])
    rus = ' '.join(['Не позволите ли вы ', glag_rus, padez_rus,
        jap_podl_rus, rus_expl])
    jap = ''.join(jap)
    return jap, hir, rus, incentive_voice_kudasai.__name__

def permission_perform_action():
    print('permission_perform_action')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    rand = random.randint(0, 1)
    if rand == 0:
        copula = 'も'
        form = a['glag_form'][glag_jap][6]
        dop_rus = 'Можно'
    else:
        copula = 'なくても'
        form = a['glag_form'][glag_jap][1]
        dop_rus = 'Можно не'
    rand2 = random.randint(0, 2)
    if rand2 == 0:
        dop = 'いい'
        dopr = ' (обычный вариант выражения разрешения)'
    elif rand2 == 1:
        dop = 'かまいません'
        dopr = ' (более вежливый вариант)'
    else:
        dop = 'よろしい'
        dopr = ' (более вежливый вариант)'
    jap = [jap_podl, padez, glag_jap, form, copula, dop]
    hir = ''.join([jap_podl_hir, padez, glag_hir, form, copula, dop])
    rus = ' '.join([dop_rus, glag_rus, padez_rus, jap_podl_rus, dopr])
    jap = ''.join(jap)
    return jap, hir, rus, permission_perform_action.__name__

def permission_perform_prop():
    print('permission_perform_action')
    ran_sush = ran(a['small object'])
    ran_sush_hir = a['small object_hir'][ran_sush]
    ran_sush_rus = a['small object'][ran_sush]
    jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(ran_sush
        , 'only_sush', 'all')
    rand = random.randint(0, 2)
    if rand == 0:
        copula = 'くてもいい'
        dop_rus = 'Можно'
    else:
        copula = 'くなくてもいい'
        dop_rus = 'Можно не'
    jap = [ran_sush, 'は', jap1, copula]
    hir = ''.join([ran_sush_hir, 'は', hir1, copula])
    rus = ' '.join([ran_sush_rus, dop_rus, rus1])
    jap = ''.join(jap)
    return jap, hir, rus, permission_perform_prop.__name__

def expression_prohibition():
    print('expression_prohibition')
    rand1 = random.randint(0, 2)
    if rand1 == 0:
        rand_copula = 'いけない'
        rus_copula = '(мягкая форма)'
    elif rand1 == 1:
        rand_copula = 'ならない'
        rus_copula = '(самая строгая форма)'
    else:
        rand_copula = 'だめだ'
        rus_copula = '(разговорная речь)'
    rand = random.randint(0, 2)
    if rand == 0:
        g = Glagols('glag_verb_stem', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        jap = [jap_podl, padez, glag_jap, form, rand_copula]
        hir = ''.join([jap_podl_hir, padez, glag_hir, form, rand_copula])
        rus = ' '.join([glag_rus, padez_rus, jap_podl_rus, '- нельзя',
            rus_copula])
    elif rand == 1:
        ran_sush = ran(a['small object'])
        ran_sush_hir = a['small object_hir'][ran_sush]
        ran_sush_rus = a['small object'][ran_sush]
        jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(
            ran_sush, 'only_sush', 'all')
        jap = [ran_sush, 'は', jap1, 'くては', rand_copula]
        hir = ''.join([ran_sush_hir, 'は', hir1, 'くては', rand_copula])
        rus = ' '.join([rus1, ran_sush_rus, '- нельзя', rus_copula])
    else:
        event_jap = ran(a['events'])
        event_hir = a['events_hir'][event_jap]
        event_rus = a['end_events2'][event_jap]
        jap = [event_jap, 'では', rand_copula]
        hir = ''.join([event_hir, 'では', rand_copula])
        rus = ' '.join([event_rus, '- нельзя', rus_copula])
    jap = ''.join(jap)
    return jap, hir, rus, expression_prohibition.__name__

def expression_obligation():
    print('expression_obligation')
    rand = random.randint(0, 1)
    if rand == 0:
        base = 'なければ'
        rand1 = random.randint(0, 2)
        rus_copula1 = '(формальный стиль'
        if rand1 == 0:
            rand_copula = 'いけない'
            rus_copula = (
                ', мягкая форма, так нужно делать по правилам, но не так строго как по законам)'
                )
        elif rand1 == 1:
            rand_copula = 'ならない'
            rus_copula = ', самая строгая форма, связанная с законами)'
        else:
            rand_copula = 'だめだ'
            rus_copula = ', самая грубая, между близкими)'
    else:
        base = 'なくては'
        rand_copula = 'いけない'
        rus_copula = (
            ', мягкая форма, так нужно делать по правилам, но не так строго как по законам)'
            )
        rus_copula1 = '(разговорный стиль'
    rand = random.randint(0, 2)
    if rand == 0:
        podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
        g = Glagols('glag_verb_stem', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][1]
        jap = [podl1, 'は', jap_podl, padez, glag_jap, form, base, base,
            rand_copula]
        hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form,
            base, rand_copula])
        rus = ' '.join([podl1_rus, 'должен/на', glag_rus, padez_rus,
            jap_podl_rus, rus_copula1, rus_copula])
    elif rand == 1:
        ran_sush = ran(a['small object'])
        ran_sush_hir = a['small object_hir'][ran_sush]
        ran_sush_rus = a['small object'][ran_sush]
        jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(
            ran_sush, 'only_sush', 'all')
        jap = [ran_sush, 'は', jap1, 'く', rand_copula]
        hir = ''.join([ran_sush_hir, 'は', hir1, 'く', rand_copula])
        rus = ' '.join([rus1, 'должен/на быть', ran_sush_rus, rus_copula1,
            rus_copula])
    else:
        event_jap = ran(a['events'])
        event_hir = a['events_hir'][event_jap]
        event_rus = a['events'][event_jap]
        jap = [event_jap, 'でなければ', rand_copula]
        hir = ''.join([event_hir, 'で', rand_copula])
        rus = ' '.join(['должен/на быть', event_rus, rus_copula1, rus_copula])
    jap = ''.join(jap)
    return jap, hir, rus, expression_obligation.__name__

def reason_happening():
    print('reason_happening')
    eve = ran(a['events'])
    eve_hir = a['events_hir'][eve]
    eve_rus = a['end_events2'][eve]
    reas = ran(a['reason_simple'])
    reas_hir = a['reason_simple_hir'][reas]
    reas_rus = a['reason_simple'][reas]
    jap = [reas, '場合、', eve, 'に行きます']
    hir = ''.join([reas_hir, 'ばあい、', eve_hir, 'に', 'いきます'])
    rus = ' '.join(['Если ', reas_rus, ', идите на(в)', eve_rus,
        '(в более формальных или официальных ситуациях, а также для описания правил, инструкций или условий.)'
        ])
    jap = ''.join(jap)
    return jap, hir, rus, reason_happening.__name__

def subordinate_clause_made():
    print('subordinate_clause_made')
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    g = Glagols('glag_budush', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    g2 = Glagols('glag_im_going_todo', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][3]
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form, 'まで、', jap_podl2,
        padez2, glag_jap2, form2]
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form,
        'まで、', jap_podl_hir2, padez2, glag_hir2, form2])
    rus = ' '.join(['До того, как ', podl1_rus, glag_rus, padez_rus,
        jap_podl_rus, ', я ', glag_rus2, padez_rus2, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, subordinate_clause_made.__name__

def service_word_sou():
    print('service_word_sou')
    g = Glagols('glag_past_one_moment2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][7]
    rand = random.randint(0, 1)
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form1, 'そうです']
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form1,
        'そうです'])
    rus = ' '.join(['Говорят, что', podl1_rus, glag_rus, padez_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, service_word_sou.__name__

def imperative_passive_voice():
    print('imperative_passive_voice')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][1]
    podl1, podl1_hir, podl1_rus = who_f('end_family3', 'end_know3', 'suff')
    if glag_jap in a['glagol_2_conjugation']:
        suff = 'させられました'
    elif form1 == 'さ' or form1 == 'さ(せ)':
        suff = 'せられました'
    else:
        suff = 'されました'
    dop = ''
    dop_rus = 'был заставлен/а'
    podl2, podl2_hir, podl2_rus = who_f('family', 'know_people', 'suff')
    jap = [podl2, 'は', podl1, 'に', jap_podl, padez, glag_jap, form1, suff, dop]
    hir = ''.join([podl2_hir, 'は', podl1_hir, 'に', jap_podl_hir, padez,
        glag_hir, form1, suff, dop])
    rus = ' '.join([podl2_rus, dop_rus, podl1_rus, glag_rus, padez_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, imperative_passive_voice.__name__

def time_form_in_tara_dara():
    print('time_form_in_tara_dara')
    rand0 = random.randint(0, 1)
    if rand0 == 0:
        mosi = 'もし'
        rus_expl = '(плюс выделение предположения говорящего)'
    else:
        mosi = ''
        rus_expl = ''
    rand = random.randint(0, 2)
    g1 = Glagols('glag_im_going_todo', 'all')
    (glag_jap1, glag_hir1, glag_rus1, jap_podl1, jap_podl_hir1,
        jap_podl_rus1, padez1, padez_rus1, rand_glag) = g1.main()
    if glag_jap1 == '聞_2' or glag_jap1 == '聞_1':
        glag_jap1 = '聞'
    form1 = a['glag_form'][glag_jap1][3]
    if rand == 0:
        podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
        g = Glagols('glag_budush', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][7]
        jap = [podl1, 'は', mosi, jap_podl, padez, glag_jap, form, 'ら、',
            jap_podl1, padez1, glag_jap1, form1]
        hir = ''.join([podl1_hir, 'は', mosi, jap_podl_hir, padez, glag_hir,
            form, 'ら、', jap_podl_hir1, padez1, glag_hir1, form1])
        rus = ' '.join(['Если ', podl1_rus, glag_rus, padez_rus,
            jap_podl_rus, ', ', glag_rus1, padez_rus1, jap_podl_rus1,
            '(Разговорная форма)', rus_expl])
    elif rand == 1:
        ran_sush = ran(a['small object'])
        ran_sush_hir = a['small object_hir'][ran_sush]
        ran_sush_rus = a['small object'][ran_sush]
        jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(
            ran_sush, 'only_sush', 'all')
        jap = [mosi, ran_sush, 'は', jap1, 'かったら、', jap_podl1, padez1,
            glag_jap1, form1]
        hir = ''.join([mosi, ran_sush_hir, 'は', hir1, 'かったら、',
            jap_podl_hir1, padez1, glag_hir1, form1])
        rus = ' '.join(['Если ', rus1, ran_sush_rus, ', ', glag_rus1,
            padez_rus1, jap_podl_rus1, '(Разговорная форма)', rus_expl])
    else:
        event_jap = ran(a['events'])
        event_hir = a['events_hir'][event_jap]
        event_rus = a['events'][event_jap]
        jap = [mosi, event_jap, 'だったら、', jap_podl1, padez1, glag_jap1, form1]
        hir = ''.join([mosi, event_hir, 'だったら、', jap_podl_hir1, padez1,
            glag_hir1, form1])
        rus = ' '.join(['Если будет', event_rus, ', ', glag_rus1,
            padez_rus1, jap_podl_rus1, '(Разговорная форма)', rus_expl])
    jap = ''.join(jap)
    return jap, hir, rus, time_form_in_tara_dara.__name__

def time_form_in_tara_dara_2():
    print('time_form_in_tara_dara_2')
    rand = random.randint(0, 2)
    event_jap = ran(a['events'])
    event_hir = a['events_hir'][event_jap]
    event_rus = a['events'][event_jap]
    rand = random.randint(0, 3)
    if rand == 0:
        g = Glagols('glag_past_one_moment2', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][7]
        jap = [event_jap, 'だったら、', jap_podl, padez, glag_jap, form]
        hir = ''.join([event_hir, 'だったら、', jap_podl_hir, padez, glag_hir, form]
            )
        rus = ' '.join(['Когда был/о ', event_rus, ', я неожиданно ',
            glag_rus, padez_rus, jap_podl_rus, '(Разговорная форма)'])
    elif rand == 1:
        g1 = Glagols('glag_past_one_moment2', 'all')
        (glag_jap1, glag_hir1, glag_rus1, jap_podl1, jap_podl_hir1,
            jap_podl_rus1, padez1, padez_rus1, rand_glag) = g1.main()
        form1 = a['glag_form'][glag_jap1][7]
        g = Glagols('glag_past_one_moment2', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][7]
        jap = [jap_podl, padez, glag_jap, form, 'ら、', jap_podl1, padez1,
            glag_jap1, form1, 'だろう']
        hir = ''.join([jap_podl_hir, padez, glag_hir, form, 'ら、',
            jap_podl_hir1, padez1, glag_hir1, form1, 'だろう'])
        rus = ' '.join(['Если бы', glag_rus, padez_rus, jap_podl_rus,
            ', то наверное', glag_rus1, 'бы', padez_rus1, jap_podl_rus1,
            '(Разговорная форма)'])
    elif rand == 2:
        g = Glagols('glag_masyou', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        jap = [event_jap, 'だったら、', jap_podl, padez, glag_jap, form, 'ください']
        hir = ''.join([event_hir, 'だったら、', jap_podl_hir, padez, glag_hir,
            form, 'ください'])
        rus = ' '.join(['Если будет ', event_rus, ', то давайте', glag_rus,
            padez_rus, jap_podl_rus, '(Разговорная форма)'])
    else:
        g = Glagols('glag_verb_stem_2', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][7]
        jap = [jap_podl, padez, glag_jap, form, 'らいいです']
        hir = ''.join([jap_podl_hir, padez, glag_hir, form, 'らいいです'])
        rus = ' '.join(['Следует', glag_rus, padez_rus, jap_podl_rus,
            '(Разговорная форма)'])
    jap = ''.join(jap)
    return jap, hir, rus, time_form_in_tara_dara_2.__name__

def similary_youna():
    print('similary_youna')
    g = Glagols('glag_now', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][2]
    rand = random.randint(0, 1)
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    podl2, podl2_hir, podl2_rus = who_f('family', 'know_people', 'suff')
    if rand == 0:
        dop = 'まるで'
        dop_rus = ', совсем'
    else:
        dop = ''
        dop_rus = ''
    rand2 = random.randint(0, 1)
    if rand2 == 0:
        jap = [podl1, 'は', dop, podl2, 'のように', jap_podl, padez, glag_jap,
            form1, 'ます']
        hir = ''.join([podl1_hir, 'は', dop, podl2_hir, 'のように', jap_podl_hir,
            padez, glag_hir, form1, 'ます'])
        rus = ' '.join([podl1_rus, glag_rus, padez_rus, jap_podl_rus,
            dop_rus, 'как', podl2_rus, '(делает наподобие, похоже)'])
    else:
        nation = ran(a['nationality'])
        nation_hir = a['nationality_hir'][nation]
        nation_rus = a['nationality'][nation]
        jap = [podl1, 'は', dop, podl2, 'のような', nation, 'です']
        hir = ''.join([podl1_hir, 'は', dop, podl2_hir, 'のような', nation_hir,
            'です'])
        rus = ' '.join([podl1_rus, dop_rus, 'как', nation_rus, '(похож)'])
    jap = ''.join(jap)
    return jap, hir, rus, similary_youna.__name__

def similary_youna_target():
    print('similary_youna_target')
    g = Glagols('glag_past_one_moment', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    form1 = a['glag_form'][glag_jap][3]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    podl2, podl2_hir, podl2_rus = who_f('family', 'know_people', 'suff')
    g2 = Glagols('glag_past_one_moment2', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    form2 = a['glag_form'][glag_jap2][2]
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form1, 'ように', podl2, 'は',
        jap_podl2, padez2, glag_jap2, form2, 'ました']
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form1,
        'ように', podl2_hir, 'は', jap_podl_hir2, padez2, glag_hir2, form2, 'ました'])
    rus = ' '.join([podl1_rus, glag_rus, padez_rus, jap_podl_rus, ', чтобы',
        podl2_rus, glag_rus2, padez_rus2, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, similary_youna_target.__name__

def strive_to_do():
    print('strive_to_do')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    podl, podl_hir, podl_rus = who_f('family', 'know_people', 'suff')
    adverb_list = ['一生懸命', '熱心に', 'できるだけ']
    adverb_hir_list = ['いっしょうけんめい', 'ねっしんに', 'できるだけ']
    adverb_rus_list = ['изо всех сил', 'усердно', 'по мере возможности']
    if random.choice([True, False]):
        adverb_index = random.randint(0, len(adverb_list) - 1)
        adverb = adverb_list[adverb_index]
        adverb_hir = adverb_hir_list[adverb_index]
        adverb_rus = adverb_rus_list[adverb_index]
    else:
        adverb = adverb_hir = adverb_rus = ''
    jap = [podl, 'は', adverb, jap_podl, padez, glag_jap, form, 'ように', 'します']
    hir = ''.join([podl_hir, 'は', adverb_hir, jap_podl_hir, padez, glag_hir,
        form, 'ように', 'します'])
    rus = ' '.join([podl_rus, adverb_rus, 'старается', glag_rus, padez_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, strive_to_do.__name__

def became_capable_youni():
    print('became_capable_youni')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][3]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form1, 'ように', 'なり', 'ました']
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form1,
        'ように', 'なり', 'ました'])
    rus = ' '.join([podl1_rus, 'начал', glag_rus, padez_rus, jap_podl_rus,
        '(начало совершения действия в силу естественного развития событий)'])
    jap = ''.join(jap)
    return jap, hir, rus, became_capable_youni.__name__

def prop_ha_sou():
    print('prop_ha_sou')
    kono = ran(a['uno'])
    kono_rus = a['uno'][kono]
    ran_sush = ran(a['small object'])
    ran_sush_hir = a['small object_hir'][ran_sush]
    ran_sush_rus = a['small object'][ran_sush]
    jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(ran_sush
        , 'only_sush', 'all')
    if jap1 == 'い' or jap1 == 'よ':
        jap1 = 'よさ'
        hir1 = 'よさ'
    rand = random.randint(0, 1)
    if rand == 0:
        ne = 'くなさ'
        ne_rus = 'не'
    else:
        ne = ''
        ne_rus = ''
    rand2 = random.randint(0, 1)
    if rand2 == 0:
        jap = [kono, ran_sush, 'は', jap1, ne, 'そうです']
        hir = ''.join([kono, ran_sush_hir, 'は', hir1, ne, 'そうです'])
        rus = ' '.join([kono_rus, ran_sush_rus, ne_rus,
            'выглядит как (кажется)', rus1,
            '. (проявление какого либо качества внешне объективно)'])
    else:
        g = Glagols('glag_past_one_moment', 'choose', ['accusative'])
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form1 = a['glag_form'][glag_jap][2]
        podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
        jap = [podl1, 'は', jap1, ne, 'そうに', jap_podl, padez, glag_jap,
            form1, 'ました']
        hir = ''.join([podl1_hir, 'は', hir1, ne, 'そうに', jap_podl_hir, padez,
            glag_hir, form1, 'ました'])
        rus = ' '.join([podl1_rus, glag_rus, jap_podl_rus, ne_rus,
            ', который/ая совсем как', rus1,
            '. (проявление какого либо качества внешне объективно)'])
    jap = ''.join(jap)
    return jap, hir, rus, prop_ha_sou.__name__

def bakari():
    print('bakari')
    g = Glagols('glag_past_one_moment', 'choose', ['accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][7]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'は', jap_podl, 'ばかり', glag_jap, form1]
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, 'ばかり', glag_hir, form1])
    rus = ' '.join([podl1_rus, glag_rus, 'только', jap_podl_rus,
        '(хотя есть другие предметы, имеющие признак который имеет значение для говорящего)'
        ])
    jap = ''.join(jap)
    return jap, hir, rus, bakari.__name__

def subordinate_clause_uti():
    print('subordinate_clause_uti')
    podl1 = ran(a['adj_non_predicative_endings'])
    podl1_hir = podl1
    podl1_rus = a['adj_non_predicative_endings'][podl1]
    g2 = Glagols('glag_verb_stem', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][3]
    jap = [podl1, 'なうちに、', jap_podl2, padez2, glag_jap2, form2]
    hir = ''.join([podl1_hir, 'なうちに、', jap_podl_hir2, padez2, glag_hir2, form2]
        )
    rus = ' '.join(['Пока', podl1_rus, ', я буду', glag_rus2, padez_rus2,
        jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, subordinate_clause_uti.__name__

def auxiliary_kuru():
    print('auxiliary_kuru')
    podl, podl_hir, podl_rus = who_f('family', 'know_people', 'suff')
    usage_type = random.choice(['development', 'appearance'])
    if usage_type == 'development':
        g = Glagols('glag_now', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        time_expressions = ['最近', 'だんだん', 'ここ数年']
        time_expressions_hir = ['さいきん', 'だんだん', 'ここすうねん']
        time_expressions_rus = ['В последнее время', 'Постепенно',
            'За последние несколько лет']
        time_index = random.randint(0, len(time_expressions) - 1)
        time_expr = time_expressions[time_index]
        time_expr_hir = time_expressions_hir[time_index]
        time_expr_rus = time_expressions_rus[time_index]
        jap = [podl, 'は', time_expr, jap_podl, padez, glag_jap, form, 'きています']
        hir = ''.join([podl_hir, 'は', time_expr_hir, jap_podl_hir, padez,
            glag_hir, form, 'きています'])
        rus = ' '.join([time_expr_rus, podl_rus, glag_rus, padez_rus,
            jap_podl_rus, '(это действие развивалось до настоящего момента)'])
    else:
        g = Glagols('glag_verb_stem', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        jap = [podl, 'は', jap_podl, padez, glag_jap, form, 'きました']
        hir = ''.join([podl_hir, 'は', jap_podl_hir, padez, glag_hir, form,
            'きました'])
        rus = ' '.join([podl_rus, 'начал(а)', glag_rus, padez_rus,
            jap_podl_rus, '(указание на начало действия)'])
    jap = ''.join(jap)
    return jap, hir, rus, auxiliary_kuru.__name__

def auxiliary_iku():
    print('auxiliary_iku')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][6]
    podl, podl_hir, podl_rus = who_f('family', 'know_people', 'suff')
    usage_type = random.choice(['gradual_change', 'continuous_action'])
    if usage_type == 'gradual_change':
        change_expressions = ['だんだん', 'しだいに', 'ゆっくり']
        change_expressions_hir = ['だんだん', 'しだいに', 'ゆっくり']
        change_expressions_rus = ['Постепенно', 'Со временем', 'Медленно']
        change_index = random.randint(0, len(change_expressions) - 1)
        change_expr = change_expressions[change_index]
        change_expr_hir = change_expressions_hir[change_index]
        change_expr_rus = change_expressions_rus[change_index]
        jap = [podl, 'は', change_expr, jap_podl, padez, glag_jap, form, '行きます']
        hir = ''.join([podl_hir, 'は', change_expr_hir, jap_podl_hir, padez,
            glag_hir, form, 'いきます'])
        rus = ' '.join([change_expr_rus, podl_rus, 'продолжает', glag_rus,
            padez_rus, jap_podl_rus, '(указание на постепенное изменение)'])
    else:
        time_expressions = ['これから', 'この先', 'ずっと']
        time_expressions_hir = ['これから', 'このさき', 'ずっと']
        time_expressions_rus = ['Отныне', 'В будущем', 'Всё время']
        time_index = random.randint(0, len(time_expressions) - 1)
        time_expr = time_expressions[time_index]
        time_expr_hir = time_expressions_hir[time_index]
        time_expr_rus = time_expressions_rus[time_index]
        jap = [podl, 'は', time_expr, jap_podl, padez, glag_jap, form, '行きます']
        hir = ''.join([podl_hir, 'は', time_expr_hir, jap_podl_hir, padez,
            glag_hir, form, 'いきます'])
        rus = ' '.join([podl_rus, time_expr_rus, 'будет продолжать',
            glag_rus, padez_rus, jap_podl_rus,
            '(указание на продолжающееся действие)'])
    jap = ''.join(jap)
    return jap, hir, rus, auxiliary_iku.__name__

def distancing_in_time():
    print('distancing_in_time')
    sentence_type = random.choice(['forgetting', 'not_seeing'])
    podl, podl_hir, podl_rus = who_f('family', 'know_people', 'suff')
    if sentence_type == 'forgetting':
        object_dict = random.choice(('telling', 'events'))
        obj_jap = ran(a[object_dict])
        obj_hir = a[f'{object_dict}_hir'][obj_jap]
        obj_rus = a[object_dict][obj_jap]
        jap = [podl, 'は', obj_jap, 'を', '忘れて', 'いきます']
        hir = ''.join([podl_hir, 'は', obj_hir, 'を', 'わすれて', 'いきます'])
        rus = ' '.join([podl_rus, 'постепенно забывает', obj_rus,
            '(отдаление во времени)'])
    else:
        object_dict = random.choice(('buildings', 'outsides'))
        obj_jap = ran(a[object_dict])
        obj_hir = a[f'{object_dict}_hir'][obj_jap]
        obj_rus = a[object_dict][obj_jap]
        jap = [obj_jap, 'が', '見えなく', 'なって', 'いきます']
        hir = ''.join([obj_hir, 'が', 'みえなく', 'なって', 'いきます'])
        rus = ' '.join([obj_rus, 'постепенно перестает быть видным',
            '(отдаление во времени)'])
    jap = ''.join(jap)
    return jap, hir, rus, distancing_in_time.__name__

def connection_with_ba():
    print('connection_with_ba')
    rand = random.choice(('move', 'accusative', 'address', 'withs'))
    g = Glagols('glag_now', 'choose', [rand])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][4]
    podl, podl_hir, podl_rus = who_f('family', 'know_people', 'suff')
    g2 = Glagols('glag_now', 'choose', [rand])
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][6]
    jap = [podl, 'は', jap_podl, 'も', glag_jap, form, 'ば、', jap_podl2, 'も',
        glag_jap2, form2, 'います']
    hir = ''.join([podl_hir, 'は', jap_podl_hir, 'も', glag_hir, form, 'ば、',
        jap_podl_hir2, 'も', glag_hir2, form2, 'います'])
    rus = ' '.join([podl_rus, 'не только ', glag_rus, padez_rus,
        jap_podl_rus, ', но и ', glag_rus2, padez_rus2, jap_podl_rus2,
        '(контрастные действия, параллельные, может быть неожиданность)'])
    jap = ''.join(jap)
    return jap, hir, rus, connection_with_ba.__name__

def condition_with_nara():
    print('condition_with_nara')
    rand = random.choice(('move', 'accusative', 'address', 'withs'))
    rand2 = random.randint(0, 2)
    no = ''
    form_infirst = 3
    rus1 = 'Если (правда)'
    if rand2 == 0:
        time1 = 'glag_im_going_todo'
        time2 = 'glag_im_going_todo'
        copula = ''
        form_insecond = 3
        rus_expl = '(говорящий стремится подчеркнуть реальность события)'
    elif rand2 == 1:
        time1 = 'glag_kudasai'
        time2 = 'glag_kudasai'
        copula = 'ください'
        form_insecond = 6
        rand3 = random.randint(0, 1)
        if rand3 == 0:
            rus_expl = '(передача просьбы в условном предложении)'
        else:
            no = 'の'
            rus_expl = (
                '(передача просьбы в условном предложении + условие высказывается на основе сообщения, сделанного собеседником)'
                )
    else:
        time1 = 'glag_past_one_moment'
        time2 = 'glag_past_one_moment'
        copula = 'でしょう'
        form_insecond = 7
        form_infirst = 7
        rus_expl = ''
        rus1 = 'Если бы (правда)'
    g = Glagols(time1, 'choose', [rand])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][form_infirst]
    g2 = Glagols(time2, 'choose', [rand])
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][form_insecond]
    jap = [jap_podl, padez, glag_jap, form, no, 'なら、', jap_podl2, padez2,
        glag_jap2, form2, copula]
    hir = ''.join([jap_podl_hir, padez, glag_hir, form, no, 'なら、',
        jap_podl_hir2, padez2, glag_hir2, form2, copula])
    rus = ' '.join([rus1, glag_rus, padez_rus, jap_podl_rus, ', то ',
        glag_rus2, padez_rus2, jap_podl_rus2, rus_expl])
    jap = ''.join(jap)
    return jap, hir, rus, condition_with_nara.__name__

def probability_you():
    print('probability_you')
    g = Glagols('glag_nast_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    form = a['glag_form'][glag_jap][3]
    rand = random.randint(0, 1)
    if rand == 0:
        copula = 'よう'
        rus_expl = (
            '(предположение на основе какого то опыта, знаниях, НЕ разговорый стиль)'
            )
    else:
        copula = 'みたい'
        rus_expl = (
            '(предположение на основе какого то опыта, знаниях, разговорый стиль)'
            )
    jap = [jap_who, 'は', jap_podl, padez, glag_jap, form, copula, 'です']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, padez, glag_hir, form,
        copula, 'です'])
    rus = ' '.join(['похоже на то, что,', rus_podl_who, padez_rus,
        jap_podl_rus, glag_rus, rus_expl])
    jap = ''.join(jap)
    return jap, hir, rus, probability_you.__name__

def probability_sou():
    print('probability_sou')
    g = Glagols('glag_nast_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    form = a['glag_form'][glag_jap][2]
    jap = [jap_who, 'は', jap_podl, padez, glag_jap, form, 'そう', 'です']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, padez, glag_hir, form,
        'そう', 'です'])
    rus = ' '.join(['Судя по ощущениям,', rus_podl_who, padez_rus,
        jap_podl_rus, glag_rus,
        '(предположение на ощущениях, чувствах, наблюдениях)'])
    jap = ''.join(jap)
    return jap, hir, rus, probability_sou.__name__

def probability_rasii():
    print('probability_rasii')
    g = Glagols('glag_nast_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    form = a['glag_form'][glag_jap][3]
    jap = [jap_who, 'は', jap_podl, padez, glag_jap, form, 'らしい', 'です']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, padez, glag_hir, form,
        'らしい', 'です'])
    rus = ' '.join(['Судя по косвенной информации,', rus_podl_who,
        padez_rus, jap_podl_rus, glag_rus,
        '(субъективное предположение, слухи, инфа из вторых рук)'])
    jap = ''.join(jap)
    return jap, hir, rus, probability_rasii.__name__

def measure_degree_hodo_kurai():
    print('measure_degree_hodo_kurai')
    podl1 = ran(a['adj_non_predicative_endings'])
    podl1_hir = podl1
    podl1_rus = a['adj_non_predicative_endings'][podl1]
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    rand = random.randint(0, 1)
    if rand == 0:
        copula = 'くらい、'
        rus_expl = '(сильная степень сравнения)'
    else:
        copula = 'ほど、'
        rus_expl = '(средняя степень сравнения)'
    jap = [jap_podl, padez, glag_jap, form, 'たい', copula, podl1, 'になった']
    hir = ''.join([jap_podl_hir, padez, glag_hir, form, 'たい', copula,
        podl1_hir, 'になった'])
    rus = ' '.join(['Стало так', podl1_rus, ', что захотелось', glag_rus,
        padez_rus, jap_podl_rus, rus_expl])
    jap = ''.join(jap)
    return jap, hir, rus, measure_degree_hodo_kurai.__name__

def meaning_wake():
    print('meaning_wake')
    podl1 = ran(a['adj_non_predicative_endings'])
    podl1_hir = podl1
    podl1_rus = a['adj_non_predicative_endings'][podl1]
    g = Glagols('glag_now', 'choose', ['accusative', 'address', 'withs'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    jap = ['ここで', podl1, 'なわけです、', jap_who, 'は', jap_podl, padez, glag_jap,
        form]
    hir = ''.join(['ここで', podl1_hir, 'なわけです、', hir_podl_who, 'は',
        jap_podl_hir, padez, glag_hir, form])
    rus = ' '.join(['Дело в том, что там', podl1_rus, ', поэтому',
        rus_podl_who, 'там', jap_podl_rus, padez_rus, glag_rus])
    jap = ''.join(jap)
    return jap, hir, rus, meaning_wake.__name__

def have_to_wazu():
    print('have_to_wazu')
    g = Glagols('glag_budush', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    t = Times('choose', ['we', 'da_f', 'vov'])
    time_jap, time_hir, time_rus = t.main()
    jap = [time_jap, jap_who, 'は', jap_podl, padez, glag_jap, form, 'はずです']
    hir = ''.join([time_hir, hir_podl_who, 'は', jap_podl_hir, padez,
        glag_hir, form, 'はずです'])
    rus = ' '.join([time_rus, rus_podl_who, ', должно быть,', glag_rus,
        padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, have_to_wazu.__name__

def time_jyouzu():
    print('time_jyouzu')
    g = Glagols('glag_past_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    g2 = Glagols('glag_past_one_moment2', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g2.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][7]
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    jap = [jap_who, 'は', jap_podl, padez, glag_jap, form, '上で、', jap_podl2,
        padez2, glag_jap2, form2]
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, padez, glag_hir, form,
        'うえで、', jap_podl_hir2, padez2, glag_hir2, form2])
    rus = ' '.join(['Когда (пока)', rus_podl_who, glag_rus, padez_rus,
        jap_podl_rus, ', он/а ', glag_rus2, padez_rus2, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, time_jyouzu.__name__

def i_want_hosii():
    print('i_want_hosii')
    rand = random.randint(0, 1)
    if rand == 0:
        g = Glagols('glag_past_one_moment', 'all')
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        jap = ['だれに', jap_podl, padez, glag_jap, form, 'でほしい']
        hir = ''.join(['だれに', jap_podl_hir, padez, glag_hir, form, 'うえで、'])
        rus = ' '.join(['Мне хочется, чтобы кто нибудь', glag_rus,
            padez_rus, jap_podl_rus])
    else:
        event_jap = ran(a['events'])
        event_hir = a['events_hir'][event_jap]
        event_rus = a['events'][event_jap]
        glag_begin = ran(a['glagol']['not_trans_fast_ev'])
        glag_begin_hir = a['glagol']['not_trans_fast_ev'][glag_begin]
        glag_begin_rus = a['glag_past_one_moment'][glag_begin]
        form = a['glag_form'][glag_begin][6]
        jap = [event_jap, 'が', glag_begin, form, 'でほしい']
        hir = ''.join([event_hir, 'が', glag_begin_hir, form, 'でほしい'])
        rus = ' '.join(['Мне хочется, чтобы', event_rus, glag_begin_rus])
    jap = ''.join(jap)
    return jap, hir, rus, i_want_hosii.__name__

def state_mama():
    print('state_mama')
    kono = ran(a['uno'])
    kono_rus = a['uno'][kono]
    ran_sush = ran(a['small object'])
    ran_sush_hir = a['small object_hir'][ran_sush]
    ran_sush_rus = a['small object'][ran_sush]
    jap1, hir1, rus1, jap1_ne, jap1_ne_hir, jap1_ne_rus = prop_no_sush(ran_sush
        , 'only_sush', 'all')
    jap = [kono, ran_sush, 'は', jap1, 'ままです']
    hir = ''.join([kono, ran_sush_hir, 'は', hir1, 'ままです'])
    rus = ' '.join([kono_rus, ran_sush_rus, 'всё еще', rus1,
        '. (так, как есть в таком состоянии)'])
    jap = ''.join(jap)
    return jap, hir, rus, state_mama.__name__

def reason_tame():
    print('reason_tame')
    reas = ran(a['reasons'])
    reas_hir = a['reasons_hir'][reas]
    reas_rus = a['reasons'][reas]
    g = Glagols('glag_past_one_moment', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][1]
    jap = [reas, 'ため、私', 'は', jap_podl, padez, glag_jap, form, 'かった']
    hir = ''.join([reas_hir, 'ため、', 'わたし', 'は', jap_podl_hir, padez,
        glag_hir, form, 'かった'])
    rus = ' '.join(['Из-за того, что', reas_rus, ', я не ', glag_rus,
        padez_rus, jap_podl_rus,
        '(объективное суждение, глагол глав. предлож выражает неконтролируемое действие)'
        ])
    jap = ''.join(jap)
    return jap, hir, rus, reason_tame.__name__

def compulsion_yorihoka():
    print('compulsion_yorihoka')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap = [jap_podl, padez, glag_jap, form, 'よりほはない ']
    hir = ''.join([jap_podl_hir, padez, glag_hir, 'よりほはない '])
    rus = ' '.join(['Ничего не остается, кроме как', glag_rus, padez_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, compulsion_yorihoka.__name__

def he_doing_onky_that():
    print('he_doing_onky_that')
    g = Glagols('glag_past_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][7]
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    jap = [jap_who, 'は', jap_podl, padez, glag_jap, form, 'きりでした']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, padez, glag_hir, form,
        'きりでした'])
    rus = ' '.join([rus_podl_who, 'только и делал, что', glag_rus,
        padez_rus, jap_podl_rus, '(и больше ничего)'])
    jap = ''.join(jap)
    return jap, hir, rus, he_doing_onky_that.__name__

def politeness_imenn_skaz():
    print('politeness_1')
    jap_who = ran(a['names'])
    rus_who = a['names'][jap_who] + '-сан'
    hir_who = a['names_hir'][jap_who] + 'さん'
    jap_who = jap_who + 'さん'
    proff = ran(a['proffession'])
    proff_hir = a['proffession_hir'][proff]
    proff_rus = a['proffession'][proff]
    jap = [jap_who, 'は', proff, 'でいらっしゃいます']
    hir = ''.join([hir_who, 'は', proff_hir, 'でいらっしゃいます'])
    rus = ' '.join([rus_who, '-', proff_rus, '(учтивая форма)'])
    jap = ''.join(jap)
    return jap, hir, rus, politeness_imenn_skaz.__name__

def politeness_imenn_skaz_me():
    print('politeness_1')
    intro_type = random.choice(['profession', 'nationality', 'workplace'])
    if intro_type == 'profession':
        prof = ran(a['profession'])
        prof_hir = a['profession_hir'][prof]
        prof_rus = a['profession'][prof]
        jap = ['私', 'は', prof, 'で', 'ございます']
        hir = ''.join(['わたくし', 'は', prof_hir, 'で', 'ございます'])
        rus = ' '.join(['Я (с большим почтением)', prof_rus])
    elif intro_type == 'nationality':
        country = ran(a['nationality'])
        country_hir = a['nationality_hir'][country]
        country_rus = a['nationality'][country]
        jap = ['私', 'は', country, 'で', 'ございます']
        hir = ''.join(['わたくし', 'は', country_hir, 'で', 'ございます'])
        rus = ' '.join(['Я (с большим почтением) ', country_rus])
    elif intro_type == 'workplace':
        workplace = ran(a['buildings'])
        workplace_hir = a['buildings_hir'][workplace]
        workplace_rus = a['buildings'][workplace]
        jap = ['私', 'の', 'しょくば', 'は', workplace, 'で', 'ございます']
        hir = ''.join(['わたくし', 'の', 'しょくば', 'は', workplace_hir, 'で', 'ございます'])
        rus = ' '.join(['Мое (с большим почтением) место работы -',
            workplace_rus])
    jap = ''.join(jap)
    return jap, hir, rus, politeness_imenn_skaz_me.__name__

def politeness_2_3_action_special_verb():
    print('politeness_2_3_action')
    g = Glagols('glag_now', 'all')
    glag_jap = ''
    while glag_jap not in a['keigo_dict']:
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
    glag_jap_n = a['keigo_dict'][glag_jap][0]
    glag_hir_n = a['keigo_dict'][glag_jap][1]
    jap_who = ran(a['names'])
    rus_who = a['names'][jap_who] + '-сан'
    hir_who = a['names_hir'][jap_who] + 'さん'
    jap_who = jap_who + 'さん'
    jap = [jap_who, 'は', jap_podl, padez, glag_jap_n]
    hir = ''.join([hir_who, 'は', jap_podl_hir, padez, glag_hir_n])
    rus = ' '.join([rus_who, glag_rus, padez_rus, jap_podl_rus,
        '(учтивая форма)'])
    jap = ''.join(jap)
    return jap, hir, rus, politeness_2_3_action_special_verb.__name__

def politeness_2_3_action_special_form():
    print('politeness_2_3_action_special_form')
    g = Glagols('glag_now', 'all')
    rand = random.randint(0, 2)
    rus_expl = ''
    if rand == 0:
        while True:
            (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir,
                jap_podl_rus, padez, padez_rus, rand_glag) = g.main()
            if glag_jap not in a['keigo_dict'] and glag_jap not in a[
                'kango_verbs']:
                break
        form = a['glag_form'][glag_jap][2]
        copula = 'になる'
        pref = 'お'
    elif rand == 1:
        while True:
            (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir,
                jap_podl_rus, padez, padez_rus, rand_glag) = g.main()
            if glag_jap in a['kango_verbs']:
                break
        form = ''
        copula = 'になる'
        pref = 'ご'
    else:
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][1]
        copula = 'れる'
        pref = ''
        rus_expl = 'не самая высокая'
    jap_who = ran(a['names'])
    rus_who = a['names'][jap_who] + '-сан'
    hir_who = a['names_hir'][jap_who] + 'さん'
    jap_who = jap_who + 'さん'
    jap = [jap_who, 'は', jap_podl, padez, pref, glag_jap, form, copula]
    hir = ''.join([hir_who, 'は', jap_podl_hir, padez, pref, glag_hir, form,
        copula])
    rus = ' '.join([rus_who, glag_rus, padez_rus, jap_podl_rus,
        '(учтивая форма, ', rus_expl, ')'])
    jap = ''.join(jap)
    return jap, hir, rus, politeness_2_3_action_special_form.__name__

def politeness_me_action_special_verb():
    print('politeness_me_action_special_verb')
    g = Glagols('glag_im_doing', 'all')
    glag_jap = ''
    while glag_jap not in a['keigo_dict_me']:
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
    glag_jap_n = a['keigo_dict_me'][glag_jap][0]
    glag_hir_n = a['keigo_dict_me'][glag_jap][1]
    jap = ['私', 'は', jap_podl, padez, glag_jap_n]
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, glag_hir_n])
    rus = ' '.join(['Я', glag_rus, padez_rus, jap_podl_rus,
        '(учтивая форма, о самом себе)'])
    jap = ''.join(jap)
    return jap, hir, rus, politeness_me_action_special_verb.__name__

def politeness_me_action_special_form():
    print('politeness_me_action_special_form')
    g = Glagols('glag_im_doing', 'all')
    rand = random.randint(0, 2)
    rus_expl = ''
    if rand == 0:
        while True:
            (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir,
                jap_podl_rus, padez, padez_rus, rand_glag) = g.main()
            print('glag_jap', glag_jap)
            if glag_jap not in a['keigo_dict_me'] and glag_jap not in a[
                'kango_verbs']:
                break
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][2]
        copula = 'いたす'
        pref = 'お'
    elif rand == 1:
        while True:
            (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir,
                jap_podl_rus, padez, padez_rus, rand_glag) = g.main()
            if glag_jap in a['kango_verbs']:
                break
        form = ''
        copula = 'いたす'
        pref = 'ご'
    else:
        (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
            padez, padez_rus, rand_glag) = g.main()
        if glag_jap == '聞_2' or glag_jap == '聞_1':
            glag_jap = '聞'
        form = a['glag_form'][glag_jap][6]
        copula = 'おります'
        pref = ''
        rus_expl = ', длительный вид'
    jap = ['私', 'は', jap_podl, padez, pref, glag_jap, form, copula]
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, pref, glag_hir, form,
        copula])
    rus = ' '.join(['Я', glag_rus, padez_rus, jap_podl_rus,
        '(учтивая форма', rus_expl, ')'])
    jap = ''.join(jap)
    return jap, hir, rus, politeness_me_action_special_form.__name__

def politeness_there_build():
    print('politeness_there_build')
    jap_w = ran(a['buildings'])
    hir_w = a['buildings_hir'][jap_w]
    rus_w = a['buildings'][jap_w]
    jap = [jap_w, 'はそこにございます']
    jap_hir = ''.join([hir_w, 'はそこにございます'])
    rus_iru = ''.join([rus_w, ' находится там',
        '(учтивая форма, работник оттуда говорит об этом месте)'])
    jap = ''.join(jap)
    return jap, jap_hir, rus_iru, politeness_there_build.__name__

def politeness_there_i():
    print('politeness_there_i')
    jap_w = ran(a['buildings'])
    hir_w = a['buildings_hir'][jap_w]
    rus_w = a['end_build4'][jap_w]
    jap = ['私', 'は', jap_w, 'におります']
    jap_hir = ''.join(['わたし', 'は', hir_w, 'におります'])
    rus_iru = ''.join(['Я нахожусь в', rus_w, '(учтивая форма)'])
    jap = ''.join(jap)
    return jap, jap_hir, rus_iru, politeness_there_i.__name__

def totomoni():
    print('totomoni')
    jap_who, hir_podl_who, rus_podl_who = who_f('end_family4', 'end_know4',
        'suff')
    prop = ran(a['adj_non_predicative_hir'])
    prop_hir = a['adj_non_predicative_hir'][prop]
    prop_rus = a['adj_non_predicative_endings'][prop]
    jap = [jap_who, 'は', '来るとともに', prop, 'になった']
    hir = ''.join([hir_podl_who, 'は', 'くるとともに', prop_hir, 'になった'])
    rus = ' '.join(['С приходом', rus_podl_who, ' стало ', prop_rus])
    jap = ''.join(jap)
    return jap, hir, rus, totomoni.__name__

def simultaneity_kan():
    print('simultaneity_kan')
    g = Glagols('glag_past_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][6]
    g = Glagols('glag_past_post', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][6]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form1, 'いる間は', '、',
        jap_podl2, padez2, glag_jap2, form2, 'いる']
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form1,
        'いるまは', '、', jap_podl_hir2, padez2, glag_hir2, form2, 'いる'])
    rus = ' '.join(['В то время как (пока)', podl1_rus, glag_rus, padez_rus,
        jap_podl_rus, ', я', glag_rus2, padez_rus2, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, simultaneity_kan.__name__

def expression_of_impossibility():
    print('expression_of_impossibility')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap_who, hir_podl_who, rus_podl_who = who_f('family', 'know_people', 'suff'
        )
    jap = [jap_who, 'は', jap_podl, padez, glag_jap, form, 'わけにはいかない']
    hir = ''.join([hir_podl_who, 'は', jap_podl_hir, padez, glag_hir, form,
        'わけにはいかない'])
    rus = ' '.join([rus_podl_who, 'не может', glag_rus, padez_rus,
        jap_podl_rus,
        '(по независящим от него причинам, например социальные нормы и т.д.)'])
    jap = ''.join(jap)
    return jap, hir, rus, expression_of_impossibility.__name__

def there_no_other_things():
    print('there_no_other_things')
    g = Glagols('glag_past_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][3]
    g = Glagols('glag_past_post', 'all')
    (glag_jap2, glag_hir2, glag_rus2, jap_podl2, jap_podl_hir2,
        jap_podl_rus2, padez2, padez_rus2, rand_glag) = g.main()
    if glag_jap2 == '聞_2' or glag_jap2 == '聞_1':
        glag_jap2 = '聞'
    form2 = a['glag_form'][glag_jap2][6]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form1, 'ほか', '、',
        jap_podl2, padez2, glag_jap2, form2, 'いった']
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form1,
        'ほか', '、', jap_podl_hir2, padez2, glag_hir2, form2, 'いった'])
    rus = ' '.join(['Кроме того, что', podl1_rus, glag_rus, padez_rus,
        jap_podl_rus, ', он/а еще', glag_rus2, padez_rus2, jap_podl_rus2])
    jap = ''.join(jap)
    return jap, hir, rus, there_no_other_things.__name__

def consists_the_fact():
    print('consists_the_fact')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][3]
    podl1, podl1_hir, podl1_rus = who_f('end_family4', 'end_know4', 'suff')
    jap = [podl1, 'の', '仕事', 'は', jap_podl, padez, glag_jap, form1, 'ことにある']
    hir = ''.join([podl1_hir, 'の', 'しごと', 'は', jap_podl_hir, padez,
        glag_hir, form1, 'ことにある'])
    rus = ' '.join(['Работа', podl1_rus, 'в том, чтобы', glag_rus,
        padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, consists_the_fact.__name__

def ga_ski_doing():
    print('ga_ski_doing')
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][3]
    if random.randint(0, 1) == 0:
        ski = '好き'
        ski_hir = 'すき'
        ski_rus = 'любит'
    else:
        ski = 'きらい'
        ski_hir = 'きらい'
        ski_rus = 'не любит'
    jap = [podl1, 'は', jap_podl, padez, glag_jap, form1, 'ことが', ski, 'です']
    hir = ''.join([podl1_hir, 'は', jap_podl_hir, padez, glag_hir, form1,
        'ことが', ski_hir, 'です'])
    rus = ' '.join([podl1_rus, ski_rus, glag_rus, padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, ga_ski_doing.__name__

def permission_perform_action_simple():
    print('permission_perform_action_simple')
    g = Glagols('glag_verb_stem', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][6]
    jap = ['ここで', 'は', jap_podl, padez, glag_jap, form1, 'いません']
    hir = ''.join(['ここで', 'は', jap_podl_hir, padez, glag_hir, form1, 'いません'])
    rus = ' '.join(['Здесь нельзя', glag_rus, padez_rus, jap_podl_rus,
        '(простая форма запрета)'])
    jap = ''.join(jap)
    return jap, hir, rus, permission_perform_action_simple.__name__

def expression_obligation_myself():
    print('expression_obligation_myself')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][1]
    jap = ['私', 'は', jap_podl, padez, glag_jap, form, 'ないと (+いけません)']
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, glag_hir, form,
        'ないと (+いけません)'])
    rus = ' '.join(['Я должен', glag_rus, padez_rus, jap_podl_rus,
        '(мягкая форма, самообязывание)'])
    jap = ''.join(jap)
    return jap, hir, rus, expression_obligation_myself.__name__

def i_have_no_time():
    print('i_have_no_time')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap = ['私', 'は', jap_podl, padez, glag_jap, form, '時間', 'が', 'ありません']
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, glag_hir, form, 'じかん',
        'が', 'ありません'])
    rus = ' '.join(['У меня нет времени на то, чтобы', glag_rus, padez_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, i_have_no_time.__name__

def i_agreed_with_someone():
    print('i_have_no_time')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    podl1, podl1_hir, podl1_rus = who_f('end_family3', 'end_know3', 'suff')
    jap = ['私', 'は', podl1, 'と', jap_podl, padez, glag_jap, form, '約束', 'が',
        'あります']
    hir = ''.join(['わたし', 'は', podl1_hir, 'と', jap_podl_hir, padez,
        glag_hir, form, 'やくそく', 'が', 'あります'])
    rus = ' '.join(['Я договорился с', podl1_rus, glag_rus, padez_rus,
        jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, i_agreed_with_someone.__name__

def i_have_deal_for_it():
    print('i_have_deal_for_it')
    g = Glagols('glag_im_doing', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form = a['glag_form'][glag_jap][3]
    jap = ['私', 'は', jap_podl, padez, glag_jap, form, '用事', 'が', 'あります']
    hir = ''.join(['わたし', 'は', jap_podl_hir, padez, glag_hir, form, 'ようじ',
        'が', 'あります'])
    rus = ' '.join(['У меня есть дела, ради которых я', glag_rus, padez_rus,
        jap_podl_rus,
        '(дела подразумевают какую-то конкретную цель или задачу, а не общую цель)'
        ])
    jap = ''.join(jap)
    return jap, hir, rus, i_have_deal_for_it.__name__

def plan_youtei():
    print('plan_youtei')
    eve_jap = ran(a['events'])
    eve_hir = a['events_hir'][eve_jap]
    eve_rus = a['events'][eve_jap]
    t = Times('choose', ['we', 'da_f', 'vov'])
    time_jap, time_hir, time_rus = t.main()
    jap = [eve_jap, 'は', time_jap, 'の', '予定です']
    hir = ''.join([eve_hir, 'は', time_hir, 'の', 'よていです'])
    rus = ' '.join([eve_rus, 'планируется', time_rus])
    jap = ''.join(jap)
    return jap, hir, rus, plan_youtei.__name__

def he_said_write_thought():
    print('he_said_write_thought')
    name_jap = ran(a['name_of_buildings_duct'])
    name_hir = a['name_of_buildings_duct_hir'][name_jap]
    name_rus = a['name_of_buildings_duct'][name_jap]
    vars_jap = {'言': 'いい', '書': 'かき', '思': 'おもい', '答え': 'こたえ'}
    rand_vars = ran(vars_jap)
    vars_hir = vars_jap[rand_vars]
    var_rus = a['glag_past_one_moment2'][rand_vars]
    jap = ['彼', 'は', name_jap, 'と', rand_vars, 'ました']
    hir = ''.join(['かれ', 'は', name_hir, 'と', vars_hir, 'ました'])
    rus = ' '.join(['ОН', var_rus, name_rus])
    jap = ''.join(jap)
    return jap, hir, rus, he_said_write_thought.__name__

def this_means_that():
    print('this_means_that')
    name_jap = ran(a['name_of_buildings_duct'])
    name_hir = a['name_of_buildings_duct_hir'][name_jap]
    name_rus = a['name_of_buildings_duct'][name_jap]
    jap = ['これ', 'は', name_jap, 'という', '意味です']
    hir = ''.join(['これ', 'は', name_hir, 'という', 'いみです'])
    rus = ' '.join(['Это означает', name_rus])
    jap = ''.join(jap)
    return jap, hir, rus, this_means_that.__name__

def similary_toorini():
    print('similary_youna_tochno')
    g = Glagols('glag_now', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][2]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    podl2, podl2_hir, podl2_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'は', podl2, 'のとおりに', jap_podl, padez, glag_jap, form1, 'ます']
    hir = ''.join([podl1_hir, 'は', podl2_hir, 'のとおりに', jap_podl_hir, padez,
        glag_hir, form1, 'ます'])
    rus = ' '.join([podl1_rus, glag_rus, padez_rus, jap_podl_rus, ', как',
        podl2_rus, '(делает точно также, как по инструкции)'])
    jap = ''.join(jap)
    return jap, hir, rus, similary_toorini.__name__

def do_you_know_that():
    print('do_you_know_that')
    g = Glagols('glag_past_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][3]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'が', jap_podl, padez, glag_jap, form1, 'のを', '知っていますか']
    hir = ''.join([podl1_hir, 'が', jap_podl_hir, padez, glag_hir, form1,
        'のを', 'しっていますか'])
    rus = ' '.join(['Вы знаете, что', podl1_rus, glag_rus, padez_rus,
        jap_podl_rus, '?'])
    jap = ''.join(jap)
    return jap, hir, rus, do_you_know_that.__name__

def during_that_event():
    print('during_that_event')
    build = ran(a['buildings'])
    build_hir = a['buildings_hir'][build]
    build_rus = a['end_build2'][build]
    reason = ran(a['reasons_naru'])
    reason_hir = a['reasons_naru_hir'][reason]
    reason_rus = a['reasons_naru'][reason]
    jap = [build, 'に行く', '途中で', reason]
    hir = ''.join([build_hir, 'にいく', 'とちゅうで', reason_hir])
    rus = ' '.join(['Во время поездки в', build_rus, reason_rus,
        '(в промежутке, в процессе)'])
    jap = ''.join(jap)
    return jap, hir, rus, during_that_event.__name__

def invented_by_someone():
    print('invented_by_someone')
    jap1 = ran(a['small object'])
    hir = a['small object_hir'][jap1]
    rus1 = a['small object'][jap1]
    podl1 = ran(a['names'])
    podl1_hir = a['names_hir'][podl1] + 'さん'
    podl1_rus = a['names'][podl1] + '-саном'
    podl1 = podl1 + 'さん'
    jap = [jap1, 'は', podl1, 'によって', '発明されました']
    hir = ''.join([podl1_hir, 'は', 'によって', 'はつめいされました'])
    rus = ' '.join([rus1, 'был/а изобретен', podl1_rus])
    jap = ''.join(jap)
    return jap, hir, rus, invented_by_someone.__name__

def going_to_build():
    print('going_to_build')
    build = ran(a['buildings'])
    build_hir = a['buildings_hir'][build]
    build_rus = a['end_build2'][build]
    jap = [build, 'へ行って来ます']
    hir = ''.join([build_hir, 'へいってきます'])
    rus = ' '.join(['Я сходил в', build_rus,
        '(пошел и вернулся, не сообщая о причине похода)'])
    jap = ''.join(jap)
    return jap, hir, rus, going_to_build.__name__

def doing_too_much():
    print('doing_too_much')
    g = Glagols('glag_past_post', 'choose', ['accusative'])
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][2]
    t = Times('choose', ['da_p'])
    time_jap, time_hir, time_rus = t.main()
    jap = [time_jap, jap_podl, padez, glag_jap, form1, 'すぎました']
    hir = ''.join([time_hir, jap_podl_hir, padez, glag_hir, form1, 'すぎました'])
    rus = ' '.join([time_rus, glag_rus, 'слишком много', padez_rus,
        jap_podl_rus, '(чересчур, в плохом смысле)'])
    jap = ''.join(jap)
    return jap, hir, rus, doing_too_much.__name__

def just_recently_did_something():
    print('just_recently_did_something')
    g = Glagols('glag_past_one_moment2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][7]
    jap = [jap_podl, padez, glag_jap, form1, 'ばかりです']
    hir = ''.join([jap_podl_hir, padez, glag_hir, form1, 'ばかりです'])
    rus = ' '.join(['Только недавно', glag_rus, padez_rus, jap_podl_rus,
        '(по ощущениям, субъективно прошло немного времени)'])
    jap = ''.join(jap)
    return jap, hir, rus, just_recently_did_something.__name__

def made_conclusion():
    print('made_conclusion')
    g = Glagols('glag_past_post', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][3]
    podl1, podl1_hir, podl1_rus = who_f('family', 'know_people', 'suff')
    jap = [podl1, 'が', jap_podl, padez, glag_jap, form1, 'のを', '知っていますか']
    hir = ''.join([podl1_hir, 'が', jap_podl_hir, padez, glag_hir, form1,
        'のを', 'しっていますか'])
    rus = ' '.join([podl1_rus, ', должно быть,', glag_rus, padez_rus,
        jap_podl_rus, '( делаю заключение на основе моей иноформации)'])
    jap = ''.join(jap)
    return jap, hir, rus, made_conclusion.__name__

def i_dont_know_how_to_do():
    print('i_dont_know_how_to_do')
    g = Glagols('glag_verb_stem_2', 'all')
    (glag_jap, glag_hir, glag_rus, jap_podl, jap_podl_hir, jap_podl_rus,
        padez, padez_rus, rand_glag) = g.main()
    if glag_jap == '聞_2' or glag_jap == '聞_1':
        glag_jap = '聞'
    form1 = a['glag_form'][glag_jap][3]
    rand = random.randint(0, 1)
    if rand == 0:
        able = 'ことができる'
        rus_able = 'смогу ли я'
        dict = {'心配です': ['しんぱいです', 'волнуюсь'], 'わかりません': ['わかりません',
            'не знаю'], '迷っています': ['まよって', 'сомневаюсь'], '興味があります': [
            'きょうみがあります', 'интересно,']}
        jap_dict = ran(dict)
        hir_dict = dict[jap_dict][0]
        rus_dict = dict[jap_dict][1]
    else:
        able = ''
        rus_able = 'стоит ли'
        dict = {'決めましている': ['きめている', 'решаю'], '調べている': ['しらべている', 'изучаю'
            ], '迷っています': ['まよっています', 'сомневаюсь'], '考えています': ['かんがえています',
            'думаю']}
        jap_dict = ran(dict)
        hir_dict = dict[jap_dict][0]
        rus_dict = dict[jap_dict][1]
    jap = [jap_podl, padez, glag_jap, form1, able, 'かどうか、', jap_dict]
    hir = ''.join([jap_podl_hir, padez, glag_hir, form1, able, 'かどうか、',
        hir_dict])
    rus = ' '.join([rus_dict, rus_able, glag_rus, padez_rus, jap_podl_rus])
    jap = ''.join(jap)
    return jap, hir, rus, i_dont_know_how_to_do.__name__


print(incentive_voice())
