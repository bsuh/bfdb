#!/usr/bin/python

import json
import glob
from util import *
from leaderskill import parse_leader_skill
from braveburst import parse_bb

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
