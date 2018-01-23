from mysql import connector
import json


with open('config.json') as f:
    config = json.load(f)


conn = connector.connect(user=config['username'],
                         password=config['password'],
                         host='127.0.0.1',
                         database='arduino')

cursor = conn.cursor()
light_insert = 'INSERT INTO light (measurement) VALUES (%s)'
temp_insert = 'INSERT INTO temperature (measurement) VALUES (%s)'

with open('/dev/ttyUSB0', encoding='ascii') as f:
    loop_ct = 1
    light_ct = 0
    acc = 0

    for line in f:
        segments = line.strip().lower().split(' ')

        if len(segments) != 2:
            continue

        if segments[0] == 't':
            cursor.execute(temp_insert, (segments[1],))

        else:
            assert(segments[0] == 'l')

            acc += int(segments[1])
            light_ct += 1

            if light_ct == 10:
                cursor.execute(light_insert, (acc/10,))
                acc = 0
                light_ct = 0

        loop_ct += 1
        if loop_ct % 100 == 0:
            conn.commit()
