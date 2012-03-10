#from bluetooth import BluetoothSocket, RFCOMM
#from homer import HOMER
import httplib, urllib, urllib2, time, thread, os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from django.utils import simplejson
import socket


BLUETOOTH_ADDR = "00:0A:84:02:5F:47"
SERVER = "localhost:8000"

def appengine_cam():
#		os.system("fswebcam --title HOMER-SP --jpeg 40 -F 2 -S 1 -q tmp.jpg")
	datagen, headers = multipart_encode({
#			'img': open('tmp.jpg', 'rb')
		'server': simplejson.dumps({'name':'homerko', 'module_name':'homer', 'version': 1}),
		'client': 'tete'
	})
	request = urllib2.Request("http://%s/dcu/" % SERVER, datagen, headers)
	try:
		getdata = urllib2.urlopen(request)
		print getdata.read()
	except urllib2.HTTPError, error:
		print error.read()

if __name__ == '__main__':
	register_openers()

#	sock = BluetoothSocket( RFCOMM )
#	sock.connect((BLUETOOTH_ADDR, 1))
#	sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	sock.connect(('', 50007))
	appengine_cam()
#	appengine_client(HOMER(sock))
