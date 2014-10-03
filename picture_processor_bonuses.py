# -*- coding: utf8 -*-

import os
import multiprocessing

from PIL import Image, ImageFilter


def images():
    image_dir = os.walk('./images').next()
    for filename in image_dir[2]:
        yield open(os.path.join(image_dir[0], filename), 'rb')


class BusbudBanner(object):
    """Image manipulation functions for Busbud Banners."""

    def __init__(cls):
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
    def scale(cls, name, image, size=1500, resample=Image.BICUBIC):
        """Scale the image along its x-axis to `size` pixels.
           Note that I removed the x from that function in order 
           to redefine that function and benefit from polymorphism."""
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
        print("data to open in that function : {}".format(file_name))
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
        scaled_picture = cls.scale(scaled_name,  picture_to_process)
        print("The thread {} is blurring the picture ".format(thread_index) + "\n")
        blurred_picture = cls.blur(blurred_name, scaled_picture[1]) # scaled_picture is a tuple
        print("The thread {} is cropping the picture".format(thread_index) + "\n")
        top_picture = cls.crop_top(top_name, blurred_picture[1])
        bottom_picture = cls.crop_bottom(bottom_name, blurred_picture[1])
        middle_picture = cls.crop_vmiddle(middle_name, blurred_picture[1])
        return   top_name, middle_name, bottom_name, top_picture, middle_picture, bottom_picture  


class BusbudBannerBonus(BusbudBanner):
    """Added for bonus to enable scaling along the 
    y axis and cropping along the x. """

    def __init__(cls):
	"""Class's constructor"""
        pass

    @classmethod
    def scale(cls, name, image, size=1500, resample=Image.BICUBIC):
        """Scale the image along its y-axis to `size` pixels."""
        x, y = image.size
        scale = float(y) / size
        y_size = size
        x_size = int(round(x / scale))
        return name, image.resize((x_size, y_size), resample)

    @classmethod
    def crop_horizontal(cls, image, x_1, x_2):
        """Crop an image along its x-axis."""
        y = image.size[1]
        return image.crop((x_1, 0, x_2, y))

    @classmethod
    def crop_bottom(cls, name, image, width=300):
        """Crop `image` to `width` pixels from the bottom."""
        return name + '-top', cls.crop_horizontal(image, 0, width)

    @classmethod
    def crop_top(cls, name, image, width=300):
        """Crop `image` to `width` pixels from the top."""
        x = image.size[0]
        return name + '-bottom', cls.crop_horizontal(image, x - width, x)

    @classmethod
    def crop_vmiddle(cls, name, image, width=300):
        """Crop `image` to `width` pixels from the middle."""
        x = image.size[0]
        offset = (x - width) / 2
        return name + '-vmiddle', cls.crop_horizontal(image, offset, x - offset)


class ParallelProcessing ():
    """ A COMPLETER
    For more details, see http://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing"""

    def __init__(self):
	"""Class's constructor"""
        pass

    def execute_process(self, file, threadID):
        """ A COMPLETER """
        # Get the image to process as well as its name and its extension
        picture_processor = BusbudBannerBonus()
        picture_name, picture_to_process, file_name, extension = \
        picture_processor.picture_data(file.name, file)
        
        # Scale, blur and crop the picture
        top_name, middle_name, bottom_name, top_picture, middle_picture, bottom_picture = \
        picture_processor.scale_blur_crop(threadID, picture_name, picture_to_process, extension)

        # Save the generated pictures
        directory_path = "./processed_images/"
        picture_processor.save(directory_path + top_name,  top_picture[1]) # top_picture is a tuple
        picture_processor.save(directory_path + middle_name,  middle_picture[1]) # middle_picture is a tuple
        picture_processor.save(directory_path + bottom_name,  bottom_picture[1]) # bottom_picture is a tuple
        

    def execute_threads(self, picture_iterator):
        """Concurrently execute processes using all the cpu cores"""
        # Create a thread per picture and start it
        process_index = 1
        processList = []
        for picture in picture_iterator:
            process_ = multiprocessing.Process(target=self.execute_process, args=(picture, process_index))
            process_.start() # to concurrently use all the cpu cores
            print("The process {} is launched to process the picture {}".format(process_index, \
            picture.name) + "\n")
            processList.append(process_)
            process_index += 1
        
       # for thread in threadList:
           # thread.process_.join() # to ensure that all the processes have finished

        print("End of the images processing using all the cpu cores")


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
#os.system("pause")


