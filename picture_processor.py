# -*- coding: utf8 -*-

import os

from PIL import Image, ImageFilter

import threading
import time

def images():
    image_dir = os.walk('./images').next()
    for filename in image_dir[2]:
        yield open(os.path.join(image_dir[0], filename), 'rb')


class BusbudBanner(object):
    """Image manipulation functions for Busbud Banners."""

    @classmethod
    def load(cls, name, fp):
        """Load an image from a file pointer."""
        return (name, Image.open(fp))

    @classmethod
    def save(cls, filename, image):
        """Save an image to filename"""
        image.save(filename)

    @classmethod
    def scale_x(cls, name, image, size=1500, resample=Image.BICUBIC):
        """Scale the image along its x-axis to `size` pixels."""
        x, y = image.size
        scale = float(x) / size
        x_size = size
        y_size = int(round(y / scale))
        return name, image.resize((x_size, y_size), resample)

    @classmethod
    def blur(cls, name, image, radius=6):
        """Apply a Gaussian blur to image."""
        return name + '-blur', image.filter(ImageFilter.GaussianBlur(radius))

    @classmethod
    def crop_vertical(cls, image, y_1, y_2):
        """Crop an image along its y-axis."""
        x = image.size[0]
        return image.crop((0, y_1, x, y_2))

    @classmethod
    def crop_top(cls, name, image, height=300):
        """Crop `image` to `height` pixels from the top."""
        return name + '-top', cls.crop_vertical(image, 0, height)

    @classmethod
    def crop_bottom(cls, name, image, height=300):
        """Crop `image` to `height` pixels from the bottom."""
        y = image.size[1]
        return name + '-bottom', cls.crop_vertical(image, y - height, y)

    @classmethod
    def crop_vmiddle(cls, name, image, height=300):
        """Crop `image` to `height` pixels from the middle."""
        y = image.size[1]
        offset = (y - height) / 2
        return name + '-vmiddle', cls.crop_verticall(image, offset, y - offset)


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


class ParallelProcessing (threading.Thread):
    """ A COMPLETER"""

    def __init__(self):
	"""Class's constructor"""
        pass

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
        index = 0 # 
	while index < len(threadList):
            threadList[index].start
            index += 1 # incrementation de l'index
            print("The thread {} is running".format(index))


def main():
    """ A COMPLETER"""
    #raise NotImplementedError
    picture_iterator = images()  # get an iterator over the pictures to process
    concurrency = ParallelProcessing() 
    concurrency.execute_threads( picture_iterator) # launch  the threads allowing to concurrently process the pictures

    print "Exiting Main Thread"


if __name__ == '__main__':
    main()


# To avoid the program to shut right after the execution (Windows)
os.system("pause")
