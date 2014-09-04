#!/usr/bin/python

import json
import glob

def damage_range(atk):
    return (int((atk * 0.9) + (atk / 32)),
            int(atk + (atk / 25)))

def parse_bb_multiple_elem_attack(process_info):
    elements_added = []

    if int(process_info[0]) != 0:
        elements_added.append(elements[process_info[0]])
    if int(process_info[1]) != 0:
        elements_added.append(elements[process_info[1]])
    if int(process_info[2]) != 0:
        elements_added.append(elements[process_info[2]])

    if len(elements_added) != 0:
        return {'bb elements': elements_added}
    return {}

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

def not_zero(a):
    return int(a) != 0

def bb_gauge(a):
    return int(a)/100

elements = {
    '0': 'all',
    '1': 'fire',
    '2': 'water',
    '3': 'earth',
    '4': 'thunder',
    '5': 'light',
    '6': 'dark'
}

ailments = {
    '1': 'poison%',
    '2': 'weaken%',
    '3': 'sick%',
    '4': 'injury%',
    '5': 'curse%',
    '6': 'paralysis%'
}

bb_process_format = {
    '1': ((0, 'bb atk%', int, not_zero),
          (1, 'bb flat atk', int, not_zero),
          (2, 'bb crit%', int, not_zero),
          (3, 'bb bc%', int, not_zero),
          (4, 'bb hc%', int, not_zero),
          (5, 'bb dmg%', int, not_zero)),

    '2': ((0, 'heal low', int),
          (1, 'heal high', int)),

    '3': ((0, 'gradual heal low', int),
          (1, 'gradual heal high', int),
          (3, 'gradual heal turns', int)),

    '4': ((0, 'bb bc fill', int, not_zero),
          (1, 'bb bc fill%', int, not_zero)),

    '5': ((0, 'element buffed', elements.get),
          (1, 'atk% buff', int, not_zero),
          (2, 'def% buff', int, not_zero),
          (3, 'rec% buff', int, not_zero),
          (4, 'crit% buff', int, not_zero),
          (5, 'buff turns', int)),

    '6': ((0, 'bc drop rate% buff', int, not_zero),
          (1, 'hc drop rate% buff', int, not_zero)),

    '7': ((0, 'angel idol effect this turn', True),),

    '10': ((0, 'remove all status ailments', True),),

    '11': (((0, 1), ailments.get, int, not_zero),
           ((2, 3), ailments.get, int, not_zero),
           ((4, 5), ailments.get, int, not_zero),
           ((6, 7), ailments.get, int, not_zero)),

    '13': ((0, 'random attack', True),
           (0, 'bb atk%', int, not_zero),
           (1, 'bb flat atk', int, not_zero),
           (2, 'bb crit%', int, not_zero),
           (3, 'bb bc%', int, not_zero),
           (4, 'bb hc%', int, not_zero),
           (5, 'hits', int, not_zero)),

    '14': ((0, 'bb atk%', int, not_zero),
           (1, 'bb flat atk', int, not_zero),
           (2, 'bb crit%', int, not_zero),
           (3, 'bb bc%', int, not_zero),
           (4, 'bb hc%', int, not_zero),
           (5, 'bb dmg%', int, not_zero),
           (6, 'hp drain% low', int),
           (7, 'hp drain% high', int)),

    '17': ((6, 'negate status ails turns', int),),

    '18': ((0, 'dmg% reduction', int),
           (1, 'dmg% reduction turns', int)),

    '19': ((0, 'increase bb gauge gradual', bb_gauge),
           (1, 'increase bb gauge gradual turns', int)),

    '22': ((0, 'defense% ignore', int),
           (1, 'defense% ignore turns', int)),

    '23': ((0, 'spark dmg% buff', int),
           (6, 'buff turns', int)),

    '29': (parse_bb_multiple_elem_attack,
           (3, 'bb atk%', int, not_zero),
           (4, 'bb flat atk', int, not_zero),
           (5, 'bb crit%', int, not_zero),
           (6, 'bb bc%', int, not_zero),
           (7, 'bb hc%', int, not_zero),
           (8, 'bb dmg%', int, not_zero)),

    '30': (parse_bb_element_change,),

    '31': ((0, 'increase bb gauge', bb_gauge),)
}

def handle_process_format(process_format, process_info):
    data = {}
    for entry in process_format:
        if hasattr(entry, '__call__'):
            data.update(entry(process_info))
            continue

        idx = entry[0]
        if hasattr(idx, '__iter__'):
            idx, idx2 = idx
        else:
            idx2 = idx

        key = entry[1]
        value = entry[2]
        if len(entry) > 3:
            predicate = entry[3]
        else:
            predicate = lambda x: True

        if idx >= len(process_info) <= idx2:
            continue

        if hasattr(key, '__call__'):
            key = key(process_info[idx])

        if hasattr(value, '__call__'):
            value = value(process_info[idx2])

        if predicate(process_info[idx2]) == True:
            data[key] = value

    return data

def parse_bb_process(process_type, process_info):
    if process_type in bb_process_format:
        return handle_process_format(bb_process_format[process_type],
                                     process_info.split(','))
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

