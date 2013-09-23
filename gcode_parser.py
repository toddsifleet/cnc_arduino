import operator
import re

valid_gcode_commands = ['G1', 'G0']

def parse_line(line):
    without_comments = line.split('(')[0].strip()
    args = re.split(' +', without_comments)

    if not args or args[0] not in valid_gcode_commands:
        return None

    parse_arg = lambda i: (i[0], float(i[1:]))
    return dict(
        command = args[0],
        **dict(map(parse_arg, args[1:]))
    )


def parse_gcode_file(file):
    for line in file:
        cmd = parse_line(line)
        if cmd:
            yield cmd


if __name__ == '__main__':
    for c in parse_gcode_file(open('test.gcode')):
        print c
