# -*- coding: utf8 -*-

import os

from PIL import Image, ImageFilter

import threading


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
        #print("Loaded image: {}".format(name) + "\n") # Added instruction
        return (name, Image.open(fp))

    @classmethod
    def save(cls, filename, image):
        """Save an image to filename"""
        image.save(filename)
        print("The image has been saved at : {}".format(filename) + "\n") # Added instruction 

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
    def image_data(cls, file_name, file_object):
        """Return the image to process as well as its name and its extension."""
        tuple_to_process = cls.load(file_name, file_object) # assigns an Image
        file_name = tuple_to_process[0]
        image_to_process = tuple_to_process[1]
        drive,path_and_file = os.path.splitdrive(file_name)
        path,file = os.path.split(path_and_file)
        name, extension = file.split(".")
        return  image_to_process, name,  extension
    
    @classmethod
    def scale_blur_crop(cls,  thread_index, imagename, image):
        """Scale, blur and crop the input image."""
        scaled_name =  imagename + "_scaled"
        blurred_name =  imagename + "_blurred"
        print("The thread {} is scaling the image".format(thread_index) + "\n")
        scaled_image = cls.scale_x(scaled_name,  image)

        print("The thread {} is blurring the image".format(thread_index) + "\n")
        blurred_image = cls.blur(blurred_name, scaled_image[1]) # scaled_image is a tuple
    
        print("The thread {} is cropping the image".format(thread_index) + "\n")
        top_image = cls.crop_top(imagename, blurred_image[1])
        bottom_image = cls.crop_bottom(imagename, blurred_image[1])
        middle_image = cls.crop_vmiddle(imagename, blurred_image[1])
        return   top_image, middle_image, bottom_image  


class ImageThread (threading.Thread): 
    """Provide functions to handle a thread allowing an image processing"""

    def __init__(self, threadID, file):
        """ Class's constructor"""
        threading.Thread.__init__(self)
	self.threadID = threadID
        self.file = file


    def run(self):
        # Get the image to process as well as its name and its extension
        image_processor = BusbudBanner()
        image, filename, extension = \
        image_processor.image_data(self.file.name, self.file)
       
        
        # Scale, blur and crop the image
        top_image, middle_image, bottom_image = \
        image_processor.scale_blur_crop(self.threadID, filename, image)

        
        # Save the generated images
        directory_path = "./processed_images/"
        image_processor.save(directory_path + top_image[0] + "." + extension,  \
        top_image[1]) # top_image is a tuple
        image_processor.save(directory_path +  middle_image[0] + "." + extension,  middle_image[1]) 
        image_processor.save(directory_path + bottom_image[0] + "." + extension,  bottom_image[1])
        

class ParallelProcessing (threading.Thread):
    """Provide functions to launch the threads allowing the concurrent 
    processing of images. For more details about threading, see 
    https://docs.python.org/2/library/threading.html#module-threading"""

    def __init__(self):
	"""Class's constructor"""
        pass

    def execute_threads(self, image_iterator):
        """Launch concurrent threads to handle the scaling, blurring
        and cropping of images"""
        # Create a thread per image and start it
        thread_index = 1
        threadList = []
        for image in image_iterator:
             thread = ImageThread(thread_index, image)
             print("The thread {} is launched to process the image {}".format(thread_index, \
             thread.file.name) + "\n")
             thread.start()
             threadList.append(thread)
             thread_index += 1
        
        for thread in threadList:
             thread.join() # to ensure that all the threads have finished

        print("End of the images processing")


def main():
    #raise NotImplementedError
    image_iterator = images()  # get an iterator over the images to process
    concurrency = ParallelProcessing() 
    concurrency.execute_threads(image_iterator) # launch the threads allowing the 
                                                # concurrent processing of the images

    print "Exiting Main Thread"


if __name__ == '__main__':
    main()

# To avoid shutting the program right after its execution (Windows)
os.system("pause")


