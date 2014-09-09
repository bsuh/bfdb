UNIT_NAME = 'utP1c0CD'
UNIT_ELEMENT = 'iNy0ZU5M'
UNIT_RARITY = '7ofj5xa1'
UNIT_BASE_HP = 'UZ1Bj7w2'
UNIT_LORD_HP = '3WMz78t6'
UNIT_BASE_ATK = 'i9Tn7kYr'
UNIT_LORD_ATK = 'omuyP54D'
UNIT_BASE_DEF = 'q78KoWsg'
UNIT_LORD_DEF = '32INDST4'
UNIT_BASE_REC = '92ij6UGB'
UNIT_LORD_REC = 'X9P3AN5d'
UNIT_IMP = 'imQJdg64'
UNIT_AI_ID = 'i74vGUFa'
DMG_FRAME = '6Aou5M9r'
DROP_CHECK_CNT = 'n9h7p02P'
BB_ID = 'nj9Lw7mV'
SBB_ID = 'iEFZ6H19'
BB_NAME = '0nxpBDz2'
BB_LEVELS = 'Kn51uR4Y'
LS_ID = 'oS3kTZ2W'
LS_NAME = 'dJPf9a5v'
LS_PROCESS = '2Smu5Mtq'
PROCESS_TYPE = 'hjAy9St3'
DESC = 'qp37xTDh'
AI_ID = '4eEVw5hL'
AI_CHANCE = 'ug9xV4Fz'
AI_TARGET = 'VBj9u0ot'
AI_ACTION_PARAMS = 'Hhgi79M1'
AI_NAME = 'L8PCsu0K'

REQ_HEADER_TAG = 'F4q6i9xe'
REQ_ID = 'Hhgi79M1'
REQ_BODY_TAG = 'a3vSYuq2'
REQ_BODY = 'Kn51uR4Y'

ITEM_NAME = 'c7Z6xDB2'
ITEM_RARITY = '7ofj5xa1'
ITEM_SELL_PRICE = 'eKtE6k0n'
ITEM_MAX_STACK = 'm9gd5h1u'
ITEM_ID = 'kixHbe54'
ITEM_MAX_EQUIPPED = 't1i2vIbT'
ITEM_PROCESS = '2Smu5Mtq'
ITEM_TARGET_TYPE = 'moWQ30GH'
ITEM_TARGET_AREA = '6E2fGPWT'
ITEM_TYPE = 'h0K7wjeH'

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

item_types = {
    '0': 'other',
    '1': 'consumable',
    '2': 'material',
    '3': 'sphere'
}


def damage_range(atk):
    return (int((atk * 0.9) + (atk / 32)),
            int(atk + (atk / 25)))


def not_zero(a):
    return int(a) != 0


def bb_gauge(a):
    return int(a) / 100


def parse_imps(args):
    return {'max hp': args[0],
            'max atk': args[1],
            'max def': args[2],
            'max rec': args[3]}


def handle_format(fmt, obj):
    import inspect

    data = {}
    for entry in fmt:
        if hasattr(entry, '__call__'):
            data.update(entry(obj))
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

        if type(idx) == int and idx >= len(obj):
            continue
        if type(idx2) == int and idx2 >= len(obj):
            continue
        if type(idx) != int and idx not in obj:
            continue
        if type(idx2) != int and idx not in obj:
            continue
        if predicate(obj[idx2]) is not True:
            continue

        if hasattr(key, '__call__'):
            args = [obj[idx]]
            try:
                if len(inspect.getargspec(key).args) > 1:
                    args.append(data)
            except TypeError:
                pass
            key = key(*args)

        if hasattr(value, '__call__'):
            args = [obj[idx2]]
            try:
                if len(inspect.getargspec(value).args) > 1:
                    args.append(data)
            except TypeError:
                pass
            value = value(*args)

        data[key] = value

    return data
