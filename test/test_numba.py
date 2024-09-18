import numpy.testing as nt
from in3110_instapy.numba_filters import numba_color2gray, numba_color2sepia
from in3110_instapy import io
import numpy as np
from pathlib import Path

"""
Unit tests for the numba implementation of color2gray and color2sepia respectively. 
The tests check that functions return correct values and the correct corresponding types. 
Further, they check wheter the filters have been applied correctly, by checking a few 
selected pixels. 

Note: I have provided an image specifically for testing, called pixel.jpg. This is a 2x2px image
with varying colours, to make it easier to implement certain tests. 

Note: I see in retrospect that I should perhaps had used the output from the
python implementation as a reference. I believe my solution should be fine for this kind of unit test, however. 
"""

def test_color2gray(image, reference_gray):

    # run color2gray
    file_path = Path("test") / "pixel.png"
    im = io.read_image(file_path)

    # slices away potential 4th channel (alpha) that .png files may have
    im = im[:, :, :3] 

    gray = numba_color2gray(im)
    io.display(gray)

    # check that the result has the right shape, type
    assert isinstance(gray, np.ndarray)
    assert len(gray.shape) == 3
    assert gray.dtype == np.uint8

    # assert uniform r,g,b values
    pixel_coordinates = [
    (0, 0),
    (0, 1), 
    (1, 0),
    (1, 1) 
    ]

    for x, y in pixel_coordinates:
        r, g, b = gray[x, y]
        assert r == g == b, f"Expected uniform r,g,b values at ({x}, {y}), but found non-uniform values: ({r}, {g}, {b})"


def test_color2sepia(image, reference_sepia):

    # run color2sepia
    file_path = Path("test") / "pixel.png"
    im = io.read_image(file_path)
    
    # slices away potential 4th channel (alpha) that .png files may have
    im = im[:, :, :3] 

    sepia = numba_color2sepia(im)
    io.display(sepia)

    # check that the result has the right shape, type
    assert isinstance(sepia, np.ndarray)
    assert len(sepia.shape) == 3
    assert sepia.dtype == np.uint8

    # expected sepia values based on pixel.png in the test directory
    expected_sepia = np.array( [
    [[48, 43, 33], [148, 132, 103]],
    [[100, 89, 69], [196, 175, 136]]
    ], dtype=np.uint8)

    # verify the pixels against expected sepia values
    # tolerance set to +- 1 unit to avoid rounding errors
    np.testing.assert_allclose(sepia, expected_sepia,  atol=1)