#!/usr/bin/env python3

import sys
import json

cast_files = sys.argv[1:]

t_offset = 0
t_last = 0
entry = [0]
max_idle = 5

for idx, cast_file in enumerate(cast_files):
    lines = open(cast_file, 'r').read().split('\n')
    meta = lines[0]
    data = lines[1:]

    if idx == 0:
        print(meta)

    for entry_raw in data:
        if entry_raw:
            # read entry and offset time stamp
            entry = json.loads(entry_raw)
            entry[0] += t_offset

            # check for long idles
            if entry[0] > t_last + max_idle:
                idle_delta = entry[0] - t_last - max_idle
                entry[0] -= idle_delta
                t_offset -= idle_delta
            t_last = entry[0]

            print(json.dumps(entry))

    t_offset = entry[0] + 3
