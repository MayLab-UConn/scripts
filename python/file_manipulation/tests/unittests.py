import unittest
import numpy as np  # noqa
import sys
sys.path.append('./..')
import file_io    # noqa


# ----------------------------------------------
# io tests
# ----------------------------------------------
class test_load_xvg(unittest.TestCase):

    def test_xvg_1D(self):
        data = file_io.load_xvg('files/testFileIO/data_1D.xvg', dims=1)
        self.assertEqual(data.shape[0], 6)
        self.assertEqual(data.shape[1], 10)
        self.assertEqual(data.shape[2], 1)

    def test_xvg_2D(self):
        data = file_io.load_xvg('files/testFileIO/data_2D.xvg', dims=2)
        self.assertEqual(data.shape[0], 6)
        self.assertEqual(data.shape[1], 10)
        self.assertEqual(data.shape[2], 2)

    def test_xvg_3D(self):
        data = file_io.load_xvg('files/testFileIO/data_3D.xvg', dims=3)
        self.assertEqual(data.shape[0], 6)
        self.assertEqual(data.shape[1], 10)
        self.assertEqual(data.shape[2], 3)

    def test_fakedata_3D(self):
        #  make sure reordering is correct, values actually right
        data = file_io.load_xvg('files/testFileIO/fake_3D_data.xvg', dims=3)
        self.assertEqual(data[1, 1, 0], 10)
        self.assertEqual(data[1, 1, 1], 11)
        self.assertEqual(data[1, 1, 2], 12)

    def test_xvg_return_time(self):
        data, time = file_io.load_xvg('files/testFileIO/data_3D.xvg', dims=3, return_time_data=True)
        self.assertEqual(time.size, 6)

    def test_xvg_comments(self):
        data = file_io.load_xvg('files/testFileIO/data_&comments.xvg', dims=3, comments=('#', '@', '&'))
        self.assertEqual(data.shape[0], 6)
        self.assertEqual(data.shape[1], 10)
        self.assertEqual(data.shape[2], 3)

    def test_xvg_column_mismatch_error(self):
        self.assertRaises(ValueError, file_io.load_xvg, 'files/testFileIO/data_1D.xvg', dims=3)


if __name__ == '__main__':
    unittest.main()
