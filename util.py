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


def damage_range(atk):
    return (int((atk * 0.9) + (atk / 32)),
            int(atk + (atk / 25)))


def not_zero(a):
    return int(a) != 0


def bb_gauge(a):
    return int(a)/100


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

        if predicate(process_info[idx2]) is True:
            data[key] = value

    return data
