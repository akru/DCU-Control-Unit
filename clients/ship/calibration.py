from cv_plugin import Camera

c = Camera(0)
print 'Capture size:', c.getSize()
c.calibrate()
