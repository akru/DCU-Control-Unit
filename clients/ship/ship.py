# -*- coding: utf-8 -*-
from cv_plugin import Disposition
from time import sleep


class Led:
  def __init__(self, sock):
    self.s = sock
    self._state = 4

  def test(self):
    for state in range(0, 5):
      if self.set_state(state):
        return True
      sleep(0.3)
    return False

  def enable(self):
    self.set_state(3)

  def disable(self):
    self.set_state(4)

  def set_state(self, state):
    self.s.send("%c" % 127)
    sleep(0.1)
    self.s.send("%c" % state)
    sleep(0.1)
    self._state = state
    return False

  def get_state(self):
    return self._state


class Drive:
  def __init__(self, sock):
    self.s = sock
    self._state = {0:127, 1:127, 2:127, 3:127}

  def test(self):
    for motor in range(0, 4):
      for value in [20, 127, 190, 127]:
        if self.set_control(motor, value):
          return True
        sleep(1)
    return False
  
  def set_control(self, motor, value):
    print 'SHIP: motor/speed: %d/%d' % (motor, value)
    self.s.send("%c" % 255)
    self.s.send("%c" % int(motor))
    self.s.send("%c" % int(value))
    self._state[motor] = value
    return False

  def get_state(self):
    return self._state

class SHIP:
  def __init__(self, sock, camera):
    self.s = sock;
    self.led = Led(sock)
    self.drv = Drive(sock)
    self.dsp = Disposition(camera)
    print 'SHIP: Led test'
    if self.led.test():
      print "SHIP: Led test Fail"
    print 'SHIP: Motor test'
    if self.drv.test():
      print "SHIP: Drive test Fail"
    print 'SHIP: Desposition test'
    if self.dsp.test():
      print "SHIP: Disposition test Fail"

  def raw_control(self, state):
    try:
      for motor in range(0, 4):
        if self.drv.set_control(motor, state["drive"][motor]):
          print "SHIP: raw_c :: drv.set_control Fail"
      if self.led.set_state(state["led"]):
        print "SHIP: raw_c :: led.set_state Fail"
    except:
      pass

  def get_state(self):
    return {"drive": self.drv.get_state(), "led": self.led.get_state()}

