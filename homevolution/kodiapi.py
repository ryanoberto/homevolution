#!/usr/bin/python
import requests
import json
import sqlite3

conn = sqlite3.connect('homevolution.db')
conn.row_factory = sqlite3.Row
con = conn.cursor()
con.execute('SELECT name, port from kodi')
row = con.fetchone()
port = row[1]
host = row[0]



#port='8080'
#host='192.168.1.11'
url="http://"+host+":"+port+"/jsonrpc"

#payload = {'key1': 'value1', 'key2': 'value2'}
#payload={"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
#r = requests.post("http://192.168.1.11:8080/jsonrpc", data=payload)
#print(r.text)

# prints status code
#r.status_code
# prints headers
#r.headers

#r = requests.post('http://192.168.1.11:8080/jsonrpc', json={"jsonrpc": "2.0","method": "Player.GetItem","params": {"properties": ["title","album","artist","season","episode","duration","showtitle","tvshowid","thumbnail","file","fanart","streamdetails"],"playerid": 1},"id": "VideoGetItem"})
#r = requests.post('http://192.168.1.11:8080/jsonrpc', json={"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1})
# show options
#r = requests.post('http://192.168.1.11:8080/jsonrpc', json={ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "params": { "filter": { "id": "AudioLibrary.GetAlbums", "type": "method" } }, "id": 1 })

#get volume level
#r = requests.post('http://192.168.1.11:8080/jsonrpc', json={"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["volume"]}, "id": 1})

#print(r.text)

#r = request.post(url,json={ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "params": { "filter": { "id": "Input", "type": "method" } }, "id": 1 })

def play():
	r = requests.post(url, json={"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": 1 }, "id": 1})
	parsed = r.json()
        return json.dumps(parsed, indent=4, sort_keys=True)

def stop():
	r = request.post(url, json={"jsonrpc": "2.0","method": "Player.Stop","params": {"playerid": 0 },"id": 1})
	parsed = r.json()
        return json.dumps(parsed, indent=4, sort_keys=True)

def volumeup():
	#Get current Volume
	"""Increment by 5"""
	r = requests.post(url, json={"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["volume"]}, "id": 1})
	volume = r.json()
	vol = volume['result']['volume']
	vol = vol + 5
	r = requests.post(url, json={"jsonrpc": "2.0","method": "Application.SetVolume","params": {"volume": vol,},"id": 1})
	parsed = r.json()
        return json.dumps(parsed, indent=4, sort_keys=True)
	
def volumedwn():
	#Get current Volume
        """Decrese by 5"""
        r = requests.post(url, json={"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["volume"]}, "id": 1})
        volume = r.json()
        vol = volume['result']['volume']
        vol = vol - 5
        r = requests.post(url, json={"jsonrpc": "2.0","method": "Application.SetVolume","params": {"volume": vol,},"id": 1})
        parsed = r.json()
        return json.dumps(parsed, indent=4, sort_keys=True)


#r = requests.post(url, json={"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1})
def getplaying():	
	r = requests.post(url, json={"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "album", "season", "episode", "showtitle", "tvshowid", "thumbnail", "file", "fanart"], "playerid": 1 }, "id": "VideoGetItem"})
	parsed = r.json()
	return json.dumps(parsed, indent=4, sort_keys=True)

