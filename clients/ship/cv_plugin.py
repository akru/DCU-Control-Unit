# -*- coding: utf-8 -*-
import cv

class Camera:
  def __init__(self, camera):
    self._cam = cv.CaptureFromCAM(camera)
    
    self.calibrate()

  def calibrate(self):
    cv.NamedWindow('orig')
    cv.NamedWindow('thold')
    while True:
      f = cv.QueryFrame(self._cam)
      red = self.getRedChannel(f)
      cont = self.getContours(red)
      for i in cont:
        print i
      cv.ShowImage('orig', f)
      cv.ShowImage('thold', red)
      cv.WaitKey(33)

  def getCoords(self):
    f = cv.QueryFrame(self._cam)
    red = self.getRedChannel(f)
    cont = self.getContours(red)


  def getContours(self, image):
    cont = cv.CreateMemStorage(0)
    cv.FindContours(image, cont)
    return cont

  def getRedChannel(self, image):
    chR = cv.CreateImage(cv.GetSize(image), 8, 1)
    chG = cv.CreateImage(cv.GetSize(image), 8, 1)
    chB = cv.CreateImage(cv.GetSize(image), 8, 1)
    cv.Split(image, chB, chG, chR, None)
    cv.Add(chB, chG, chG);
    cv.Sub(chR, chG, chR);
    cv.Threshold(chR, chR, 20, 255, cv.CV_THRESH_BINARY)
    return chR


class Disposition:
  def __init__(self, camera):
    pass

  def test(self):
    return False
