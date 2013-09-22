import operator
import re

valid_gcode_commands = ['G1', 'G0']

def parse_line(input):
    line = re.split(' +', input.split('(')[0].strip())
    if not line or line[0] not in valid_gcode_commands:
        return None

    arguments = dict(map(lambda i: (i[0], float(i[1:])), line[1:]))
    return dict(
        command = line[0],
        **arguments
    )


def parse_gcode_file(file):
    for line in file:
        cmd = parse_line(line)
        if cmd:
            yield cmd


if __name__ == '__main__':
    for c in parse_gcode_file(open('test.gcode')):
        print c
