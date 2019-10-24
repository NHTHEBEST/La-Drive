#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name:        Quiz 0.1.5
# Purpose:     Download magnet links from url and upload completed file
#
# Author:      cosmo.zavoda
#
# Created:     25/09/2019
# Copyright:   (c) cosmo.zavoda 2019 (The Drive)
# Licence:     MIT 
# Change Log:
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Getting an error on HASH in magnet links its being a bitch
#
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# globals
#<<<<<<< HEAD
#=======
URL     = "http://noserver.hadar.net.nz/thedrive/"       #URL for downloading magnet link
#>>>>>>> dbce5bc6b8bc41261eb33f610150b20a88fbaaee
#global URL
DELFILE = True    #Deletes downloaded data after uploading
#global DELFILE
SAVEPATH= "/tmp/stuff/"       #Path to dumped data 
#global SAVEPATH
UPDDELAY= 60       #Delay between database syncs
#global UPDDELAY
UPLOADCMD = "gdrive upload -p 1BMRqZT7fwv0X_ZzweNrePfd3pgqaJ8Il -r "
#global UPLOADCMD
HASH    = ""       #hash to download
#global HASH
#Trakers
TRAKERS_file = open("trakers.txt","r")
TRAKERS = TRAKERS_file.read()
#print(TRAKERS)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# modules
import libtorrent as lt
import time
import os
import requests
#-------------------------------------------------------------------------------


#loop for ever
#gethash
# if gethash returns nothing
#deley of UPDDELAY
#end if
# torrent
# upload
# delet
# update server of completion

#-------------------------------------------------------------------------------
# torrenter
def torrent():
	ses = lt.session()
	ses.listen_on(6881, 6891)
	params = {
		'save_path': SAVEPATH,
		'storage_mode': lt.storage_mode_t(2),
		'paused': False,
		'auto_managed': True,
		'duplicate_is_error': True}
	link = "magnet:?xt=urn:btih:"+HASH+TRAKERS
	print(link)
	handle = lt.add_magnet_uri(ses, link, params)
	ses.start_dht()

	print('downloading metadata...')
	while (not handle.has_metadata()):
		time.sleep(1)
		print("#", end = '')
	print('got metadata, starting torrent download...')
	while (handle.status().state != lt.torrent_status.seeding):
		 s = handle.status()
		 state_str = ['queued', 'checking', 'downloading metadata', \
					 'downloading', 'finished', 'seeding', 'allocating']
		# print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3' % \
		#		(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
		#		s.num_peers, state_str[s.state], s.total_download/1000000)
		 print(s.progress*100,end="\r")
		 time.sleep(5)
#-------------------------------------------------------------------------------
#get the hash from server
def gethash():
	output = requests.get(URL+"get.php").text
	print("hash is:"+output)
	print("url reveived")
	return output
#-------------------------------------------------------------------------------
#upload file to the drive
def upload():
	os.system("rm /tmp/stuff/**/*.jpg /tmp/stuff/**/*.txt /tmp/stuff/**/*.sub /tmp/stuff/**/*.png /tmp/stuff/**/*.str")
	os.system(UPLOADCMD+str(SAVEPATH)+"*")
	print("file uploaded")
#-------------------------------------------------------------------------------
#delete uploaded data
def deldata():
	if DELFILE:
		os.system("rm -r "+SAVEPATH+"*")
		print("File deleted")
#-------------------------------------------------------------------------------
# updates the server
def updateserver(hash):
	requests.get(URL+"/rm.php?key=625c93b5-fbfe-4ea5-921d-27b7da51aa10&hash="+hash)
	print("server updated")
#-------------------------------------------------------------------------------
#main
while True:
	hash = gethash()
	if hash == "":
		time.sleep(UPDDELAY)
	else:
		HASH = hash
		torrent()
		upload()
		deldata()
		updateserver(hash)
#-------------------------------------------------------------------------------
