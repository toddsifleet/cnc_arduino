import operator
import re

def linear_interpolate(position, command):
    next_position = list(position)
    for i, a in enumerate('XYZ'):
        if a in command:
            next_position[i] = command[a]

    return [tuple(next_position)]

gcode_commands = {
    'G1': linear_interpolate,
    'G0': linear_interpolate
}


def get_movements(points, current_position = (0, 0, 0)):
    for point in points:
        yield tuple(map(operator.sub, point, current_position))
        current_position = point

def run_command(position, command):
    return gcode_commands[command['command']](position, command)

def get_points(gcode, position = (0, 0, 0)):
    for command in gcode:
        for point in  run_command(position, command):
            yield point
        position = point

def map_to_steps(movements, step_per):
    def scale(val):
        return int(step_per * val)

    return map(lambda x: map(scale , x), movements)


if __name__ == '__main__':
    import gcode_parser
    gcode = gcode_parser.parse_gcode_file(open('test.gcode'))
    points = get_points(gcode)
    movements = get_movements(points)

    for m in map_to_steps(movements, 100):
        print m 