def parse_elements_buffed(process_info):
    buffs = dict()

    if process_info[0] != '0':
        buffs['elements buffed'] = buffs.get('elements buffed', []) + [elements[process_info[0]]]
    if process_info[1] != '0':
        buffs['elements buffed'] = buffs.get('elements buffed', []) + [elements[process_info[1]]]

    return buffs

def crit_elem_weakness(x):
    return float(x)*100

genders = {'0': 'genderless', '1': 'male', '2': 'female'}

ls_process_format = {
    '1': ((0, 'atk% buff', int, not_zero),
          (1, 'def% buff', int, not_zero),
          (2, 'rec% buff', int, not_zero),
          (3, 'crit% buff', int, not_zero),
          (4, 'hp% buff', int, not_zero)),

    '2': (parse_elements_buffed,
          (2, 'atk% buff', int, not_zero),
          (3, 'def% buff', int, not_zero),
          (4, 'rec% buff', int, not_zero),
          (5, 'crit% buff', int, not_zero),
          (6, 'hp% buff', int, not_zero)),

    '4': ((0, 'poison resist%', int, not_zero),
          (1, 'weaken resist%', int, not_zero),
          (2, 'sick resist%', int, not_zero),
          (3, 'injury resist%', int, not_zero),
          (4, 'curse resist%', int, not_zero),
          (5, 'paralysis resist%', int, not_zero)),

    '5': (([0, 1], lambda el: '%s resist%%' % elements[el], int),),

    '9': ((0, 'bc fill per turn', bb_gauge),),

    '10': ((0, 'hc effectiveness%', int),),

    '11': ((0, 'atk% buff', int, not_zero),
           (1, 'def% buff', int, not_zero),
           (2, 'rec% buff', int, not_zero),
           (3, 'crit% buff', int, not_zero),
           ([5, 4], lambda s: 'hp %s %% buff requirement' % ('above' if int(s) == 1 else 'below'), int, not_zero)),

    '14': ((0, 'dmg reduction%', int),
           (1, 'dmg reduction chance%', int)),

    '19': ((1, 'hc production%', int),),

    '20': (((0, 1), ailments.get, int, not_zero),
           ((2, 3), ailments.get, int, not_zero),
           ((4, 5), ailments.get, int, not_zero),
           ((6, 7), ailments.get, int, not_zero)),

    '21': ((0, 'first x turns atk%', int, not_zero),
           (1, 'first x turns def%', int, not_zero),
           (2, 'first x turns', int)),

    '25': ((0, 'bc fill when attacked low', bb_gauge),
           (1, 'bc fill when attacked high', bb_gauge),
           (2, 'bc fill when attacked%', int)),

    '29': ((0, 'ignore def%', int),),

    '31': ((0, 'damage% for spark', int, not_zero),
           (1, 'bc drop% for spark', int, not_zero),
           (2, 'hc drop% for spark', int, not_zero),
           (3, 'item drop% for spark GUESSED', int, not_zero),
           (4, 'zel drop% for spark', int, not_zero),
           (5, 'karma drop% for spark', int, not_zero)),

    '32': ((0, 'bb gauge fill rate%', int),),

    '34': ((0, 'dmg% for crits', crit_elem_weakness),),

    '35': ((0, 'bc fill when attacking low', bb_gauge),
           (1, 'bc fill when attacking high', bb_gauge),
           (2, 'bc fill when attacking%', int)),

    '41': ((0, 'unique elements required', int),
           (1, 'atk% buff', int, not_zero),
           (2, 'def% buff', int, not_zero),
           (3, 'rec% buff', int, not_zero),
           (4, 'crit% buff', int, not_zero),
           (5, 'hp% buff', int, not_zero)),

    '42': ((0, 'gender required', lambda s: genders[s[0]]),
           (1, 'atk% buff', int, not_zero),
           (2, 'def% buff', int, not_zero),
           (3, 'rec% buff', int, not_zero),
           (4, 'crit% buff', int, not_zero),
           (5, 'hp% buff', int, not_zero)),

    '43': ((0, 'take 1 dmg%', int),),

    '48': ((0, 'reduced bb bc cost%', int),),

    '50': ((0, lambda el: '%s units do extra elemental weakness dmg' % elements[el], True, not_zero),
           (1, lambda el: '%s units do extra elemental weakness dmg' % elements[el], True, not_zero),
           (2, lambda el: '%s units do extra elemental weakness dmg' % elements[el], True, not_zero),
           (3, lambda el: '%s units do extra elemental weakness dmg' % elements[el], True, not_zero),
           (4, lambda el: '%s units do extra elemental weakness dmg' % elements[el], True, not_zero),
           (5, lambda el: '%s units do extra elemental weakness dmg' % elements[el], True, not_zero),
           (6, 'dmg% for elemental weakness', crit_elem_weakness)),
}

def parse_ls_process(process_type, process_info):
    if process_type in ls_process_format:
        return handle_process_format(ls_process_format[process_type],
                                     process_info.split(','))
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
