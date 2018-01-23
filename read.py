from mysql import connector
import json


with open('config.json') as f:
    config = json.load(f)


conn = connector.connect(user=config['username'],
                         password=config['password'],
                         host='127.0.0.1',
                         database='arduino')

with open('/dev/ttyUSB0') as f:
    cursor = conn.cursor()
    light_insert = 'INSERT INTO light (measurement) VALUES (%f)'
    temp_insert = 'INSERT INTO temperature (measurement) VALUES (%d)'

    ct = 0
    acc = 0

    for line in f:
        segments = line.strip().lower().split(' ')

        if len(segments) != 2:
            continue

        if segments[0] == 't':
            cursor.execute(temp_insert, segments[1])

        else:
            assert(segments[0] == 'l')

            acc += int(segments[1])
            ct += 1

            if ct == 10:
                cursor.execute(light_insert, acc)
                acc = 0
                ct = 0
