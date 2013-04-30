import db

class Request(object):
    def __init__(self, name, song, artist, album):
        self.name = name
        self.song = song
        self.artist = artist
	self.album = album
