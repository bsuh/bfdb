#!/usr/bin/python

import collections
import glob
import json
import sys
from util import *
from leaderskill import parse_leader_skill
from braveburst import parse_skill


def parse_unit(unit, skills, bbs, leader_skills, ais, dictionary):
    def max_bc_gen(s, data):
        return int(s) * data['hits']

    def _damage_range(s):
        return '~'.join(map(str, damage_range(int(s))))

    def _parse_skill(bb_id, data):
        return parse_skill(data, skills[bb_id], bbs[bb_id], dictionary)

    def parse_ls(ls_id, data):
        return parse_leader_skill(data, leader_skills[ls_id], dictionary)

    unit_format = ((UNIT_NAME, 'name', get_dict_str(dictionary)),
                   (UNIT_ELEMENT, 'element', elements.get),
                   (UNIT_RARITY, 'rarity', int),
                   (UNIT_BASE_HP, 'base hp', int),
                   (UNIT_LORD_HP, 'lord hp', int),
                   (UNIT_BASE_ATK, 'base atk', int),
                   (UNIT_LORD_ATK, 'lord atk', int),
                   (UNIT_BASE_DEF, 'base def', int),
                   (UNIT_LORD_DEF, 'lord def', int),
                   (UNIT_BASE_REC, 'base rec', int),
                   (UNIT_LORD_REC, 'lord rec', int),
                   (DMG_FRAME, 'hits', hits),
                   (DMG_FRAME, 'hit dmg% distribution', hit_dmg_dist),
                   (DROP_CHECK_CNT, 'max bc generated', max_bc_gen),
                   (UNIT_LORD_ATK, 'lord damage range', _damage_range),
                   (UNIT_AI_ID, 'ai', ais.get),
                   (UNIT_IMP, 'imp', lambda s: parse_imps(s.split(':'))),
                   (BB_ID, 'bb', _parse_skill, not_zero),
                   (SBB_ID, 'sbb', _parse_skill, not_zero),
                   (LS_ID, 'leader skill', parse_ls, not_zero))

    return handle_format(unit_format, unit)


def parse_ai(ai):
    ai_format = ((AI_ID, 'id', str),
                 (AI_CHANCE, 'chance%', float),
                 (AI_TARGET, 'target', str),
                 (AI_ACTION_PARAMS, 'action', lambda s: s.split('@')[0]))

    return handle_format(ai_format, ai)

if __name__ == '__main__':
    _dir = 'data/decoded_dat/'
    if len(sys.argv) > 1:
        _dir = sys.argv[1]

    files = {
        'dict': 'data/dictionary_raw.txt',
        'unit':         _dir + 'Ver*_2r9cNSdt*',
        'skill level':  _dir + 'Ver*_zLIvD5o2*',
        'skill':        _dir + 'Ver*_wkCyV73D*',
        'leader skill': _dir + 'Ver*_4dE8UKcw*',
        'ai':           _dir + 'Ver*_XkBhe70R*',
    }

    jsons = {}
    for name, filename in files.iteritems():
        with open(glob.glob(filename)[-1]) as f:
            if f.name.split('.')[-1] == 'txt':
                jsons[name] = dict([
                    line.split('^')[:2] for line in f.readlines()
                ])
            else:
                jsons[name] = json.load(f)

    def key_by_id(lst, id_str):
        return {obj[id_str]: obj for obj in lst}

    skills = key_by_id(jsons['skill'], BB_ID)
    skill_levels = key_by_id(jsons['skill level'], BB_ID)
    leader_skills = key_by_id(jsons['leader skill'], LS_ID)

    ais = collections.defaultdict(list)
    for ai in jsons['ai']:
        ai_data = parse_ai(ai)
        ais[ai_data['id']].append(ai_data)
        ai_data.pop('id')

    units_data = {}
    for unit in jsons['unit']:
        unit_data = parse_unit(unit, skills, skill_levels, leader_skills,
                               ais, jsons['dict'])
        units_data[unit_data['name']] = unit_data
        unit_data.pop('name')

    print json.dumps(units_data)
