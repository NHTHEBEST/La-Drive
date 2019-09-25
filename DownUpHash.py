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
# globals
URL     = ""       #URL for downloading magnet link
global URL
DELFILE = False    #Deletes downloaded data after uploading
global DELFILE
SAVEPATH= ""       #Path to dumped data 
global SAVEPATH
UPDDELAY= 60       #Delay between database syncs
global UPDDELAY
UPLOADCMD = "gdrive upload -p 1BMRqZT7fwv0X_ZzweNrePfd3pgqaJ8Il -r "
global UPLOADCMD
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# modules
import libtorrent as lt
import time
import os
import requests
#-------------------------------------------------------------------------------

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
	link = URL
	handle = lt.add_magnet_uri(ses, link, params)
	ses.start_dht()

	print 'downloading metadata...'
	while (not handle.has_metadata()):
	    time.sleep(1)
	print 'got metadata, starting torrent download...'
	while (handle.status().state != lt.torrent_status.seeding):
		filedown = False
#-------------------------------------------------------------------------------
#get the magnet url
def geturl():
	output = requests.get(URL).text
	print(output)
	print("url reveived")
#-------------------------------------------------------------------------------
#upload file to the drive
def upload():
	os.system(UPLOADCMD+str(SAVEPATH))
	print("file uploaded")
#-------------------------------------------------------------------------------

