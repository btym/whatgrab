import whatapi
import cPickle as pickle
import time
import os.path

desired_score = 5 #if the torrent has less than this amount of seeders+leechers, the script will ignore it

try:
	cookies = pickle.load(open('cookies.dat', 'rb'))
	api = whatapi.WhatAPI(username='WHAT USERNAME', password='WHAT PASSWORD', cookies=cookies)
except:
	api = whatapi.WhatAPI(username='WHAT USERNAME', password='WHAT PASSWORD')
while True:
	browse = api.request('browse',searchstr='',format='FLAC',encoding='Lossless')
	for result in browse['response']['results']:
		if len(result['torrents']) > 1:
			continue
		time.sleep(2)
		gid = result['groupId']
		existing = api.request('torrentgroup',id=gid)
		flactorrent = existing['response']['torrents'][0]
		score = flactorrent['seeders'] + flactorrent['leechers']
		if score < desired_score:
			continue
		v0 = False
		for torrent in existing['response']['torrents']:
			if torrent['encoding'] == "V0 (VBR)":
				v0 = True
		if v0:
			continue
		print 'groupId: ' + str(gid)
		for torrent in existing['response']['torrents']:
			print str(torrent['id']) + ": " + torrent['encoding'] + " "+ torrent['format'] + " (" + str(torrent['seeders']) + "/" + str(torrent['leechers']) + ")"
		path = str(flactorrent['id'])+".torrent"
		if os.path.isfile(path):
			continue
		data = api.get_torrent(flactorrent['id'])
		with open(path,"wb") as f:
			f.write(data)
	time.sleep(60)

pickle.dump(api.session.cookies, open('cookies.dat', 'wb'))
