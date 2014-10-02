# -*- coding: utf8 -*-

import os # on importe le module os qui dispose de variables
          # et de fonctions utiles pour dialoguer avec votre
          # systeme d'exploitation

import picture
import parallelism

from PIL import Image, ImageFilter

import threading
# import time

class ParallelProcessing (threading.Thread):
    """ Cette classe permet de lancer et de gerer l'execution
        de plusieurs threads. Des fonctionnalites pourront lui etre
        rajoutees afin qu'elle permette de suspendre un thread, de 
        l'annuler, d'accorder plus de ressources d'execution a des
        threads donnes, etc."""

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

      def execute_threads_cores(self, picture_iterator):
      	    """Run a list of threads using all the CPU cores """
            pass # completer cette fonction
       
	
print "Exiting the parallel processing"