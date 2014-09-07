from util import *
from braveburst import parse_bb_process


def parse_item_remove_status_ailments(process_info):
    effect = dict()
    for status in process_info:
        if int(status) != 0 and int(status) < 7:
            effect['remove ' + ailments[status].rstrip('%')] = True
    return effect

item_process_format = {
    '1': ((0, 'item atk%', int, not_zero),
          (1, 'item flat atk', int, not_zero),
          (2, 'item crit%', int, not_zero),
          (3, 'item bc%', int, not_zero),
          (4, 'item hc%', int, not_zero),
          (5, 'item dmg%', int, not_zero)),

    '10': (parse_item_remove_status_ailments,),
}

def parse_item_process(process_type, process_info):
    if process_type in item_process_format:
        return handle_process_format(item_process_format[process_type],
                                     process_info.split(','))
    return parse_bb_process(process_type, process_info)