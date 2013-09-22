import serial
import time

class ArduinoSerial(object):
	def __init__(self, port, baud_rate):
		self.port = port
		self.baud_rate = baud_rate

	def connect(self):
		print 'Connecting to: %s' % self.port
		try:
			self.conn = serial.Serial(self.port, self.baud_rate)
		except Exception as e:
			print "Something went horribly wrong connecting to the arduino..."
			print "Odds are %s is not the correct port (or the arduino is unplugged)" % self.port
			raise e

		print "Flushing Serial..."
		self.flush(wait = 1)
		self.write('s')
		print "Waiting for ready response..."
		line = self.read_line()
		while 'ready' not in line:
			line = arduino.read_line()

		self.flush(wait = 1)

	def write(self, data, log = True):
		if log:
			print "Sending: %s" % str(data)
		self.conn.write(data)

	def write_line(self, data):
		self.write(data + "\r")

	def read_line(self):
		return self.conn.readline().strip()

	def flush(self, wait = 0.):
		start = time.time()
		while self.conn.inWaiting() or time.time() - start <= wait:
			if self.conn.inWaiting():
				self.conn.read()

	def read_lines(self, block = True, wait = 0.):
		start = time.time()
		if block:
			yield self.read_line()

		while self.conn.inWaiting() or time.time() - start <= wait:
			if self.conn.inWaiting():
				yield self.read_line()


	def close(self, wait = False):
		if wait:
			raw_input("Enter To Close...")
		self.conn.close()
