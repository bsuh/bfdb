from util import *


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


def parse_bb_heal(process_info):
    rec_added_1 = 1 + float(process_info[2]) / 100
    rec_added_2 = rec_added_1 * float(process_info[3]) / 100
    rec_added = 100 + (rec_added_1 + rec_added_2) * 10
    return {'rec added% (heal)': rec_added}


def parse_bb_regen(process_info):
    rec_added = (1 + 1 * float(process_info[2]) / 100) / 10
    return {'rec added% (regen)': rec_added * 100}


bb_process_format = {
    '1': ((0, 'bb atk%', int, not_zero),
          (1, 'bb flat atk', int, not_zero),
          (2, 'bb crit%', int, not_zero),
          (3, 'bb bc%', int, not_zero),
          (4, 'bb hc%', int, not_zero),
          (5, 'bb dmg%', int, not_zero)),

    '2': ((0, 'heal low', int),
          (1, 'heal high', int),
          parse_bb_heal),

    '3': ((0, 'gradual heal low', int),
          (1, 'gradual heal high', int),
          parse_bb_regen,
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

    '11': (([0, 1], ailments.get, second_int, not_zero),
           ([2, 3], ailments.get, second_int, not_zero),
           ([4, 5], ailments.get, second_int, not_zero),
           ([6, 7], ailments.get, second_int, not_zero)),

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

    '20': ((0, 'bc fill when attacked high', bb_gauge),
           (1, 'bc fill when attacked low', bb_gauge),
           (2, 'bc fill when attacked%', int),
           (3, 'bc fill when attacked turns', int)),

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


def parse_bb_process(process_type, process_info):
    if process_type in bb_process_format:
        return handle_format(bb_process_format[process_type],
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

    data['name'] = dictionary.get(skill[BB_NAME], skill[BB_NAME])
    data['desc'] = dictionary.get(skill[DESC], skill[DESC])
    for process_type, atk_frames in zip(skill[PROCESS_TYPE].split('@'),
                                        skill[DMG_FRAME].split('@')):
        if process_type in ['1', '14', '29']:
            data['hits'] = len(atk_frames.split(','))
            data['hit dmg% distribution'] = [
                int(hit.split(':')[1]) for hit in atk_frames.split(',')
            ]
            data['max bc generated'] = data['hits'] * int(
                skill[DROP_CHECK_CNT])

    data['levels'] = []

    levels_info = bb[BB_LEVELS].split('|')

    for level_info in levels_info:
        level, bc_cost, misc = level_info.split(':')
        level_data = {'bc cost': int(bc_cost)/100}
        level_data.update(parse_bb_level(skill[PROCESS_TYPE].split('@'),
                                         misc.split('@')))
        if 'hits' in level_data:
            level_data['max bc generated'] = level_data['hits'] * int(
                skill[DROP_CHECK_CNT])

        if 'bb atk%' in level_data:
            total_atk = unit_data['lord atk']
            modifier = level_data['bb atk%']
            modifier += level_data.get('atk% buff', 0)

            total_atk = total_atk * (1 + float(modifier) / 100)
            total_atk += level_data.get('bb flat atk', 0)
            total_atk = total_atk * (1 + float(level_data.get('bb dmg%', 0))
                                     / 100)
            total_atk = total_atk * float(sum(
                data.get('hit dmg% distribution', [100]))) / 100
            total_atk = int(total_atk)
            level_data['lord damage range'] = '~'.join(
                map(str, damage_range(total_atk)))

        assert int(level) == len(data['levels']) + 1
        data['levels'].append(level_data)

    return data
