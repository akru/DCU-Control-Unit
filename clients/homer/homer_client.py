from homer import HOMER
import httplib, urllib, urllib2, time, thread, os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from django.utils import simplejson
import socket


def homer_client(sock):
	h = HOMER(sock)
	while True:
		datagen, headers = multipart_encode({
			'server': simplejson.dumps({'name':'homer-1', 'module_name':'homer', 'version': 1}),
			'client': 'get_tc'
		})
		request = urllib2.Request("http://%s/dcu/" % SERVER, datagen, headers)
		try:
			getdata = urllib2.urlopen(request)
			if getdata in "client":
				c = simplejson.loads(getdata["client"])
				h.setTrackControl(c["track_left"], c["track_right"])
			else:
				print getdata
		except urllib2.HTTPError, error:
			print error.read()

if __name__ == '__main__':
	register_openers()
	sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('', 50007))
	homer_client(sock)
