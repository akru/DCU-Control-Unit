# SSC32 Servo Controller
import time

class SSC32Controller:
	""" SSC32 controller communication """
	def __init__(self, numServo, leftTrack, rightTrack, sock):
		self._nums = numServo
		self._sock = sock
		self._pvec = []
		self._time = 2000
		self._left = leftTrack
		self._right = rightTrack
		self._leftc = 1500   # Left track control
		self._rightc = 1500  # Right track control

	def setPositionVector(self, vect):
		""" Set servo position """
		self._pvec = vect

	def setTimeDuration(self, time):
		""" Set duration of movements """
		self._time = time

	def flush(self):
		""" Send state to SSC32 """		
		for servo in range(self._nums):
			self._sock.send("#%d P%d" % (servo, self._pvec[servo]))
		self._sock.send("#%d P%d" % (self._left, self._leftc))
		self._sock.send("#%d P%d" % (self._right, self._rightc))
		self._sock.send(" T%d\r" % self._time)

	def positionIsSet(self):
		""" Verify position state """
		self._sock.send("Q\r")
		if self._sock.recv(1) == ".":
			return True
		return False

	def setTrackPos(self, leftControl, rightControl):
		self._leftc = leftControl
		self._rightc = rightControl
		self.flush()

