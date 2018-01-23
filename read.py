from mysql import connector
import json


with open('config.json') as f:
    config = json.load(f)


with connector.connect(user=config['username'],
                       password=config['password'],
                       host='127.0.0.1',
                       database='arduino') as conn, open('/dev/ttyUSB0') as f:
    cursor = conn.cursor()
    light_insert = 'INSERT INTO light (measurement) VALUES (?)'
    temp_insert = 'INSERT INTO temperature (measurement) VALUES (?)'

    ct = 0
    acc = 0

    for line in f:
        segments = line.strip().lower().split(' ')

        if len(line) != 2:
            continue

        if line[0] == 't':
            cursor.execute(temp_insert, line[1])

        else:
            assert(line[0] == 'l')

            acc += int(line[1])
            ct += 1

            if ct == 10:
                cursor.execute(light_insert, acc)
                acc = 0
                ct = 0
