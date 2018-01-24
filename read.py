#!/usr/bin/env python

from mysql import connector
from serial.tools import list_ports
import json

LIGHT_CT = 250
LOOP_CT = 1000

with open('config.json') as f:
    config = json.load(f)


conn = connector.connect(user=config['username'],
                         password=config['password'],
                         host='127.0.0.1',
                         database='arduino')

print('connected to database')

cursor = conn.cursor()
light_insert = 'INSERT INTO light (measurement) VALUES (%s)'
temp_insert = 'INSERT INTO temperature (measurement) VALUES (%s)'

ports = list_ports.comports(include_links=True)

print('got the following ports:')
print(',\n'.join([port.device for port in ports]))

print('\nusing first found port')

with open(ports[0].device, encoding='ascii') as f:
    loop_ct = 1
    light_ct = 1
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

            if light_ct % LIGHT_CT == 0:
                cursor.execute(light_insert, (acc/10,))
                acc = 0

        loop_ct += 1
        if loop_ct % LOOP_CT == 0:
            conn.commit()
