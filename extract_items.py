#!/usr/bin/python

import json
import glob
import sys
from util import *
from leaderskill import parse_ls_process
from braveburst import parse_bb
from items import *


def parse_item_effect(item, data):
    effects = dict()
    for process_type, process_info in zip(item[PROCESS_TYPE].split('@'), item[ITEM_PROCESS].split('@')):
        effects.update(parse_item_process(process_type, process_info))
    effects['target_type'] = 'enemy' if item[ITEM_TARGET_TYPE] == '2' else 'self'
    effects['target_area'] = 'single' if item[ITEM_TARGET_AREA] == '1' else 'aoe'
    return effects


def parse_sphere_effect(item, data, dictionary):
    effects = dict()
    for process_type, process_info in zip(item[PROCESS_TYPE].split('@'), item[ITEM_PROCESS].split('@')):
        effects.update(parse_ls_process(process_type, process_info))
    return effects


def parse_item(item, dictionary):
    data = dict()
    data['name'] = dictionary.get(item[ITEM_NAME], item[ITEM_NAME])
    data['desc'] = dictionary.get(item[DESC], item[DESC])
    data['rarity'] = int(item[ITEM_RARITY])
    data['sell_price'] = int(item[ITEM_SELL_PRICE])
    data['max_stack'] = int(item[ITEM_MAX_STACK])
    data['id'] = int(item[ITEM_ID])
    if item[ITEM_TYPE] == '0':
        data['type'] = 'other'
    elif item[ITEM_TYPE] == '1':
        data['type'] = 'consumable'
        data['max equipped'] = int(item[item_params[ITEM_MAX_EQUIPPED]])
        data['effect'] = parse_item_effect(item, data)
    elif item[ITEM_TYPE] == '2':
        data['type'] = 'material'
    elif item[ITEM_TYPE] == '3':
        data['type'] = 'sphere'
        data['effect'] = parse_sphere_effect(item, data, dictionary)
    return data

if __name__ == '__main__':
    subdirectory = 'data/decoded_dat'
    if len(sys.argv) > 1:
        subdirectory = sys.argv[1]
    with open(glob.glob(subdirectory + 'Ver*_2r9cNSdt*')[-1]) as f:
        with open(glob.glob('data/dictionary_raw.txt')[-1]) as f2:
            with open(glob.glob(subdirectory + 'Ver*_zLIvD5o2*')[-1]) as f3:
                with open(glob.glob(subdirectory + 'Ver*_wkCyV73D*')[-1]) as f4:
                    with open(glob.glob(subdirectory + 'Ver*_4dE8UKcw*')[-1]) as f5:
                        with open(glob.glob(subdirectory + 'Ver*_83JWTCGy.dat.json')[-1]) as f6:
                            units = json.load(f)
                            skills_js = json.load(f4)
                            bbs_js = json.load(f3)
                            leader_skills_js = json.load(f5)
                            items = json.load(f6)
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

                            items_data = {}
                            for item in items:
                                item_data = parse_item(item, dictionary)
                                items_data[item_data['name']] = item_data
                                item_data.pop('name')

                            if 'jp' in sys.argv:
                                print json.dumps(items_data, sort_keys=True, indent=4, ensure_ascii=False).encode('utf8')
                            else:
                                print json.dumps(items_data, sort_keys=True, indent=4)
