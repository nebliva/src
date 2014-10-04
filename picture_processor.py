# -*- coding: utf8 -*-

import os

from PIL import Image, ImageFilter

import threading
#import time

def images():
    image_dir = os.walk('./images').next()
    for filename in image_dir[2]:
        yield open(os.path.join(image_dir[0], filename), 'rb')


class BusbudBanner(object):
    """Image manipulation functions for Busbud Banners."""

    def __init__(self):
	"""Class's constructor"""
        pass

    @classmethod
    def load(cls, name, fp):
        """Load an image from a file pointer."""
        #print("Loaded picture: {}".format(name) + "\n") # Added instruction
        return (name, Image.open(fp))

    @classmethod
    def save(cls, filename, image):
        """Save an image to filename"""
        image.save(filename)
        print("The picture has been saved at : {}".format(filename) + "\n") # Added instruction 

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
        return name + '-vmiddle', cls.crop_vertical(image, offset, y - offset)
    
    @classmethod
    def picture_data(cls, file_name, file_object):
        """Return the image to process as well as its name and its extension."""
        tuple_to_process = cls.load(file_name, file_object) # assigns an Image
        file_name = tuple_to_process[0]
        picture_to_process = tuple_to_process[1]
        drive,path_and_file = os.path.splitdrive(file_name)
        path,file = os.path.split(path_and_file)
        picture_name, extension = file.split(".")
        return  picture_name,  picture_to_process, file_name, extension
    
    @classmethod
    def scale_blur_crop(cls,  thread_index, picture_name, picture_to_process, extension):
        """Scale, blur and crop the input image."""
        top_name = picture_name + "-top" + "." + extension
        middle_name =  picture_name + "-vmiddle"  + "." + extension
        bottom_name =  picture_name + "-bottom" + "." + extension
        scaled_name =  picture_name + "_scaled" + "." + extension
        blurred_name =  picture_name + "_blurred" + "." + extension

        print("The thread {} is scaling the picture".format(thread_index) + "\n")
        scaled_picture = cls.scale_x(scaled_name,  picture_to_process)

        print("The thread {} is blurring the picture ".format(thread_index) + "\n")
        blurred_picture = cls.blur(blurred_name, scaled_picture[1]) # scaled_picture is a tuple
    
        print("The thread {} is cropping the picture".format(thread_index) + "\n")
        top_picture = cls.crop_top(top_name, blurred_picture[1])
        bottom_picture = cls.crop_bottom(bottom_name, blurred_picture[1])
        middle_picture = cls.crop_vmiddle(middle_name, blurred_picture[1])
        return   top_name, middle_name, bottom_name, top_picture, middle_picture, bottom_picture  


class PictureThread (threading.Thread):
    def __init__(self, threadID, file):
        """ Class's constructor"""
        threading.Thread.__init__(self)
	self.threadID = threadID
        self.file = file


    def run(self):
        """ A COMPLETER """
        # Get the image to process as well as its name and its extension
        picture_processor = BusbudBanner()
        picture_name, picture_to_process, file_name, extension = \
        picture_processor.picture_data(self.file.name, self.file)
       
        
        # Scale, blur and crop the picture
        top_name, middle_name, bottom_name, top_picture, middle_picture, bottom_picture = \
        picture_processor.scale_blur_crop(self.threadID, picture_name, picture_to_process, extension)

        
        # Save the generated pictures
        directory_path = "./processed_images/"
        picture_processor.save(directory_path + top_name,  top_picture[1]) # top_picture is a tuple
        picture_processor.save(directory_path + middle_name,  middle_picture[1]) # middle_picture is a tuple
        picture_processor.save(directory_path + bottom_name,  bottom_picture[1]) # bottom_picture is a tuple
        

class ParallelProcessing (threading.Thread):
    """ A COMPLETER
    For more details, see http://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing"""

    def __init__(self):
	"""Class's constructor"""
        pass

    def execute_threads(self, picture_iterator):
        """A COMPLETER """
        # Create a thread per picture and start it
        thread_index = 1
        threadList = []
        for picture in picture_iterator:
             thread = PictureThread(thread_index, picture)
             print("The thread {} is launched to process the picture {}".format( thread_index, \
             thread.file.name) + "\n")
             thread.start()
             threadList.append(thread)
             thread_index += 1
        
        for thread in threadList:
             thread.join() # to ensure that all the threads have finished

        print("End of the images processing")


def main():
    """ A COMPLETER"""
    #raise NotImplementedError
    picture_iterator = images()  # get an iterator over the pictures to process
    concurrency = ParallelProcessing() 
    concurrency.execute_threads(picture_iterator) # launch the threads allowing to concurrently process the pictures

    print "Exiting Main Thread"


if __name__ == '__main__':
    main()

# To avoid the program to shut right after the execution (Windows)
os.system("pause")


