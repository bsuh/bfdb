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

def parse_imps(args):
    return {'max hp': args[0],
            'max atk': args[1],
            'max def': args[2],
            'max rec': args[3]}

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
