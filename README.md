# instapy
---
This package contains tools for turning your image of choice into a dramatic grayscale or nostalgic sepia image.
The package contains a selection of implementations (pure python, numpy, and numba) to perform these tasks, as well as a module to report the time it takes to run the various implementations, for comparison. Finally, the package also includes a Command Line Interface (CLI), for ease of use. 

## Installation:
1. First, clone the repository to your local machine using git:
```bash
git clone https://github.uio.no/IN3110/IN3110-stefansp.git
cd in3110_instapy
```

2. Install the dependencies with pip:
```bash
pip install .
```
(If that doesn't work, try replacing pip with pip3.)

## How to run the package: 
To run the package, run it in a terminal by typing `instapy [path_to_some_image]`.
For example: `instapy ./some/path/my_image.png`.

By default, this will **display** a **grayscale** version of your image, and the conversion will be done using the **python** implementation.

You can run the `-h`or `--help` flag to display an overview of all the optional functions and how to use them: `instapy -h`. 

### Saving the image
To save the image, you can include a filename or a path after a `-o` or `--out` flag. Like this: `instapy ./path/my_image.png -o new_file_name.png` Don't forget to include a file extension, like .png, .jpg, and so on. Also, if no path is specified, then the file will be saved to the current working directory. 

### Selecting filters
You can choose between a grayscale or a sepia filter. This is done by including the flags `-g` or `--gray` for grayscale, or `-se` or `--sepia` for sepia. If no filter is selected, it will default to gray. 

### Rescaling the image
You can rescale the image by inclduing the `-sc` or `--scale` flags, followed by the scale you wish to adjust the image with. The default scale is `1`. For example: `instapy my_image.png -sc 2` will double the size of the image, while `instapy my_image.png -sc 0.5` will halve the image size. 

### Selecting an implementation
You can choose which implementation of the filter functions you want to run. These include python, numpy and numba implementations, all of which may vary in performance. To select a implementation, inlcude the `-i` or `--implementation` flag, followed by your desired implementation. 
For example: `instapy my_image.png -i numpy` will apply a grayscale filter using the numpy implementation. 

### Runtime tracking
You can see how long it takes on average to run your selected implementation. Do do this, include the flag `-r` or `--runtime`, and the result will be printed to the terminal.

