#!/usr/bin/python

import json
import glob
import sys
from util import *
from leaderskill import parse_ls_process
from items import *


def parse_item_effect(item, data):
    effects = dict()
    for process_type, process_info in zip(item[PROCESS_TYPE].split('@'),
                                          item[ITEM_PROCESS].split('@')):
        effects.update(parse_item_process(process_type, process_info))
    if item[ITEM_TARGET_TYPE] == '2':
        effects['target_type'] = 'enemy'
    else:
        effects['target_type'] = 'self'
    if item[ITEM_TARGET_TYPE] == '1':
        effects['target_area'] = 'single'
    else:
        effects['target_area'] = 'aoe'
    return effects


def parse_sphere_effect(item, data, dictionary):
    effects = dict()
    for process_type, process_info in zip(item[PROCESS_TYPE].split('@'),
                                          item[ITEM_PROCESS].split('@')):
        effects.update(parse_ls_process(process_type, process_info))
    return effects


def parse_item(item, dictionary):
    def get_dict_str(s):
        return dictionary.get(s, s)

    def parse_type(item_data):
        data = dict()
        item_type = item_data[ITEM_TYPE]
        if item_type == '0':
            data['type'] = 'other'
        elif item_type == '1':
            data['type'] = 'consumable'
            data['max equipped'] = int(item[ITEM_MAX_EQUIPPED])
            data['effect'] = parse_item_effect(item_data, data)
        elif item_type == '2':
            data['type'] = 'material'
        elif item_type == '3':
            data['type'] = 'sphere'
            data['effect'] = parse_sphere_effect(item_data, data, dictionary)
        return data

    item_format = ((ITEM_NAME, 'name', get_dict_str),
                   (DESC, 'desc', get_dict_str),
                   (ITEM_RARITY, 'rarity', int),
                   (ITEM_SELL_PRICE, 'sell_price', int),
                   (ITEM_MAX_STACK, 'max_stack', int),
                   (ITEM_ID, 'id', int),
                   (ITEM_TYPE, 'type', item_types.get),
                   (parse_type))

    return handle_format(item_format, item)

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
        'items':        _dir + 'Ver*_83JWTCGy*',
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
    bbs = key_by_id(jsons['skill level'], BB_ID)
    leader_skills = key_by_id(jsons['leader skill'], LS_ID)

    items_data = {}
    for item in jsons['items']:
        item_data = parse_item(item, jsons['dict'])
        items_data[item_data['name']] = item_data
        item_data.pop('name')

    print json.dumps(items_data)
