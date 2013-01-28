# -*- coding: utf-8 -*-
import cv

MIN_SIZE = 1000
MIN_THOLD = 60

class Camera:
    def __init__(self, camera):
        self._cam = cv.CaptureFromCAM(camera)

    def calibrate(self):
        cv.NamedWindow('calibration')
        while True:
            f = cv.QueryFrame(self._cam)
            red = self.getRedChannel(f)
            seq = cv.FindContours(red, 
                cv.CreateMemStorage(0), 
                cv.CV_RETR_EXTERNAL, 
                cv.CV_CHAIN_APPROX_SIMPLE)
            while seq:
                size = abs(cv.ContourArea(seq))
                if size > MIN_SIZE:
                    bb = cv.BoundingRect(seq, 0)
                    center = (bb[0]+bb[2]/2, bb[1]+bb[3]/2)
                    cv.Circle(f, center, 10, cv.Scalar(0,255,0))
                seq = seq.h_next()
            cv.ShowImage('calibration', f)
            cv.WaitKey(33)

    def getRedChannel(self, image):
        chR = cv.CreateImage(cv.GetSize(image), 8, 1)
        chG = cv.CreateImage(cv.GetSize(image), 8, 1)
        chB = cv.CreateImage(cv.GetSize(image), 8, 1)
        cv.Split(image, chB, chG, chR, None)
        cv.Add(chB, chG, chG);
        cv.Sub(chR, chG, chR);
        cv.Threshold(chR, chR, MIN_THOLD, 255, cv.CV_THRESH_BINARY)
        return chR

    def getCoords(self):
        f = cv.QueryFrame(self._cam)
        seq = cv.FindContours(red, 
            cv.CreateMemStorage(0), 
            cv.CV_RETR_EXTERNAL, 
            cv.CV_CHAIN_APPROX_SIMPLE)
        while seq:
            size = abs(cv.ContourArea(seq))
            if size > MIN_SIZE:
                bb = cv.BoundingRect(seq, 0)
                center = (bb[0]+bb[2]/2, bb[1]+bb[3]/2)
                yield center
            seq = seq.h_next()
  
    def getSize(self):
        height = cv.GetCaptureProperty(self._cam, cv.CV_CAP_PROP_FRAME_HEIGHT)
        width = cv.GetCaptureProperty(self._cam, cv.CV_CAP_PROP_FRAME_WIDTH)
        return (width, height)

class Disposition:
    def __init__(self, camera):
        self._cam = Camera(camera)
        self._size = self._cam.getSize()

    def getRelativeCoords(self):
        coords = []
        for pos in self._c.getCoords():
            Rx = pos[0] / self._size[0]
            Ry = pos[1] / self._size[1]
            coords.append((Rx, Ry))
        return coords

    def test(self):
        if len(self.getRelativeCoords()) != 3:
            return True
        return False

