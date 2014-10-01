# -*- coding: utf8 -*-

import os # on importe le module os qui dispose de variables
          # et de fonctions utiles pour dialoguer avec votre
          # systeme d'exploitation

from PIL import Image, ImageFilter

import threading
# import time

class ParallelProcessing (threading.Thread):
    """ A COMPLETER"""

    def __init__(self):
	"""Class's constructor"""
        # A COMPLETER

    def execute_threads(self, picture_iterator):
        """A COMPLETER """
        # Create a thread per picture
        thread_index = 1
        threadList = [] # Create an empty list of threads
        for picture in picture_iterator:
             thread = PictureThread(thread_index, "Thread" + picture_index, picture)
             threadList.append(thread)
             picture_index +=1

	# Start all the created Threads
        for thread in threadList
	     thread.start()
	
print "Exiting the parallel processing"