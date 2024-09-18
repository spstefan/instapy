from in3110_instapy import python_filters, numba_filters, numpy_filters
from in3110_instapy import io
import numpy as np
from pathlib import Path

def test_compare_implementations():

    """
    Compares the results of the different implementations to verify that they're
    sufficiently similar. The test compares the results of the sepia filters.
    """

    # read image
    file_path = Path("test") / "pixel.png"
    im = io.read_image(file_path)

    # slices away potential 4th channel (alpha) that .png files may have
    im = im[:, :, :3] 

    # get results
    sepia_python = python_filters.python_color2sepia(im)
    sepia_numpy = numpy_filters.numpy_color2sepia(im)
    sepia_numba = numba_filters.numba_color2sepia(im)

    # compare results
    np.testing.assert_allclose(sepia_python, sepia_numpy)
    np.testing.assert_allclose(sepia_python, sepia_numba)
