# -*- coding: utf8 -*-

import os
from multiprocessing import Process

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
    def picture_data(cls, image_tuple):
        """Function added to get the image's name and extension."""
        
        file_name = image_tuple[0]
        drive,path_and_file = os.path.splitdrive(file_name)
        path,file = os.path.split(path_and_file)
        name, extension = file.split(".")
        return  name, extension
    
    @classmethod
    def scale_blur_crop(cls,  process_index, name, image):
        """Function added to Scale, blur and crop the input image."""
        scaled_name =  name + "_scaled"
        blurred_name =  name + "_blurred"

        print("The process {} is scaling the picture".format(process_index) + "\n")
        scaled_image = cls.scale(scaled_name,  image)
        print("The process {} is blurring the picture ".format(process_index) + "\n")
        blurred_image = cls.blur(blurred_name, scaled_image[1]) # scaled_image is a tuple
        print("The process {} is cropping the picture".format(process_index) + "\n")
        top_image = cls.crop_top(name, blurred_image[1])
        bottom_image = cls.crop_bottom(name, blurred_image[1])
        middle_image = cls.crop_vmiddle(name, blurred_image[1])
        return  top_image, middle_image, bottom_image  


class BusbudBannerBonus(BusbudBanner):
    """Provide support for image scaling along the y axis and cropping 
    along the x. """

    def __init__(cls):
	"""Class's constructor."""
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


class ImageProcess ():
    """ Provide functions to handle a process allowing the scaling,
    blurring and cropping of an image"""

    def __init__(self, threadID, tuple_picture):
        """ Class's constructor"""
	self.threadID = threadID
        self.tuple_picture = tuple_picture 
        self.process_ = Process(target=self.run_process)


    def run_process(self):
        """ Produce 3 images from the scaling, blurring and cropping of an image
        and save these 3 images. """
        # Get the image to process as well as its name and its extension
        image_processor = BusbudBannerBonus() # picture_processor = BusbudBanner()
        image_name, extension = image_processor.picture_data(self.tuple_picture)
       
        # Scale, blur and crop the image
        top_image, middle_image, bottom_image = \
        image_processor.scale_blur_crop(self.threadID, image_name, self.tuple_picture[1])
        
        # Save the generated pictures
        directory_path = "./processed_images/"
        image_processor.save(directory_path + top_image[0] + "_bonus" + "." \
        + extension,  top_image[1]) # top_image is a tuple
        image_processor.save(directory_path + middle_image[0] + "_bonus" + \
        "." + extension,  middle_image[1]) 
        image_processor.save(directory_path +  bottom_image[0] + "_bonus" \
        + "." + extension,  bottom_image[1]) 
        

class ParallelProcessing ():
    """ Provide functions to launch the processes allowing the concurrent 
    processing of images. For more details about multiprocessing, see 
    https://docs.python.org/2/library/multiprocessing.html"""

    def __init__(self):
	"""Class's constructor"""
        pass

    def execute_processes(self, image_iterator):
        """Launch concurrent processes to handle the scaling, blurring
        and cropping of images"""
        # Create a process per image and start it
        process_index = 1
        processList = []
        banner = BusbudBannerBonus()
        for tuple_image in image_iterator:
             image_process = ImageProcess(process_index, banner.load(tuple_image.name, tuple_image))
             print("The process {} is launched to process the image {}".format(process_index, \
             tuple_image.name) + "\n")
             image_process.process_.start()
             processList.append(image_process)
             process_index += 1
        
        for image_process in processList:
            image_process.process_.join() # to ensure that all the processes have finished

        print("End of the images processing.")


def main():
    #raise NotImplementedError
    image_iterator = images()  # get an iterator over the images to process
    concurrency = ParallelProcessing() 
    concurrency.execute_processes(image_iterator) # launch the threads allowing the concurrent 
                                                  # processing of the the images

    print "Exiting Main Thread."


if __name__ == '__main__':
    main()

# To avoid the program to shut right after the execution (Windows)
#os.system("pause")
