# -*- coding: utf8 -*-

import os # on importe le module os qui dispose de variables
          # et de fonctions utiles pour dialoguer avec votre
          # systeme d'exploitation

from PIL import Image, ImageFilter

import threading
import time

class PictureThread (threading.Thread):
    def __init__(self, threadID, thread_name, picture):
        """ Class's constructor"""
        threading.Thread.__init__(self)
	self.threadID = threadID
        self.picture = picture
        self.thread_name = thread_name

    def run(self):
        """ A COMPLETER """
        picture_processor = new BusbudBanner()
        scaled_picture = picture_processor.scale(self.picture)
        blurred_picture = picture_processor.blur(scaled_picture)
        vertical_picture = crop_top()
        top_picture = crop_bottom()
        bottom_picture = crop_crop_vmiddle()

print "Exiting a Thread"
