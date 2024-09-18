"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys

from in3110_instapy import python_filters, numpy_filters, numba_filters, timing
import numpy as np
from PIL import Image

from . import io

# Implementation + filter combination for ease of use later
IMPLEMENTATIONS = {
    "python": {
        "color2gray": python_filters.python_color2gray,
        "color2sepia": python_filters.python_color2sepia
    },
    "numpy": {
        "color2gray": numpy_filters.numpy_color2gray,
        "color2sepia": numpy_filters.numpy_color2sepia
    },
    "numba": {
        "color2gray": numba_filters.numba_color2gray,
        "color2sepia": numba_filters.numba_color2sepia
    }
}

def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Run the selected filter"""

    # Load the image from a file
    image = io.read_image(file)

    if scale != 1:
        height, width = image.shape[:2]

        # Convert into PIL image for resizing
        as_image = Image.fromarray(image)

        new_width = int(width * scale)
        new_height = int(height * scale)
        resized = as_image.resize((new_width, new_height))
       
        # Convert back into np.array
        image = np.array(resized)

    # Apply the filter
    selected_implementation = IMPLEMENTATIONS[implementation][filter]
    filtered = selected_implementation(image)

    if out_file:
        # save the file, if out-flag was selected
        filtered = io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", type=str, help="The output filename")

    filter_group = parser.add_mutually_exclusive_group(required=False) # Ensures only one of the filters is selected
    filter_group.add_argument("-g", "--gray", action="store_true", help="Apply a gray filter to the image")
    filter_group.add_argument("-se", "--sepia", action="store_true", help="Apply a sepia filter to the image")

    parser.add_argument("-sc", "--scale", type=float, default=1, help="Set a scale factor to resize the image. Default scale is 1.")
    
    parser.add_argument("-i", "--implementation", 
                        choices=["python", "numba", "numpy"], # Omitting cython since it's not implemented.
                        default="python",
                        help="Select which implementation to run")
    
    parser.add_argument("-r", "--runtime", action="store_true", help="Tracks the average runtime over 3 runs with the currently selected implementation." )


    # parse arguments and call run_filter
    args = parser.parse_args(argv)

    file = args.file
    out_file = args.out
    filter = "color2sepia" if args.sepia else "color2gray"
    scale = args.scale
    implementation = args.implementation

    if args.runtime:
        image_array = io.read_image(file)
        selected_filter_func = IMPLEMENTATIONS[implementation][filter]
        runtime = timing.time_one(selected_filter_func, image_array)
        print(f"Average time over 3 runs: {runtime:.3f}s")
    
    run_filter(file, out_file, implementation, filter, scale)