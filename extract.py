#!/usr/bin/python

import json
import glob

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def damage_range(atk):
    return (int((atk * 0.9) + (atk / 32)),
            int(atk + (atk / 25)))

def parse_bb_attack(process_info):
    buffs = dict()

    if int(process_info[0]) != 0:
        buffs['bb atk%'] = int(process_info[0])
    if int(process_info[1]) != 0:
        buffs['bb flat atk'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['bb crit%'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['bb bc%'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['bb hc%'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['bb dmg%'] = int(process_info[5])

    return buffs

def parse_bb_heal(process_info):
    return {'heal low': int(process_info[0]),
            'heal high': int(process_info[1])}

def parse_bb_gradual_heal(process_info):
    return {'gradual heal low': int(process_info[0]),
            'gradual heal high': int(process_info[1]),
            'gradual heal turns': int(process_info[3])}

def parse_bb_bb_fill_gauge_to_max(process_info):
    return {'self fill bb gauge': True}

elements = {
    '0': 'all',
    '1': 'fire',
    '2': 'water',
    '3': 'earth',
    '4': 'thunder',
    '5': 'light',
    '6': 'dark'
}

def parse_bb_buff_stats(process_info):
    buffs = {'element buffed': elements[process_info[0]],
             'buff turns': int(process_info[5])}

    if int(process_info[1]) != 0:
        buffs['atk% buff'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['def% buff'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['rec% buff'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['crit% buff'] = int(process_info[4])

    return buffs

def parse_bb_buff_drop_rate(process_info):
    buffs = dict()

    if int(process_info[0]) != 0:
        buffs['bc drop rate% buff'] = int(process_info[0])
    if int(process_info[1]) != 0:
        buffs['hc drop rate% buff'] = int(process_info[1])

    return buffs

def parse_bb_remove_status_ailments(process_info):
    return {'remove all status ailments': True}

ailments = {
    '1': 'poison%',
    '2': 'weaken%',
    '3': 'sick%',
    '4': 'injury%',
    '5': 'curse%',
    '6': 'paralysis%'
}
def parse_bb_apply_status_ailments(process_info):
    ails = {}
    for ail, percent in chunks(process_info[:-1], 2):
        if ail != '0':
            ails[ailments[ail]] = int(percent)
    return ails

def parse_bb_random_attack(process_info):
    buffs = {'random attack': True}

    if int(process_info[0]) != 0:
        buffs['bb atk%'] = int(process_info[0])
    if int(process_info[1]) != 0:
        buffs['bb flat atk'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['bb crit%'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['bb bc%'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['bb hc%'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['hits'] = int(process_info[5])

    return buffs

def parse_bb_attack_hp_drain(process_info):
    buffs = dict()

    if int(process_info[0]) != 0:
        buffs['bb atk%'] = int(process_info[0])
    if int(process_info[1]) != 0:
        buffs['bb flat atk'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['bb crit%'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['bb bc%'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['bb hc%'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['bb dmg%'] = int(process_info[5])

    buffs['hp drain% low'] = int(process_info[6])
    buffs['hp drain% high'] = int(process_info[7])
    return buffs

def parse_bb_negate_status_ailments_for_turns(process_info):
    return {'negate status ails turns': int(process_info[6])}

def parse_bb_damage_reduction(process_info):
    return {'dmg% reduction': int(process_info[0]),
            'dmg% reduction turns': int(process_info[1])}

def parse_bb_increase_bb_for_turns(process_info):
    return {'increase bb gauge gradual': int(process_info[0])/100,
            'increase bb gauge gradual turns': int(process_info[1])}

def parse_bb_defense_ignore(process_info):
    return {'defense% ignore': int(process_info[0]),
            'defense% ignore turns': int(process_info[1])}

def parse_bb_boost_spark_damage(process_info):
    return {'spark dmg% buff': int(process_info[0]),
            'buff turns': int(process_info[6])}

def parse_bb_multiple_elem_attack(process_info):
    buffs = dict()
    elements_added = []

    if int(process_info[0]) != 0:
        elements_added.append(elements[process_info[0]])
    if int(process_info[1]) != 0:
        elements_added.append(elements[process_info[1]])
    if int(process_info[2]) != 0:
        elements_added.append(elements[process_info[2]])

    if len(elements_added) != 0:
        buffs['bb elements'] = elements_added
    if int(process_info[3]) != 0:
        buffs['bb atk%'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['bb flat atk'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['bb crit%'] = int(process_info[5])
    if int(process_info[6]) != 0:
        buffs['bb bc%'] = int(process_info[6])
    if int(process_info[7]) != 0:
        buffs['bb hc%'] = int(process_info[7])
    if int(process_info[8]) != 0:
        buffs['bb dmg%'] = int(process_info[8])

    return buffs

def parse_bb_element_change(process_info):
    elements_added = []

    if int(process_info[0]) != 0:
        elements_added.append(elements[process_info[0]])
    if int(process_info[1]) != 0:
        elements_added.append(elements[process_info[1]])
    if int(process_info[2]) != 0:
        raise 'Guessed path'
        elements_added.append(elements[process_info[2]])

    return {'elements added': elements_added,
            'elements added turns': int(process_info[6])}

def parse_bb_increase_bb_gauge(process_info):
    return {'increase bb gauge': int(process_info[0])/100}

def parse_bb_process(process_type, process_info):
    fns = {
        '1': parse_bb_attack,
        '2': parse_bb_heal,
        '3': parse_bb_gradual_heal,
        '4': parse_bb_bb_fill_gauge_to_max,
        '5': parse_bb_buff_stats,
        '6': parse_bb_buff_drop_rate,
        '10': parse_bb_remove_status_ailments,
        '11': parse_bb_apply_status_ailments,
        '13': parse_bb_random_attack,
        '14': parse_bb_attack_hp_drain,
        '17': parse_bb_negate_status_ailments_for_turns,
        '18': parse_bb_damage_reduction,
        '19': parse_bb_increase_bb_for_turns,
        #'20': parse_bb_chance_of_bb_filling_and_increases_fill_rate,
        '22': parse_bb_defense_ignore,
        '23': parse_bb_boost_spark_damage,
        '29': parse_bb_multiple_elem_attack,
        '30': parse_bb_element_change,
        '31': parse_bb_increase_bb_gauge
        }
    if process_type in fns:
        return fns[process_type](process_info.split(','))
    return {}

def parse_bb_level(process_types, process_infos):
    process_data = {}
    for process_type, process_info in zip(process_types, process_infos):
        bb_data = parse_bb_process(process_type, process_info)
        if 'elements added' in bb_data and 'elements added' in process_data:
            data['elements added'] += bb_data.pop('elements added')

        if 'bb elements' in bb_data and 'bb elements' in process_data:
            data['bb elements'] += bb_data.pop('bb elements')

        process_data.update(bb_data)

    return process_data

def parse_bb(unit_data, bb_id, skills, bbs, dictionary):
    data = dict()

    skill = skills[bb_id]
    bb = bbs[bb_id]

    data['name'] = dictionary[skill['0nxpBDz2']]
    data['desc'] = dictionary[skill['qp37xTDh']]
    for process_type, atk_frames in zip(skill['hjAy9St3'].split('@'), skill['6Aou5M9r'].split('@')):
        if process_type in ['1', '14', '29']:
            data['hits'] = len(atk_frames.split(','))
            data['hit dmg% distribution'] = [int(hit.split(':')[1]) for hit in atk_frames.split(',')]
            data['max bc generated'] = data['hits'] * int(skill['n9h7p02P'])

    data['levels'] = []

    levels_info = bb['Kn51uR4Y'].split('|')

    for level_info in levels_info:
        level, bc_cost, misc = level_info.split(':')
        level_data = {'bc cost': int(bc_cost)/100}
        level_data.update(parse_bb_level(skill['hjAy9St3'].split('@'), misc.split('@')))
        if 'hits' in level_data:
            level_data['max bc generated'] = level_data['hits'] * int(skill['n9h7p02P'])

        if 'bb atk%' in level_data:
            total_atk = unit_data['lord atk']
            modifier = level_data['bb atk%']
            modifier += level_data.get('atk% buff', 0)

            total_atk = total_atk * (1 + float(modifier) / 100)
            total_atk += level_data.get('bb flat atk', 0)
            total_atk = total_atk * (1 + float(level_data.get('bb dmg%', 0)) / 100)
            total_atk = total_atk * float(sum(data.get('hit dmg% distribution', [100]))) / 100
            total_atk = int(total_atk)
            level_data['lord damage range'] = '~'.join(map(str, damage_range(total_atk)))

        assert int(level) == len(data['levels']) + 1
        data['levels'].append(level_data)

    return data

def parse_ls_stat_boost_all_types(process_info):
    buffs = dict()

    if int(process_info[0]) != 0:
        buffs['atk% buff'] = int(process_info[0])
    if int(process_info[1]) != 0:
        buffs['def% buff'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['rec% buff'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['crit% buff'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['hp% buff'] = int(process_info[4])

    return buffs

def parse_ls_stat_boost_types(process_info):
    buffs = dict()

    if process_info[0] != '0':
        buffs['elements buffed'] = buffs.get('elements buffed', []) + [elements[process_info[0]]]
    if process_info[1] != '0':
        buffs['elements buffed'] = buffs.get('elements buffed', []) + [elements[process_info[1]]]

    if int(process_info[2]) != 0:
        buffs['atk% buff'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['def% buff'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['rec% buff'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['crit% buff'] = int(process_info[5])
    if int(process_info[6]) != 0:
        buffs['hp% buff'] = int(process_info[6])

    return buffs

def parse_ls_resist_ails(process_info):
    buffs = dict()

    if int(process_info[0]) != 0:
        buffs['poison resist%'] = int(process_info[0])
    if int(process_info[1]) != 0:
        buffs['weaken resist%'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['sick resist%'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['injury resist%'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['curse resist%'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['paralysis resist%'] = int(process_info[5])

    return buffs

def parse_ls_resist_element(process_info):
    return {'%s resist%%' % elements[process_info[0]]: int(process_info[1])}

def parse_ls_increase_bb_for_turns(process_info):
    return {'bc fill per turn': int(process_info[0])/100}

def parse_ls_hc_effectiveness(process_info):
    return {'hc effectiveness%': int(process_info[0])}

def parse_ls_chance_damage_reduction(process_info):
    return {'dmg reduction%': int(process_info[0]),
            'dmg reduction chance%': int(process_info[1])}

def parse_ls_boost_hc_production(process_info):
    return {'hc production%': int(process_info[1])}

def parse_ls_inflict_status_ail(process_info):
    ails = {}
    for ail, percent in chunks(process_info, 2):
        if ail != '0':
            ails[ailments[ail]] = int(percent)
    return ails

def parse_ls_boost_for_first_turns(process_info):
    return {'first x turns atk%': int(process_info[0]),
            'first x turns def%': int(process_info[1]),
            'first x turns': int(process_info[2])}

def parse_ls_bb_gauge_fill_when_attacked(process_info):
    return {'bc fill when attacked low': int(process_info[0])/100,
            'bc fill when attacked high': int(process_info[1])/100,
            'bc fill when attacked%': int(process_info[2])}

def parse_ls_chance_ignore_def(process_info):
    return {'ignore def%': int(process_info[0])}

def parse_ls_boost_with_spark(process_info):
    buffs = dict()

    if int(process_info[0]) != 0:
        buffs['damage% for spark'] = int(process_info[0])
    if int(process_info[1]) != 0:
        buffs['bc drop% for spark'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['hc drop% for spark'] = int(process_info[2])
    if int(process_info[3]) != 0:
        raise 'Guessed path hit'
        buffs['item drop% for spark'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['zel drop% for spark'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['karma drop% for spark'] = int(process_info[5])

    return buffs

def parse_ls_bb_gauge_fill_rate(process_info):
    return {'bb gauge fill rate%': int(process_info[0])}

def parse_ls_boost_crit_damage(process_info):
    return {'dmg% for crits': float(process_info[0])*100}

def parse_ls_chance_bb_fill_when_attacking(process_info):
    return {'bc fill when attacking low': int(process_info[0])/100,
            'bc fill when attacking high': int(process_info[1])/100,
            'bc fill when attacking%': int(process_info[2])}

def parse_ls_rainbow_boost(process_info):
    buffs = {'unique elements required': int(process_info[0])}

    if int(process_info[1]) != 0:
        buffs['atk% buff'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['def% buff'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['rec% buff'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['crit% buff'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['hp% buff'] = int(process_info[5])

    return buffs

genders = {'0': 'genderless', '1': 'male', '2': 'female'}
def parse_ls_gender_boost(process_info):
    buffs = {'gender required': genders[process_info[0][0]]}

    if int(process_info[1]) != 0:
        buffs['atk% buff'] = int(process_info[1])
    if int(process_info[2]) != 0:
        buffs['def% buff'] = int(process_info[2])
    if int(process_info[3]) != 0:
        buffs['rec% buff'] = int(process_info[3])
    if int(process_info[4]) != 0:
        buffs['crit% buff'] = int(process_info[4])
    if int(process_info[5]) != 0:
        buffs['hp% buff'] = int(process_info[5])

    return buffs

def parse_ls_chance_1_damage(process_info):
    return {'take 1 dmg%': int(process_info[0])}

def parse_ls_boost_elemental_weakness_damage(process_info):
    buffs = {'dmg% for elemental weakness': float(process_info[6])*100}

    for element in process_info[:-1]:
        if element != '0':
            buffs['%s units do extra elemental weakness dmg' % elements[element]] = True
 
    return buffs
    
def parse_ls_dmg_boost_by_hpcondition(process_info):
    return {'atk% buff': int(process_info[0]),
            'hp% trigger': int(process_info[4]),
            'trigger condition': 'greater than' if (process_info[5] == '1') else 'less than'}

def parse_ls_process(process_type, process_info):
    fns = {
        '1': parse_ls_stat_boost_all_types,
        '2': parse_ls_stat_boost_types,
        '4': parse_ls_resist_ails,
        '5': parse_ls_resist_element,
        '9': parse_ls_increase_bb_for_turns,
        '11': parse_ls_dmg_boost_by_hpcondition,
        '10': parse_ls_hc_effectiveness,
        '14': parse_ls_chance_damage_reduction,
        '19': parse_ls_boost_hc_production,
        '20': parse_ls_inflict_status_ail,
        '21': parse_ls_boost_for_first_turns,
        '25': parse_ls_bb_gauge_fill_when_attacked,
        '29': parse_ls_chance_ignore_def,
        '31': parse_ls_boost_with_spark,
        '32': parse_ls_bb_gauge_fill_rate,
        '34': parse_ls_boost_crit_damage,
        '35': parse_ls_chance_bb_fill_when_attacking,
        '41': parse_ls_rainbow_boost,
        '42': parse_ls_gender_boost,
        '43': parse_ls_chance_1_damage,
        '50': parse_ls_boost_elemental_weakness_damage
        }
    if process_type in fns:
        return fns[process_type](process_info.split(','))
    return {}

def parse_leader_skill(unit_data, leader_skill, dictionary):
    data = dict()

    data['name'] = dictionary[leader_skill['dJPf9a5v']]
    data['desc'] = dictionary[leader_skill['qp37xTDh']]

    for process_type, process_info in zip(leader_skill['hjAy9St3'].split('@'), leader_skill['2Smu5Mtq'].split('@')):
        process_data = parse_ls_process(process_type, process_info)
        if 'elements buffed' in process_data and 'elements buffed' in data:
            data['elements buffed'] += process_data.pop('elements buffed')

        data.update(process_data)

    return data

def parse_unit(unit, skills, bbs, leader_skills, dictionary):
    data = dict()

    data['name'] = dictionary[unit['utP1c0CD']]
    data['element'] = elements[unit['iNy0ZU5M']]
    data['rarity'] = int(unit['7ofj5xa1'])
    data['base hp'] = int(unit['UZ1Bj7w2'])
    data['lord hp'] = int(unit['3WMz78t6'])
    data['base atk'] = int(unit['i9Tn7kYr'])
    data['lord atk'] = int(unit['omuyP54D'])
    data['base def'] = int(unit['q78KoWsg'])
    data['lord def'] = int(unit['32INDST4'])
    data['base rec'] = int(unit['92ij6UGB'])
    data['lord rec'] = int(unit['X9P3AN5d'])
    data['hits'] = len(unit['6Aou5M9r'].split(','))
    data['hit dmg% distribution'] = [int(hit.split(':')[1]) for hit in unit['6Aou5M9r'].split(',')]
    data['max bc generated'] = data['hits'] * int(skill['n9h7p02P'])
    data['lord damage range'] = '~'.join(map(str, damage_range(data['lord atk'])))

    if unit['nj9Lw7mV'] != '0':
        data['bb'] = parse_bb(data, unit['nj9Lw7mV'], skills, bbs, dictionary)

    if unit['iEFZ6H19'] != '0':
        data['sbb'] = parse_bb(data, unit['iEFZ6H19'], skills, bbs, dictionary)

    if unit['oS3kTZ2W'] != '0':
        data['leader skill'] = parse_leader_skill(data, leader_skills[unit['oS3kTZ2W']], dictionary)

    return data

if __name__ == '__main__':
    with open(glob.glob('Ver*_2r9cNSdt.json')[-1]) as f:
        with open(glob.glob('sgtext_dictionary_*.csv')[-1]) as f2:
            with open(glob.glob('Ver*_zLIvD5o2.json')[-1]) as f3:
                with open(glob.glob('Ver*_wkCyV73D.json')[-1]) as f4:
                    with open(glob.glob('Ver*_4dE8UKcw.json')[-1]) as f5:
                        units = json.load(f)
                        skills_js = json.load(f4)
                        bbs_js = json.load(f3)
                        leader_skills_js = json.load(f5)
                        dictionary = dict([line.split('^')[:2] for line in f2.readlines()])

                        skills = dict()
                        for skill in skills_js:
                            if skill['h6UL9A1B'] not in ['1', '2', '3']:
                                print dictionary[skill['0nxpBDz2']], dictionary[skill['qp37xTDh']], 'type:', skill['h6UL9A1B']

                            skills[skill['nj9Lw7mV']] = skill

                        bbs = dict()
                        for bb in bbs_js:
                            bbs[bb['nj9Lw7mV']] = bb

                        leader_skills = dict()
                        for leader_skill in leader_skills_js:
                            leader_skills[leader_skill['oS3kTZ2W']] = leader_skill

                        units_data = {}
                        for unit in units:
                            unit_data = parse_unit(unit, skills, bbs, leader_skills, dictionary)
                            units_data[unit_data['name']] = unit_data
                            unit_data.pop('name')

                        print json.dumps(units_data)
