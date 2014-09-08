from util import *


skill_level_process_format = {
    '1': ((0, 'bb atk%', int, not_zero),
          (1, 'bb flat atk', int, not_zero),
          (2, 'bb crit%', int, not_zero),
          (3, 'bb bc%', int, not_zero),
          (4, 'bb hc%', int, not_zero),
          (5, 'bb dmg%', int, not_zero)),

    '2': ((0, 'heal low', int),
          (1, 'heal high', int),
          ([2, 3], 'rec added% (heal)',
           lambda x, y: 100 + ((1 + float(x) / 100) *
                               (1 + float(y) / 100) * 10))),

    '3': ((0, 'gradual heal low', int),
          (1, 'gradual heal high', int),
          (2, 'rec added% (regen)', lambda x: (1 + float(x) / 100) * 10),
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

    '29': (([0, 1, 2], 'bb elements',
            lambda x, y, z: map(elements.get, filter(not_zero, [x, y, z]))),
           (3, 'bb atk%', int, not_zero),
           (4, 'bb flat atk', int, not_zero),
           (5, 'bb crit%', int, not_zero),
           (6, 'bb bc%', int, not_zero),
           (7, 'bb hc%', int, not_zero),
           (8, 'bb dmg%', int, not_zero)),

    '30': (([0, 1, 2], 'elements added',
            lambda x, y, z: map(elements.get, filter(not_zero, [x, y, z]))),
           (6, 'elements added turns', int)),

    '31': ((0, 'increase bb gauge', bb_gauge),)
}


def parse_skill_level_process(process_type, process_info):
    if process_type in skill_level_process_format:
        return handle_format(skill_level_process_format[process_type],
                             process_info.split(','))
    return {}


def parse_skill_level_processes(process_types, process_infos):
    level_data = {}
    for process_type, process_info in zip(process_types, process_infos):
        process_data = parse_skill_level_process(process_type,
                                                 process_info)
        if 'elements added' in process_data and 'elements added' in level_data:
            level_data['elements added'] += process_data.pop('elements added')

        if 'bb elements' in process_data and 'bb elements' in level_data:
            level_data['bb elements'] += process_data.pop('bb elements')

        level_data.update(process_data)

    return level_data


def parse_skill_levels(unit_data, skill_data, skill, skill_levels):
    skill_level_format = (
        (1, 'bc cost', bb_gauge),

        lambda lvl: parse_skill_level_processes(
            skill[PROCESS_TYPE].split('@'), lvl[2].split('@')),

        ([], 'max bc generated',
         lambda data: data['hits'] * int(skill[DROP_CHECK_CNT]),
         lambda data: 'hits' in data),

        ([], 'lord damage range',
         lambda data: dmg_str(damage_range_bb(unit_data, skill_data, data)),
         lambda data: 'bb atk%' in data)
    )

    return [handle_format(skill_level_format, level_info.split(':'))
            for level_info in skill_levels[SKILL_LEVELS_PROCESSES].split('|')]


def parse_skill(unit_data, skill, skill_levels, dictionary):
    atk_process_types = {'1', '14', '29'}

    def get_skill_atk_frame(process_types, action_frames):
        for process_type, action_frame in zip(process_types.split('@'),
                                              action_frames.split('@')):
            if process_type in atk_process_types:
                return action_frame

    skill_format = ((BB_NAME, 'name', get_dict_str(dictionary)),
                    (DESC, 'desc', get_dict_str(dictionary)),

                    ([PROCESS_TYPE, DMG_FRAME], 'hits',
                     lambda p, a: hits(get_skill_atk_frame(p, a)),
                     lambda p: not set(p.split('@')).isdisjoint(
                         atk_process_types)),

                    ([PROCESS_TYPE, DMG_FRAME], 'hit dmg% distribution',
                     lambda p, a: hit_dmg_dist(get_skill_atk_frame(p, a)),
                     lambda p, a, data: 'hits' in data),

                    (DROP_CHECK_CNT, 'max bc generated',
                     lambda x, data: data['hits'] * int(x),
                     lambda x, data: 'hits' in data),

                    ([], 'levels', lambda data: parse_skill_levels(
                        unit_data, data, skill, skill_levels)))

    return handle_format(skill_format, skill)
