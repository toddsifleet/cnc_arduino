import gcode_interpreter
import gcode_parser
import serial_transmitter
import time
import sys

arduino = serial_transmitter.ArduinoSerial('/dev/tty.usbmodem641', 9600)
arduino.connect()

steps_per_rotation = 200 * 32
mm_per_rotation = 8
steps_per_mm = steps_per_rotation / mm_per_rotation

def get_route(file_name):
	g_code = gcode_parser.parse_gcode_file(open(file_name)) 
	points = gcode_interpreter.get_points(g_code)
	movements = gcode_interpreter.get_movements(points)
	return gcode_interpreter.map_to_steps(movements, steps_per_mm)

def run_gcode(file_name):
	for movement in get_route('test.gcode'):
		cmd = '%d %d %d' % tuple(movement)
		arduino.write(cmd)
		print "Reading...."
		for i in arduino.read_lines(count = 2):
			print i
	arduino.close(wait = True)

def run_manual():
	cmd = raw_input('Action: ').strip()
	while 'exit' not in cmd:
		arduino.write(cmd)
		print "Reading...."
		for i in arduino.read_lines(count = 2):
			print i
		cmd = raw_input('Action: ')
	arduino.close()

def run():
	if len(sys.argv) > 1:
		run_gcode(sys.argv[1])
	else:
		run_manual()

run()
