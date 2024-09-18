from __future__ import annotations

import time
from typing import Callable
from functools import wraps

from . import get_filter, io


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """

    timed_function = timing_decorator(filter_function)
    
    total_time = 0
    for _ in range(calls):  # run the filter function `calls` times
        _, elapsed_time = timed_function(*arguments)
        total_time += elapsed_time

    # return the _average_ time of one call
    average_time = total_time / calls
    return average_time
    


def make_reports(filename: str = "test/Alexander_the_Great_mosaic.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
        calls (int):
            The number of times to call the function,
            for measurement
    
    Returns:
        None
    
    Outputs: 
        timing-report.txt(file): simple text file displaying the timing report in the root dir. 
    """

    # load the image, display it and print its dimensions
    image = io.read_image(filename)

    io.display(image)

    height, width, _ = image.shape

    with open('timing-report.txt', 'w') as report_file:

        file_info = f"Timing performed using {filename}: {width}x{height}\n"
        report_file.write(file_info)

        # iterate through the filters
        filter_names = ["color2gray", "color2sepia"]
        for filter_name in filter_names:
            # get the reference filter function
            reference_filter = get_filter(filter_name, "python")

            # time the reference implementation
            timed_filter = timing_decorator(reference_filter)
            _, reference_time = timed_filter(image) # We're only interested in the time here

            reference_info = f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})\n"
            report_file.write(reference_info)

            # iterate through the implementations
            implementations = ["numpy", "numba"]
            for implementation in implementations:
                filter = get_filter(filter_name, implementation)
                # time the filter
                timed_filter = timing_decorator(filter)
                _, filter_time = timed_filter(image)
                # compare the reference time to the optimized time
                speedup = reference_time / filter_time
                
                filter_info = f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)\n"
                report_file.write(filter_info)
            
            report_file.write("\n")


def timing_decorator(func):
    """ 
    This decorator times a given function, and returns the return-value of the function 
    as well as the elapsed time.

    Parameters: 
        func: 
            The given function to be timed.

    Returns: 
        result:
            The return-value of the passed function
        elapsed_time: 
            The time it took to run and complete the given function
    """
    @wraps(func) 
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return result, elapsed_time  
    return wrapper


if __name__ == "__main__":
    # run as `python -m in3110_instapy.timing`
    make_reports()
